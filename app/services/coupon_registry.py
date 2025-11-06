from typing import Dict, Type
from .coupon_strategy_base import CouponStrategy

class CouponRegistry:
    _strategies: Dict[str, Type[CouponStrategy]] = {}

    @classmethod
    def register(cls, coupon_type: str):
        def decorator(strategy_cls: Type[CouponStrategy]):
            cls._strategies[coupon_type] = strategy_cls
            return strategy_cls
        return decorator

    @classmethod
    def get(cls, coupon_type: str):
        return cls._strategies.get(coupon_type)
