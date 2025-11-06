
# Coupons Management API (FastAPI)

## 📘 Overview

This is a modular and extensible **Coupons Management API** built using **FastAPI** and **SQLAlchemy**.  
It supports multiple coupon types and follows a **Strategy + Registry** pattern to easily extend the system with new coupon logic without changing existing routes.

The project focuses on **correctness**, **design clarity**, **scalability**, and — most importantly — **coverage of diverse coupon use cases**, including those that are **not yet implemented but considered**.

---

## ✨ Key Features Implemented

- CRUD operations for Coupons
- Coupon application logic
- Coupon lifecycle (`is_active`, `expires_at`)
- Coupon types: `cart-wise`, `product-wise`, `bxgy`
- Strategy pattern for extensibility

---

## 🧩 Coupon Types (Implemented + Potential Extensions)

| Type | Description | Status |
|------|--------------|--------|
| **Cart-wise** | Discount applied when total cart value exceeds a threshold. | ✅ Implemented |
| **Product-wise** | Discount applied only on specific product(s). | ✅ Implemented |
| **BxGy (Buy X Get Y)** | Buy certain quantity of one product to get another product(s) free. | ✅ Implemented |
| **Flat Discount** | Straight fixed discount on total cart (e.g., ₹100 off). | 🔹Easy to implement |
| **Category-wise** | Discount applies only to items in a specific category. | 🔹Requires category metadata |
| **Brand-wise** | Discount applies to all products of a certain brand. | 🔹Requires brand info |
| **User-specific** | Coupon valid only for specific users or user segments. | 🔹Needs user auth context |
| **First-time Buyer** | Valid only for first purchase. | 🔹Needs order history tracking |
| **Payment-method-based** | Only valid for specific payment methods (e.g., UPI, credit card). | 🔹Needs payment info in cart |
| **Minimum Item Count** | Valid only if cart has ≥ N items. | 🔹Easy rule extension |
| **Bundle Discount** | Discount applies when multiple specific products are in the cart together. | 🔹Complex condition matching |
| **Tiered Discount** | Progressive discount: 5% for ₹500+, 10% for ₹1000+, etc. | 🔹Requires slab logic |
| **Free Shipping** | Removes delivery charges instead of product discounts. | 🔹Needs shipping integration |
| **Limited-use Coupon** | Can only be used X times globally or per user. | 🔹Requires tracking table |
| **Auto-applied Coupon** | Automatically applied at checkout if eligible. | 🔹Client-side auto detection |
| **Stackable Coupons** | Allow multiple coupons on one order. | ⚠️ Difficult — needs precedence and conflict handling |

---

## 🎯 Edge Cases Considered

| # | Case | Description | Current Behavior |
|---|------|--------------|------------------|
| 1 | Cart total below threshold | Discount skipped | ✅ Handled |
| 2 | Product not present in cart | No discount | ✅ Handled |
| 3 | Multiple buy products in BxGy | Calculates combined buy sets | ✅ Handled |
| 4 | Get product fewer than required | Partial discount only for available quantity | ✅ Handled |
| 5 | Get product priced differently | Higher-priced items prioritized | ✅ Handled |
| 6 | Coupon inactive | Ignored/rejected | ✅ Handled |
| 7 | Coupon expired | Ignored/rejected | ✅ Handled |
| 8 | Repetition limit exceeded | Respects cap | ✅ Handled |
| 9 | Invalid coupon type | Safely ignored | ✅ Handled |
| 10 | Empty cart | Returns validation error | ✅ Handled |
| 11 | Multiple coupons applicable | Only one evaluated | ⚠️ Not combined |
| 12 | Mixed buy/get categories | Works if IDs match | ✅ Handled |
| 13 | Compound offers | Complex logic (Buy X, get Y% off Z) | ⚠️ Not implemented |
| 14 | Duplicate product IDs | Quantities aggregated | ✅ Handled |
| 15 | Free items > stock | Capped to available | ✅ Handled |
| 16 | Discount > total | Prevented automatically | ✅ Handled |
| 17 | Expired + active mix | Expired ignored | ✅ Handled |

---

## 🧠 Assumptions

| Area | Assumption |
|------|-------------|
| Currency | INR, two-decimal precision |
| Cart Structure | Each item has `product_id`, `quantity`, `price` |
| Coupon Validity | Active **and** not expired |
| Products | No global catalog; data from cart |
| Single Coupon | One coupon per request |
| Discounts | Rounded to 2 decimals |
| DB | SQLite for simplicity |
| Ownership | Coupons are system-level |
| Quantities | Integers only |
| Tax/Shipping | Excluded from discount logic |

---

## ⚠️ Limitations

| Area | Limitation |
|------|-------------|
| Stackable Coupons | Only one per checkout |
| User Context | No authentication |
| Analytics | No usage tracking |
| Inventory | No stock validation |
| Category/Brand | No metadata support |
| Performance | Optimized for small data; no caching |
| Order Rollback | Stateless discount calc |
| Priority System | Not yet implemented |
| Auto-Add Free Items | Not added to cart (discount only) |
| Currency | Single currency (INR) |

---

## 🧮 Example Coupon Configurations

### Cart-Wise
```json
{
  "type": "cart-wise",
  "details": { "threshold": 500, "discount": 10 }
}
```

### Product-Wise
```json
{
  "type": "product-wise",
  "details": { "product_id": 5, "discount": 20 }
}
```

### BxGy (Buy 3 of P1 → Get 1 of P3 free)
```json
{
  "type": "bxgy",
  "details": {
    "buy_products": [{ "product_id": 1, "quantity": 3 }],
    "get_products": [{ "product_id": 3, "quantity": 1 }],
    "repetition_limit": 1
  }
}
```

---

## 🧠 Future Enhancements

- Priority rules (`highest_price`, `lowest_price`, `sequential`)
- Auto-add missing free items
- Tiered/Slab discounts
- Stackable coupon logic
- User-based redemption limits
- Category and brand-specific filters
- Usage analytics and dashboards
- Caching for performance

---

## 🧰 Tech Stack

- FastAPI — Web Framework  
- SQLAlchemy ORM — Database Layer  
- SQLite — Storage  
- Pydantic v2 — Validation  

---

## ✅ Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
