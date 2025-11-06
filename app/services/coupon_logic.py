from typing import Dict
from .coupon_registry import CouponRegistry
from .strategies import *  # noqa: F401,F403  # ensure registration

def calc_discount_for_coupon(coupon: Dict, cart: Dict) -> float:
    strategy_cls = CouponRegistry.get(coupon["type"])
    if not strategy_cls:
        return 0.0
    strategy = strategy_cls()
    return strategy.calculate_discount(coupon["details"], cart)
