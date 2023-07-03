import typing as T

import requests

from util import log, wait

MY_IP_URL = "http://icanhazip.com/"


class Web2Client:
    def __init__(
        self,
        base_url: str = "",
        rate_limit_delay: float = 5.0,
        dry_run: bool = False,
    ) -> None:
        self.dry_run = dry_run
        self.base_url = base_url
        self.rate_limit_delay = rate_limit_delay

        if dry_run:
            log.print_warn("Web2Client in dry run mode...")

        self.requests = requests

    def get_request(
        self,
        url: str,
        headers: T.Optional[T.Dict[str, T.Any]] = None,
        params: T.Optional[T.Dict[str, T.Any]] = None,
        timeout: float = 5.0,
    ) -> T.Any:
        if self.rate_limit_delay > 0.0:
            wait.wait(self.rate_limit_delay)

        if headers is None:
            headers = {}

        if params is None:
            params = {}

        try:
            return self.requests.request(
                "GET", url, params=params, headers=headers, timeout=timeout
            ).json()
        except KeyboardInterrupt:
            raise
        except:  # pylint: disable=bare-except
            return {}

    def post_request(
        self,
        url: str,
        json_data: T.Optional[T.Dict[str, T.Any]] = None,
        headers: T.Optional[T.Dict[str, T.Any]] = None,
        params: T.Optional[T.Dict[str, T.Any]] = None,
        timeout: float = 5.0,
        delay: float = 5.0,
    ) -> T.Any:
        if self.dry_run:
            return {}

        if headers is None:
            headers = {}

        if params is None:
            params = {}

        if json_data is None:
            json_data = {}

        if delay > 0.0:
            wait.wait(delay)

        try:
            return self.requests.request(
                "POST",
                url,
                json=json_data,
                params=params,
                headers=headers,
                timeout=timeout,
            ).json()
        except KeyboardInterrupt:
            raise
        except:  # pylint: disable=bare-except
            log.format_fail(f"Failed to post to {url}")
            return {}

    def url_download(
        self,
        url: str,
        file_path: str,
        data: str,
        headers: T.Optional[T.Dict[str, T.Any]] = None,
        params: T.Optional[T.Dict[str, T.Any]] = None,
        timeout: float = 5.0,
    ) -> None:
        if self.dry_run:
            return

        if headers is None:
            headers = {}

        if params is None:
            params = {}

        try:
            with self.requests.request(
                "GET",
                url,
                data=data,
                params=params,
                headers=headers,
                timeout=timeout,
                stream=True,
                allow_redirects=True,
            ) as response:
                response.raise_for_status()
                with open(file_path, "wb") as outfile:
                    for chunk in response.iter_content(chunk_size=8192):
                        outfile.write(chunk)
        except KeyboardInterrupt:
            raise
        except:  # pylint: disable=bare-except
            log.format_fail(f"Failed to download {url} to {file_path}")
            return
