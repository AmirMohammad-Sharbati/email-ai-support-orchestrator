from src.mock_data.mock_apis import MockRefundAPI

class RefundService:
    async def get_policy(self) -> dict:
        """Get refund policy from mock API"""
        return await MockRefundAPI.get_refund_policy()