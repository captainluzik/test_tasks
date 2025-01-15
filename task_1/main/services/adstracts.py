from abc import ABC, abstractmethod
from task_1.main.models import Cart, Discount
from typing import Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, cart: Cart, discount: Discount) -> None:
        pass


class GatewayAbstract(ABC):

    def __init__(self, base_url: str, merchant_domain: str, api_key: str) -> None:
        self.base_url: str = base_url
        self.merchant_domain: str = merchant_domain
        self.api_key: str = api_key

    @abstractmethod
    def _make_headers(self) -> Dict[str, str]:
        pass

    def __make_request(self, method: str, endpoint: str, data: Dict[str, Any]) -> requests.Response:

        """Executes a request to the API with retries in case of an error"""

        headers = self._make_headers()

        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)

        match method.lower():
            case "get":
                response = session.get(self.base_url + endpoint, params=data)
            case "post":
                response = session.post(self.base_url + endpoint, json=data, headers=headers)
            case _:
                raise ValueError("Method not supported")

        return response

    def _get(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:

        """Executes a GET request to the API"""

        return self.__make_request("get", endpoint, data)

    def _post(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:

        """Executes a POST request to the API"""

        return self.__make_request("post", endpoint, data)
