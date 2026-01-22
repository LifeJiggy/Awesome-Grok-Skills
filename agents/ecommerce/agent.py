"""
Ecommerce Agent
E-commerce operations and management
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class ProductStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class ProductCatalog:
    """Product catalog management"""
    
    def __init__(self):
        self.products = {}
        self.categories = {}
        self.inventory = {}
    
    def add_product(self,
                   name: str,
                   sku: str,
                   price: float,
                   category: str,
                   attributes: Dict = None) -> str:
        """Add product to catalog"""
        product_id = f"prod_{len(self.products) + 1}"
        
        self.products[product_id] = {
            "id": product_id,
            "name": name,
            "sku": sku,
            "price": price,
            "category": category,
            "status": ProductStatus.DRAFT,
            "attributes": attributes or {},
            "created_at": datetime.now()
        }
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(product_id)
        
        self.inventory[product_id] = {
            "quantity": 0,
            "reserved": 0,
            "low_stock_threshold": 10
        }
        
        return product_id
    
    def update_product(self, product_id: str, updates: Dict) -> bool:
        """Update product"""
        if product_id not in self.products:
            return False
        
        self.products[product_id].update(updates)
        self.products[product_id]["updated_at"] = datetime.now()
        return True
    
    def get_product(self, product_id: str) -> Dict:
        """Get product details"""
        if product_id not in self.products:
            return {"error": "Product not found"}
        
        product = self.products[product_id].copy()
        product["inventory"] = self.inventory.get(product_id, {})
        return product
    
    def search_products(self, query: str = None, category: str = None, 
                       min_price: float = None, max_price: float = None) -> List[Dict]:
        """Search products"""
        results = []
        
        for product in self.products.values():
            if query and query.lower() not in product["name"].lower():
                continue
            if category and product["category"] != category:
                continue
            if min_price is not None and product["price"] < min_price:
                continue
            if max_price is not None and product["price"] > max_price:
                continue
            
            results.append(product)
        
        return results


class ShoppingCart:
    """Shopping cart operations"""
    
    def __init__(self):
        self.carts = {}
    
    def create_cart(self, user_id: str) -> str:
        """Create new cart"""
        cart_id = f"cart_{len(self.carts) + 1}"
        self.carts[cart_id] = {
            "user_id": user_id,
            "items": [],
            "created_at": datetime.now()
        }
        return cart_id
    
    def add_item(self, cart_id: str, product_id: str, quantity: int = 1) -> Dict:
        """Add item to cart"""
        if cart_id not in self.carts:
            return {"error": "Cart not found"}
        
        cart = self.carts[cart_id]
        
        for item in cart["items"]:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                return item
        
        cart["items"].append({
            "product_id": product_id,
            "quantity": quantity,
            "added_at": datetime.now()
        })
        
        return cart["items"][-1]
    
    def calculate_total(self, cart_id: str) -> Dict:
        """Calculate cart total"""
        if cart_id not in self.carts:
            return {"error": "Cart not found"}
        
        subtotal = 0
        for item in self.carts[cart_id]["items"]:
            subtotal += item.get("price", 0) * item["quantity"]
        
        tax = subtotal * 0.1
        shipping = 5.99 if subtotal < 50 else 0
        
        return {
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "shipping": shipping,
            "total": round(subtotal + tax + shipping, 2)
        }
    
    def checkout(self, cart_id: str, shipping_address: Dict) -> Dict:
        """Process checkout"""
        if cart_id not in self.carts:
            return {"error": "Cart not found"}
        
        totals = self.calculate_total(cart_id)
        
        order = {
            "order_id": f"order_{len(self.carts) + 1}",
            "cart_id": cart_id,
            "items": self.carts[cart_id]["items"],
            "totals": totals,
            "shipping_address": shipping_address,
            "status": "processing",
            "created_at": datetime.now()
        }
        
        del self.carts[cart_id]
        
        return order


class OrderManager:
    """Order management"""
    
    def __init__(self):
        self.orders = {}
        self.fulfillment_queue = []
    
    def create_order(self, user_id: str, items: List[Dict], shipping_address: Dict) -> str:
        """Create new order"""
        order_id = f"order_{len(self.orders) + 1}"
        
        self.orders[order_id] = {
            "id": order_id,
            "user_id": user_id,
            "items": items,
            "shipping_address": shipping_address,
            "status": "pending",
            "payment_status": "paid",
            "created_at": datetime.now()
        }
        
        self.fulfillment_queue.append(order_id)
        return order_id
    
    def update_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        if order_id not in self.orders:
            return False
        
        self.orders[order_id]["status"] = status
        self.orders[order_id]["updated_at"] = datetime.now()
        
        if status == "shipped":
            self.orders[order_id]["shipped_at"] = datetime.now()
        
        return True
    
    def get_order_history(self, user_id: str) -> List[Dict]:
        """Get user order history"""
        return [o for o in self.orders.values() if o["user_id"] == user_id]


class PricingEngine:
    """Dynamic pricing operations"""
    
    def __init__(self):
        self.pricing_rules = []
    
    def apply_discount(self, 
                      product_id: str,
                      base_price: float,
                      discount_type: str = "percentage",
                      discount_value: float = 0) -> Dict:
        """Calculate discounted price"""
        if discount_type == "percentage":
            discount_amount = base_price * (discount_value / 100)
        elif discount_type == "fixed":
            discount_amount = discount_value
        else:
            discount_amount = 0
        
        final_price = max(0, base_price - discount_amount)
        
        return {
            "original_price": base_price,
            "discount_amount": discount_amount,
            "final_price": round(final_price, 2),
            "savings_percent": round(discount_amount / base_price * 100, 1) if base_price > 0 else 0
        }
    
    def calculate_bundle_price(self, items: List[Dict], discount_percent: float = 10) -> Dict:
        """Calculate bundle pricing"""
        subtotal = sum(item["price"] * item["quantity"] for item in items)
        bundle_discount = subtotal * (discount_percent / 100)
        
        return {
            "original_total": subtotal,
            "bundle_discount": round(bundle_discount, 2),
            "bundle_price": round(subtotal - bundle_discount, 2),
            "savings": round(bundle_discount, 2)
        }


class InventoryManager:
    """Inventory management"""
    
    def __init__(self):
        self.inventory = {}
        self.movements = []
    
    def adjust_stock(self, product_id: str, quantity_change: int, reason: str = "manual"):
        """Adjust inventory"""
        if product_id not in self.inventory:
            self.inventory[product_id] = {"quantity": 0, "reserved": 0}
        
        self.inventory[product_id]["quantity"] += quantity_change
        
        self.movements.append({
            "product_id": product_id,
            "change": quantity_change,
            "new_quantity": self.inventory[product_id]["quantity"],
            "reason": reason,
            "timestamp": datetime.now()
        })
    
    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Reserve stock for order"""
        if product_id not in self.inventory:
            return False
        
        available = self.inventory[product_id]["quantity"] - self.inventory[product_id]["reserved"]
        if available < quantity:
            return False
        
        self.inventory[product_id]["reserved"] += quantity
        return True
    
    def get_stock_status(self, product_id: str) -> Dict:
        """Get stock status"""
        if product_id not in self.inventory:
            return {"error": "Product not found"}
        
        inv = self.inventory[product_id]
        return {
            "quantity": inv["quantity"],
            "reserved": inv["reserved"],
            "available": inv["quantity"] - inv["reserved"],
            "low_stock": (inv["quantity"] - inv["reserved"]) < 10,
            "out_of_stock": (inv["quantity"] - inv["reserved"]) <= 0
        }
    
    def generate_report(self) -> Dict:
        """Generate inventory report"""
        low_stock = []
        out_of_stock = []
        
        for product_id, inv in self.inventory.items():
            available = inv["quantity"] - inv["reserved"]
            if available <= 0:
                out_of_stock.append(product_id)
            elif available < 10:
                low_stock.append(product_id)
        
        return {
            "total_products": len(self.inventory),
            "low_stock_count": len(low_stock),
            "out_of_stock_count": len(out_of_stock),
            "total_value": sum(
                inv["quantity"] * 100 for inv in self.inventory.values()
            ),
            "low_stock_items": low_stock[:10],
            "out_of_stock_items": out_of_stock[:10]
        }


