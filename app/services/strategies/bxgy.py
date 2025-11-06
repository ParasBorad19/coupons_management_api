from ..coupon_registry import CouponRegistry
from ..coupon_strategy_base import CouponStrategy


@CouponRegistry.register("bxgy")
class BxGyStrategy(CouponStrategy):
    def calculate_discount(self, details, cart):
        buy_products = details.get("buy_products", [])
        get_products = details.get("get_products", [])
        repetition_limit = details.get("repetition_limit", 1)

        # Precompute product quantities for faster lookups
        cart_qty_map = {item["product_id"]: item["quantity"] for item in cart["items"]}
        cart_price_map = {item["product_id"]: item["price"] for item in cart["items"]}

        # --- Step 1: Count how many "buy sets" the customer qualifies for ---
        total_buy_sets = 0
        for b in buy_products:
            pid = b["product_id"]
            required_qty = b.get("quantity", 1)
            available_qty = cart_qty_map.get(pid, 0)
            total_buy_sets += available_qty // required_qty

        applicable_times = min(total_buy_sets, repetition_limit)
        if applicable_times <= 0:
            return 0.0

        # --- Step 2: Determine how many free units are eligible ---
        free_units_total = sum(g.get("quantity", 1) for g in get_products) * applicable_times

        # --- Step 3: Identify eligible items for free units ---
        get_product_ids = {g["product_id"] for g in get_products}
        eligible_items = [
            item for item in cart["items"] if item["product_id"] in get_product_ids
        ]

        # --- Step 4: Sort eligible items by price descending (give free expensive ones first) ---
        eligible_items.sort(key=lambda x: x["price"], reverse=True)

        # --- Step 5: Apply the discount ---
        discount = 0.0
        remaining = free_units_total
        for item in eligible_items:
            if remaining <= 0:
                break
            take = min(item["quantity"], remaining)
            discount += take * item["price"]
            remaining -= take

        return discount
    
    def apply_to_cart(self, details, cart, discount):
        updated_items = [{**i, "total_discount": 0.0} for i in cart["items"]]
        remaining = discount
        get_pids = [g["product_id"] for g in details.get("get_products", [])]
        for it in sorted(updated_items, key=lambda x: x["price"], reverse=True):
            if remaining <= 0:
                break
            if it["product_id"] in get_pids:
                alloc = min(it["quantity"] * it["price"], remaining)
                it["total_discount"] = round(alloc, 2)
                remaining -= alloc
        total_price = sum(i["quantity"] * i["price"] for i in cart["items"])
        return {
            "items": updated_items,
            "total_price": round(total_price, 2),
            "total_discount": round(discount, 2),
            "final_price": round(total_price - discount, 2)
        }
