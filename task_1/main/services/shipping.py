from .adstracts import GatewayAbstract
from typing import Dict, Any


class ShippingGateway(GatewayAbstract):

    def __init__(self, base_url: str, merchant_domain: str, api_key: str) -> None:
        super().__init__(base_url, merchant_domain, api_key)

    def _make_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"X-Api-Key {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_shipping(self, order_id: int, address: str) -> Dict[str, Any]:
        endpoint = "shipping"
        data = {
            "order_id": order_id,
            "address": address,
            "service_url": f"{self.merchant_domain}/api/shipping/callback",
        }
        response = self._post(endpoint, data)
        return response.json()