if __name__ == "__main__":
    catalog = ProductCatalog()
    product_id = catalog.add_product("Laptop", "SKU-001", 999.99, "Electronics")
    products = catalog.search_products(category="Electronics")
    
    cart = ShoppingCart()
    cart_id = cart.create_cart("user_123")
    cart.add_item(cart_id, product_id, 1)
    totals = cart.calculate_total(cart_id)
    order = cart.checkout(cart_id, {"address": "123 Main St"})
    
    orders = OrderManager()
    order_id = orders.create_order("user_123", [{"product_id": product_id, "quantity": 1, "price": 999.99}], {})
    orders.update_status(order_id, "shipped")
    
    pricing = PricingEngine()
    discounted = pricing.apply_discount(product_id, 999.99, "percentage", 20)
    bundle = pricing.calculate_bundle_price([
        {"product_id": product_id, "quantity": 1, "price": 999.99},
        {"product_id": "prod_2", "quantity": 1, "price": 49.99}
    ], 15)
    
    inventory = InventoryManager()
    inventory.adjust_stock(product_id, 100, "initial_stock")
    inventory.reserve_stock(product_id, 2)
    status = inventory.get_stock_status(product_id)
    report = inventory.generate_report()
    
    print(f"Product ID: {product_id}")
    print(f"Cart total: ${totals['total']:.2f}")
    print(f"Order ID: {order['order_id']}")
    print(f"Discounted price: ${discounted['final_price']:.2f}")
    print(f"Bundle savings: ${bundle['savings']:.2f}")
    print(f"Stock available: {status['available']}")
    print(f"Low stock items: {len(report['low_stock_items'])}")
