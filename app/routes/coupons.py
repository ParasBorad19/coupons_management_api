from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .. import schemas, crud, models
from ..database import SessionLocal, engine
from ..services.coupon_logic import calc_discount_for_coupon
from ..services.coupon_registry import CouponRegistry

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _is_coupon_usable(c):
    if not c.is_active:
        return False
    if c.expires_at is not None:
        now = datetime.now(timezone.utc)
        exp = c.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if now > exp:
            return False
    return True

@router.post("/coupons", response_model=schemas.CouponOut)
def create_coupon(payload: schemas.CouponCreate, db: Session = Depends(get_db)):
    return crud.create_coupon(db, payload)

@router.get("/coupons", response_model=list[schemas.CouponOut])
def list_coupons(db: Session = Depends(get_db)):
    return crud.list_coupons(db)

@router.get("/coupons/{coupon_id}", response_model=schemas.CouponOut)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    c = crud.get_coupon(db, coupon_id)
    if not c:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return c

@router.patch("/coupons/{coupon_id}", response_model=schemas.CouponOut)
def patch_coupon(
    coupon_id: int,
    payload: schemas.CouponUpdate,
    db: Session = Depends(get_db)
):
    update_data = payload.dict(exclude_unset=True)
    c = crud.update_coupon(db, coupon_id, update_data)
    if not c:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return c


@router.delete("/coupons/{coupon_id}")
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_coupon(db, coupon_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return {"success": True}

@router.post("/applicable-coupons")
def applicable_coupons(payload: dict, db: Session = Depends(get_db)):
    cart = payload.get("cart")
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is required")
    coupons = [c for c in crud.list_coupons(db) if _is_coupon_usable(c)]
    result = []
    for c in coupons:
        discount = calc_discount_for_coupon({"type": c.type, "details": c.details}, cart)
        if discount > 0:
            result.append({"coupon_id": c.id, "type": c.type, "discount": round(discount, 2)})
    return {"applicable_coupons": result}

@router.post("/apply-coupon/{coupon_id}")
def apply_coupon(coupon_id: int, payload: schemas.CartWrapper, db: Session = Depends(get_db)):
    coupon = crud.get_coupon(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    if not _is_coupon_usable(coupon):
        raise HTTPException(status_code=400, detail="Coupon is inactive or expired")

    cart = payload.dict().get('cart')
    discount = calc_discount_for_coupon({"type": coupon.type, "details": coupon.details}, cart)
    strategy_cls = CouponRegistry.get(coupon.type)
    if not strategy_cls:
        raise HTTPException(status_code=400, detail="Unsupported coupon type")

    strategy = strategy_cls()
    updated_cart = strategy.apply_to_cart(coupon.details, cart, discount)
    return {"updated_cart": updated_cart}

