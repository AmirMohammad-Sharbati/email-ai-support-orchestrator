from src.mock_data.mock_apis import MockOrderAPI

class OrderService:
    async def get_status(self, order_id: str) -> dict:
        """Get order status from mock API"""
        return await MockOrderAPI.get_order_status(order_id)