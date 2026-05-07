# Implementation Plan: Session 12 – Flash Sale, Coupons & UI Theme Integration

## Overview

This plan implements three frontend-only features: connecting shop.html to the flash sales API, enhancing cart.html coupon validation UX, and applying dynamic theme colors to invoices and order management pages. All changes consume existing backend APIs — no new endpoints needed.

## Tasks

- [x] 1. Flash Sale Integration in shop.html
  - [x] 1.1 Add `loadFlashSales()` function and state variable
    - Add `let activeFlashSale = null` state variable
    - Implement `loadFlashSales()` that fetches `GET /api/flash-sales` with auth token
    - On success with sales, store first active sale in `activeFlashSale` and call `renderFlashBanner()`
    - On error or empty array, hide the flash banner (`flashBanner.style.display = 'none'`)
    - Call `loadFlashSales()` in `init()` instead of `startCountdown(4 * 3600 + 23 * 60 + 18)`
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 1.2 Implement `startCountdownFromTimestamp(endsAt)` replacing hardcoded countdown
    - Create `startCountdownFromTimestamp(endsAt)` that calculates remaining seconds from `new Date(endsAt).getTime() - Date.now()`
    - Decompose remaining seconds into hours, minutes, seconds and update `cdHr`, `cdMin`, `cdSec` elements
    - When countdown reaches zero, call `loadFlashSales()` to re-fetch
    - Remove or replace the old `startCountdown(secs)` function
    - _Requirements: 1.4, 1.5_

  - [x] 1.3 Implement `getFlashSaleDiscount(productId)` pure function
    - Return `null` if `activeFlashSale` is null
    - If `product_ids` array is non-empty and doesn't include `productId`, return `null`
    - If `product_ids` is empty, apply discount to all products
    - For `discount_type === 'percentage'`: calculate `original * (1 - discount_value / 100)`
    - For `discount_type === 'fixed'`: calculate `Math.max(0, original - discount_value)`
    - Return `{ discountedPrice, label }` object
    - _Requirements: 2.1, 2.2, 2.3, 2.5_

  - [x] 1.4 Modify `renderGrid()` to display flash sale discounts on product cards
    - Call `getFlashSaleDiscount(item.id)` for each product in the grid
    - When a discount exists, show original price with strikethrough and new discounted price
    - Add a sale badge (e.g., "⚡ 20% OFF") on affected product cards
    - Ensure non-sale products render normally without badges
    - _Requirements: 2.1, 2.4_

  - [ ]* 1.5 Write property test for flash sale discount calculation (Property 1)
    - **Property 1: Flash sale discount calculation**
    - Use fast-check to generate arbitrary prices (positive numbers) and discount values
    - Verify percentage discount: `price * (1 - value/100)` matches `getFlashSaleDiscount` output
    - Verify fixed discount: `Math.max(0, price - value)` matches output
    - **Validates: Requirements 2.2, 2.3**

  - [ ]* 1.6 Write property test for flash sale badge targeting (Property 2)
    - **Property 2: Flash sale badge targeting**
    - Use fast-check to generate arrays of product IDs and verify only matching products get badges
    - Verify empty `product_ids` array applies to all products
    - **Validates: Requirements 2.1, 2.5**

  - [ ]* 1.7 Write property test for countdown timer calculation (Property 3)
    - **Property 3: Countdown timer calculation**
    - Use fast-check to generate future timestamps and verify h:m:s decomposition
    - Verify `floor((endsAt - now) / 1000)` correctly decomposes into hours, minutes, seconds
    - **Validates: Requirements 1.4**

- [x] 2. Checkpoint - Verify flash sale integration
  - Ensure all tests pass, ask the user if questions arise.

- [x] 3. Coupon Validation UX in cart.html
  - [x] 3.1 Refactor `applyVoucher()` to use backend-only validation with proper UX
    - Add `let appliedCoupon = null` state variable (alongside existing `let discount = 0`)
    - Add auth check: if no token, show toast "Please log in to apply a coupon" and return
    - Send `POST /api/coupons/validate` with `{ code, cart_total }` (cart subtotal)
    - On success (`valid: true`): store `appliedCoupon = { code, discount_amount }`, set `discount = data.discount_amount`
    - On 400/404 error: show toast with the `detail` message from the API response
    - On network error: show toast "Failed to validate coupon. Please try again."
    - Call `renderAppliedCoupon()` and `updateSummary()` after state changes
    - Remove any hardcoded test coupon codes (SAVE10, CARWASH50, PROMO20) if present
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3_

  - [x] 3.2 Implement `renderAppliedCoupon()` with remove button
    - When `appliedCoupon` is set: replace voucher input row with applied coupon display showing code, discount amount, and a remove (✕) button
    - When `appliedCoupon` is null: restore the original input + Apply button HTML
    - Style the applied coupon display with brand colors and green discount text
    - _Requirements: 3.5_

  - [x] 3.3 Implement `removeCoupon()` function
    - Set `appliedCoupon = null` and `discount = 0`
    - Call `renderAppliedCoupon()` to restore input field
    - Call `updateSummary()` to recalculate total
    - Show toast "Coupon removed"
    - _Requirements: 3.6_

  - [x] 3.4 Update order summary to reflect coupon discount
    - Show/hide the discount row (`#discountRow`) based on whether `discount > 0`
    - Display discount amount in `#discountAmt`
    - Subtract discount from total in `#summaryTotal` and `#mobileTotal`
    - _Requirements: 3.2, 3.3_

  - [ ]* 3.5 Write property test for coupon discount applied to order summary (Property 4)
    - **Property 4: Coupon discount applied to order summary**
    - Use fast-check to generate subtotals and discount amounts
    - Verify displayed total equals `subtotal - discount_amount`
    - **Validates: Requirements 3.2, 3.3**

  - [ ]* 3.6 Write property test for coupon removal resets total (Property 6)
    - **Property 6: Coupon removal resets total**
    - Use fast-check to generate any previously applied discount
    - Verify after removal: discount is 0 and total equals subtotal
    - **Validates: Requirements 3.6**

- [x] 4. Checkpoint - Verify coupon validation flow
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Theme Color Application
  - [x] 5.1 Apply `--sidebar-color` to Invoices page buttons
    - Add CSS rule for `.btn-primary` on invoices.html to use `background: var(--sidebar-color, #2c3e50)`
    - Update PDF button rendering in `invoices.js` to use `style="background:var(--sidebar-color, #2c3e50)"` instead of hardcoded color
    - Verify buttons update dynamically when theme changes (CSS custom properties are reactive)
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 5.2 Apply `--sidebar-color` to Order Management card headers
    - Replace the hardcoded `.card-header` gradient (`#667eea` to `#764ba2`) with `linear-gradient(135deg, var(--sidebar-color, #667eea) 0%, color-mix(in srgb, var(--sidebar-color, #667eea) 70%, #000) 100%)`
    - Ensure white text remains readable (gradient always produces dark-enough background)
    - Verify card headers update dynamically when theme changes
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [ ]* 5.3 Write property test for sidebar color applied to themed elements (Property 7)
    - **Property 7: Sidebar color applied to themed elements**
    - Use fast-check to generate valid CSS color values
    - Verify that setting `--sidebar-color` results in the correct computed background on target elements
    - **Validates: Requirements 5.2, 5.3, 6.2**

- [x] 6. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- All changes are frontend-only — no backend modifications needed
- The `menu.js` theme system already sets `--sidebar-color` on `:root`, so themed pages just reference the CSS variable
- Property tests use the [fast-check](https://github.com/dubzzz/fast-check) library for JavaScript PBT
- Checkpoints ensure incremental validation between feature areas
