"""Mock APIs for order, product, and refund services"""

class MockOrderAPI:
    """Mock order status API"""
    
    @staticmethod
    async def get_order_status(order_id: str) -> dict:
        # Mock database
        statuses = {
            "1234": {
                "status": "Shipped - Out for delivery",
                "estimated_delivery": "Tomorrow",
                "tracking_number": "TRK123456789",
                "carrier": "FedEx"
            },
            "5678": {
                "status": "Processing - Will ship in 2 days",
                "estimated_delivery": "3-5 business days",
                "tracking_number": None,
                "carrier": None
            },
            "9999": {
                "status": "Delivered - Signed by customer",
                "estimated_delivery": "Delivered on Jan 15",
                "tracking_number": "TRK987654321",
                "carrier": "UPS"
            }
        }
        
        info = statuses.get(order_id, {
            "status": f"Order {order_id} found - In warehouse",
            "estimated_delivery": "Pending confirmation",
            "tracking_number": None,
            "carrier": None
        })
        
        return {
            "tool": "order_status",
            "order_id": order_id,
            **info
        }

class MockProductAPI:
    """Mock product information API"""
    
    @staticmethod
    async def get_product_info(product_name: str) -> dict:
        products = {
            "speaker": {
                "name": "Bluetooth Speaker X200",
                "warranty": "2 years limited warranty",
                "support": "24/7 technical support via chat",
                "manual_url": "https://support.example.com/speaker-x200",
                "troubleshooting": "Try resetting by holding power button for 10 seconds"
            },
            "laptop": {
                "name": "UltraBook Pro",
                "warranty": "1 year manufacturer warranty",
                "support": "Phone support: 1-800-555-0123",
                "manual_url": "https://support.example.com/ultrabook-pro",
                "drivers_url": "https://drivers.example.com/ultrabook-pro"
            },
            "headphone": {
                "name": "Noise Cancelling Headphones H9",
                "warranty": "18 months",
                "support": "Email support@example.com",
                "manual_url": "https://support.example.com/headphones-h9"
            }
        }
        
        product_key = product_name.lower()
        info = products.get(product_key, {
            "name": product_name,
            "warranty": "Standard warranty applies",
            "support": "Contact support@example.com for assistance",
            "manual_url": "https://support.example.com/products"
        })
        
        return {
            "tool": "product_info",
            "product_name": product_name,
            **info
        }

class MockRefundAPI:
    """Mock refund policy API"""
    
    @staticmethod
    async def get_refund_policy() -> dict:
        return {
            "tool": "refund_policy",
            "policy": """Our refund policy:
- 30-day return window from delivery date
- Original packaging required
- Product must be in original condition
- Refund processed within 5-7 business days
- Shipping costs are non-refundable
- For defective products, we cover return shipping""",
            "return_address": "Returns Dept, 123 Business St, City, ZIP",
            "processing_time": "5-7 business days",
            "conditions": ["Original packaging", "Undamaged product", "Proof of purchase"]
        }