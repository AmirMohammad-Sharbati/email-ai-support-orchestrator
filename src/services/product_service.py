from mock_data.mock_apis import MockProductAPI

class ProductService:
    async def get_info(self, product_name: str) -> dict:
        """Get product info from mock API"""
        return await MockProductAPI.get_product_info(product_name)