from ..coupon_registry import CouponRegistry
from ..coupon_strategy_base import CouponStrategy

@CouponRegistry.register("product-wise")
class ProductWiseStrategy(CouponStrategy):
    def calculate_discount(self, details, cart):
        pid = details.get("product_id")
        discount_pct = details.get("discount", 0)
        return sum(item["quantity"] * item["price"] * (discount_pct / 100.0) for item in cart["items"] if item["product_id"] == pid)

    def apply_to_cart(self, details, cart, discount):
        pid = details.get("product_id")
        disc_pct = details.get("discount", 0)
        updated_items = []
        for i in cart["items"]:
            item_copy = {**i, "total_discount": 0.0}
            if i["product_id"] == pid:
                item_copy["total_discount"] = round(i["quantity"] * i["price"] * (disc_pct / 100.0), 2)
            updated_items.append(item_copy)
        total_price = sum(i["quantity"] * i["price"] for i in cart["items"])
        return {
            "items": updated_items,
            "total_price": round(total_price, 2),
            "total_discount": round(discount, 2),
            "final_price": round(total_price - discount, 2)
        }