import copy
import datetime
import enum
import json
import threading
import time
import typing as T

import deepdiff
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.watch import DocumentChange

from firebase import data_types
from property_guru.data_types import SearchParams
from util import log
from util.dict_util import check_dict_keys_recursive, patch_missing_keys_recursive, safe_get


class Changes(enum.Enum):
    ADDED = 1
    MODIFIED = 2
    REMOVED = 3


class FirebaseUser:
    TIME_FORMAT = "%Y_%m_%d%H_%M_%S_%f"
    HEALTH_PING_TIME = 60 * 30

    def __init__(self, credentials_file: str, verbose: bool = False) -> None:
        if not firebase_admin._apps:
            auth = credentials.Certificate(credentials_file)
            firebase_admin.initialize_app(auth)
        self.db = firestore.client()
        self.verbose = verbose

        self.user_ref: CollectionReference = self.db.collection("user")
        self.admin_ref: CollectionReference = self.db.collection("admin")

        self.users_watcher = self.user_ref.on_snapshot(self._collection_snapshot_handler)

        self.db_cache: T.Dict[str, data_types.User] = {}

        self.callback_done: threading.Event = threading.Event()
        self.db_cache_lock: threading.Lock = threading.Lock()

        self.last_health_ping: T.Optional[float] = None

    def _delete_user(self, name: str) -> None:
        with self.db_cache_lock:
            if name in self.db_cache:
                del self.db_cache[name]
        log.print_warn(f"Deleting user {name} from cache")

    def _collection_snapshot_handler(
        self,
        collection_snapshot: T.List[DocumentSnapshot],
        changed_docs: T.List[DocumentChange],
        read_time: T.Any,
    ) -> None:
        log.print_warn(f"Received collection snapshot for {len(collection_snapshot)} documents")

        users = self.db_cache.keys()
        with self.db_cache_lock:
            self.db_cache = {}
            for doc in collection_snapshot:
                doc_dict = doc.to_dict()
                if not doc_dict:
                    continue
                self.db_cache[doc.id] = doc_dict  # type: ignore
                log.print_normal(f"{json.dumps(doc_dict, indent=4, sort_keys=True)}")

        for user in users:
            if user not in self.db_cache:
                self._delete_user(user)

        for change in changed_docs:
            doc_id = change.document.id
            email = safe_get(
                dict(self.db_cache[doc_id]), "preferences.notifications.email.email".split("."), ""
            )
            phone_number = safe_get(
                dict(self.db_cache[doc_id]),
                "preferences.notifications.sms.phoneNumber".split("."),
                "",
            )
            if phone_number and not phone_number.startswith("+1"):
                phone_number = "+1" + phone_number

            if change.type.name == Changes.ADDED.name:
                log.print_ok_blue(f"Added document: {doc_id}")
            elif change.type.name == Changes.MODIFIED.name:
                log.print_ok_blue(f"Modified document: {doc_id}")
            elif change.type.name == Changes.REMOVED.name:
                log.print_ok_blue(f"Removed document: {doc_id}")
                self._delete_user(doc_id)

        self.callback_done.set()

    def _handle_firebase_update(self, user: str, db_user: data_types.User) -> None:
        log.print_normal(f"Checking to see if we need to update {user} databases...")
        old_db_user = copy.deepcopy(db_user)

        if not db_user:
            db_user = copy.deepcopy(data_types.NULL_USER)
            log.print_normal(
                f"Initializing new user {user} in database:\n{json.dumps(db_user, indent=4, sort_keys=True)}"
            )
        missing_keys = check_dict_keys_recursive(dict(data_types.NULL_USER), dict(db_user))
        if missing_keys:
            log.print_warn(f"Missing keys in user {user}:\n{missing_keys}")
            patch_missing_keys_recursive(dict(data_types.NULL_USER), dict(db_user))

        diff = deepdiff.DeepDiff(
            old_db_user,
            db_user,
            ignore_order=True,
        )
        if not diff:
            return

        log.print_normal(
            f"Updated client {user} in database:\n{diff.to_json(indent=4, sort_keys=True)}"
        )

    def update_watchers(self) -> None:
        log.print_warn(f"Updating watcher...")
        if self.users_watcher:
            self.users_watcher.unsubscribe()

        self.users_watcher = self.user_ref.on_snapshot(self._collection_snapshot_handler)

    def update_from_firebase(self) -> None:
        """
        Synchronous update from firebase database. We do this periodically to ensure
        that we are not missing any updates from the database. This is a fallback
        mechanism in case the watcher fails, which it seems to periodically do.
        """
        log.print_warn(f"Updating from firebase database instead of cache")
        users = self.db_cache.keys()
        with self.db_cache_lock:
            self.db_cache = {}
            for doc in self.user_ref.list_documents():
                self.db_cache[doc.id] = doc.get().to_dict()

        for user in users:
            if user not in self.db_cache:
                self._delete_user(user)

        self.callback_done.set()

    def check_and_maybe_handle_firebase_db_updates(self) -> None:
        if self.callback_done.is_set():
            self.callback_done.clear()
            log.print_bright("Handling firebase database updates")
            for user, info in self.db_cache.items():
                self._handle_firebase_update(user, info)

    def health_ping(self) -> None:
        if self.last_health_ping and time.time() - self.last_health_ping < self.HEALTH_PING_TIME:
            return

        self.last_health_ping = time.time()

        log.print_ok_arrow("Health ping")
        self.admin_ref.document("health_monitor").set(
            {"heartbeat": firestore.SERVER_TIMESTAMP}, merge=True
        )

    def _get_users(self) -> T.Dict[str, data_types.User]:
        with self.db_cache_lock:
            return copy.deepcopy(self.db_cache)

    def get_search_params(self) -> T.Dict[str, SearchParams]:
        user_search_params = {}
        with self.db_cache_lock:
            for user, info in self.db_cache.items():
                property_id = info["searchParams"]["searchString"].split("-")[-1]
                if isinstance(property_id, str) and not property_id.isdigit():
                    log.print_fail(f"Invalid property id {property_id}!")
                    continue

                search_params: SearchParams = {
                    "minprice": info["searchParams"]["minPrice"],
                    "maxprice": info["searchParams"]["maxPrice"],
                    "beds": list(
                        range(info["searchParams"]["minBeds"], info["searchParams"]["maxBeds"] + 1)
                    ),
                    "baths": list(
                        range(
                            info["searchParams"]["minBaths"], info["searchParams"]["maxBaths"] + 1
                        )
                    ),
                    "minsize": info["searchParams"]["minSize"],
                    "maxsize": info["searchParams"]["maxSize"],
                    "newProject": "all",
                    "search": True,
                    "listing_type": "sale",
                    "market": "residential",
                    "property_id": int(property_id),
                }
                user_search_params[user] = search_params
        return user_search_params

    def get_listing_ids(self) -> T.Dict[str, T.List[int]]:
        user_listing_ids = {}
        with self.db_cache_lock:
            for user, info in self.db_cache.items():
                user_listing_ids[user] = info.get("listingIds", [])
        return user_listing_ids
