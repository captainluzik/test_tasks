from typing import Dict, Any
from .adstracts import GatewayAbstract


class PaymentGateway(GatewayAbstract):
    """Class for interacting with the Payment Gateway API"""

    def __init__(self, base_url: str, merchant_domain: str, api_key: str) -> None:
        super().__init__(base_url, merchant_domain, api_key)

    def _make_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_payment(self, amount: float, order_id: int) -> Dict[str, Any]:
        endpoint = "payments"
        data = {
            "amount": amount,
            "order_id": order_id,
            "service_url": f"{self.merchant_domain}/api/payments/callback",
        }
        response = self._post(endpoint, data)
        return response.json()
