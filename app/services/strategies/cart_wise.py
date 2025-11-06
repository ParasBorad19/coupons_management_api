from ..coupon_registry import CouponRegistry
from ..coupon_strategy_base import CouponStrategy

@CouponRegistry.register("cart-wise")
class CartWiseStrategy(CouponStrategy):
    def calculate_discount(self, details, cart):
        threshold = details.get("threshold")
        discount_pct = details.get("discount", 0)
        total = sum(i["quantity"] * i["price"] for i in cart["items"])
        if threshold is not None and total > threshold:
            return total * (discount_pct / 100.0)
        return 0.0

    def apply_to_cart(self, details, cart, discount):
        """
        Default implementation — just attaches total_discount = 0.
        Override this in strategy if the coupon affects specific items.
        """
        updated_items = [{**i, "total_discount": 0.0} for i in cart["items"]]
        return {
            "items": updated_items,
            "total_price": sum(i["quantity"] * i["price"] for i in cart["items"]),
            "total_discount": round(discount, 2),
            "final_price": round(sum(i["quantity"] * i["price"] for i in cart["items"]) - discount, 2)
        }