from bioto_client.domain.repository import Repository
from bioto_client.domain.users import User
from bioto_client.domain.auth import SessionExpired
import functools
import requests
from requests import Response


class HTTPException(Exception):
    pass


def response(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> dict:
        response: Response = func(*args, **kwargs)

        if response.status_code < 300:
            return response.json()
        elif response.status_code == 403:
            raise SessionExpired("Session expired")
        else:
            message = response.reason

            has_content = len(response.content) > 0

            if not has_content:
                raise HTTPException(message)

            response_data = response.json()
            if "detail" in response_data:
                message = response_data["detail"]

            raise HTTPException(message)

    return wrapper


class Api(Repository):
    base_endpoint: str
    user: User
    verify_ssl: bool = True

    def __init__(self, user: User, config: list[str]):
        self.user = user
        self.base_endpoint = config["BASE_ENDPOINT"]
        # When not on production use specified CA_BUNDLE as cert or disable
        # ssl altogether
        if config["ENV"] != "prod":
            if "CA_BUNDLE" in config:
                self.verify_ssl = config["CA_BUNDLE"]
            else:
                self.verify_ssl = False

    @response
    def search_garden(self, name: str) -> Response:
        return requests.get(
            f"https://{self.base_endpoint}/gardens/search",
            params={"name": name},
            headers={"Authorization": f"Bearer {self.user.access_token}"},
            verify=self.verify_ssl
        )

    @response
    def get_gardens(self) -> Response:
        return requests.get(
            f"https://{self.base_endpoint}/gardens/",
            headers={"Authorization": f"Bearer {self.user.access_token}"},
            verify=self.verify_ssl
        )

    @response
    def subscribe_garden(self, uuid: str) -> Response | dict:
        return requests.post(
            f"https://{self.base_endpoint}/gardens/{uuid}/subscribe",
            headers={"Authorization": f"Bearer {self.user.access_token}"},
            verify=self.verify_ssl
        )

    @response
    def update_user(self) -> Response:
        return requests.post(
            f"https://{self.base_endpoint}/profile/",
            json={"username": self.user.name},
            headers={"Authorization": f"Bearer {self.user.access_token}"},
            verify=self.verify_ssl
        )
