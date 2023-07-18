import datetime
import typing as T


class HealthMonitor(T.TypedDict):
    reset: bool
    heartbeat: datetime.datetime


class Email(T.TypedDict):
    email: str
    updatesEnabled: bool


class Sms(T.TypedDict):
    phoneNumber: str
    updatesEnabled: bool


class Notifications(T.TypedDict):
    email: Email
    sms: Sms


class Preferences(T.TypedDict):
    notifications: Notifications


class SearchParams(T.TypedDict):
    searchString: str
    minBaths: int
    maxBaths: int
    minBeds: int
    maxBeds: int
    maxPrice: int
    minPrice: int
    maxSize: int
    minSize: int


class User(T.TypedDict):
    preferences: Preferences
    searchParams: SearchParams


NULL_USER = User(
    preferences=Preferences(
        notifications=Notifications(
            email=Email(email="", updatesEnabled=False),
            sms=Sms(
                phoneNumber="",
                updatesEnabled=False,
            ),
        )
    ),
    searchParams=SearchParams(
        searchString="",
        minBaths=0,
        maxBaths=5,
        minBeds=0,
        maxBeds=5,
        maxPrice=10000000,
        minPrice=100000,
        maxSize=6000,
        minSize=0,
    ),
)
