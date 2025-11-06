from sqlalchemy.orm import Session
from . import models, schemas

def create_coupon(db: Session, coupon_in: schemas.CouponCreate):
    coupon = models.Coupon(
        type=coupon_in.type,
        details=coupon_in.details,
        is_active=coupon_in.is_active,
        expires_at=coupon_in.expires_at,
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

def get_coupon(db: Session, coupon_id: int):
    return db.query(models.Coupon).filter(models.Coupon.id == coupon_id).first()

def list_coupons(db: Session):
    return db.query(models.Coupon).all()

def update_coupon(db: Session, coupon_id: int, coupon_in: dict):
    c = get_coupon(db, coupon_id)
    if not c:
        return None

    for field, value in coupon_in.items():
        setattr(c, field, value)

    db.commit()
    db.refresh(c)
    return c


def delete_coupon(db: Session, coupon_id: int):
    c = get_coupon(db, coupon_id)
    if not c:
        return False
    db.delete(c)
    db.commit()
    return True
