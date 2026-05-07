# Requirements Document

## Introduction

Session 12 of the Car Wash Management System (v6.7.0) implements three frontend integration features: connecting the shop page to real flash sale data from the backend, connecting the cart voucher input to the backend coupon validation system, and applying the dynamic sidebar theme color to specific UI elements on the Invoices and Order Management pages.

## Glossary

- **Shop_Page**: The client-facing product browsing page (`shop.html`) that displays products, services, and promotional content
- **Cart_Page**: The client-facing shopping cart page (`cart.html`) where users review items and apply vouchers before checkout
- **Flash_Sale_Banner**: The promotional banner component in `shop.html` that displays active flash sale countdown and information
- **Coupon_Validator**: The frontend logic that communicates with `POST /api/coupons/validate` to verify promo codes
- **Flash_Sales_API**: The backend endpoint `GET /api/flash-sales` that returns active flash sales for the current business
- **Coupons_Validate_API**: The backend endpoint `POST /api/coupons/validate` that validates a coupon code and returns discount details
- **Theme_System**: The dynamic color theming system that stores sidebar_color in the active theme and applies it via CSS custom properties (`--sidebar-color`)
- **Order_Management_Page**: The admin page (`order-management.html`) displaying order cards with stat widgets
- **Invoices_Page**: The admin page (`invoices.html`) for managing and creating invoices
- **Sidebar_Color**: The CSS custom property `--sidebar-color` loaded from the active theme via `/api/settings/theme/active`
- **Product_Card**: A product display card in the shop grid showing name, price, image, and add-to-cart button
- **Discount_Amount**: The calculated monetary value to subtract from the cart total based on coupon type (percentage or fixed)

## Requirements

### Requirement 1: Fetch Active Flash Sales on Shop Page

**User Story:** As a client, I want to see real flash sale promotions on the shop page, so that I can take advantage of time-limited discounts.

#### Acceptance Criteria

1. WHEN the Shop_Page loads, THE Shop_Page SHALL fetch active flash sales from the Flash_Sales_API using the client's authentication token
2. IF the Flash_Sales_API returns an error or no active sales, THEN THE Flash_Sale_Banner SHALL be hidden from view
3. WHEN at least one active flash sale is returned, THE Flash_Sale_Banner SHALL display the title of the first active flash sale
4. WHEN an active flash sale is displayed, THE Flash_Sale_Banner SHALL show a live countdown timer calculated from the flash sale's `ends_at` timestamp
5. WHEN the countdown timer reaches zero, THE Shop_Page SHALL re-fetch flash sales from the Flash_Sales_API and update the display accordingly

### Requirement 2: Display Discounted Prices on Flash Sale Products

**User Story:** As a client, I want to see which products are on flash sale with their discounted prices, so that I can identify deals at a glance.

#### Acceptance Criteria

1. WHEN an active flash sale includes specific product IDs, THE Shop_Page SHALL display a sale badge on each affected Product_Card
2. WHEN a product is part of an active flash sale with discount_type "percentage", THE Product_Card SHALL display the discounted price calculated as `original_price * (1 - discount_value / 100)`
3. WHEN a product is part of an active flash sale with discount_type "fixed", THE Product_Card SHALL display the discounted price calculated as `original_price - discount_value` (minimum ₱0)
4. WHEN a product has a flash sale discount applied, THE Product_Card SHALL display the original price with a strikethrough style alongside the new discounted price
5. WHEN an active flash sale has an empty product_ids array, THE Shop_Page SHALL apply the flash sale discount to all products displayed in the grid

### Requirement 3: Validate Coupon Codes Against Backend

**User Story:** As a client, I want to apply a coupon code in my cart and have it validated by the system, so that I receive the correct discount on my order.

#### Acceptance Criteria

1. WHEN the user enters a coupon code and clicks "Apply", THE Coupon_Validator SHALL send a POST request to the Coupons_Validate_API with the code and current cart subtotal
2. WHEN the Coupons_Validate_API returns a successful response with `valid: true`, THE Cart_Page SHALL display the discount amount in the order summary
3. WHEN the Coupons_Validate_API returns a successful response, THE Cart_Page SHALL subtract the Discount_Amount from the total displayed in the order summary
4. IF the Coupons_Validate_API returns a 400 or 404 error, THEN THE Cart_Page SHALL display the error message from the API response (e.g., "Invalid or expired coupon code", "This coupon has expired", "Minimum spend of ₱X required")
5. WHEN a valid coupon is applied, THE Cart_Page SHALL display the coupon code with a remove/clear button to allow the user to unapply it
6. WHEN the user removes an applied coupon, THE Cart_Page SHALL reset the discount to zero and recalculate the order total

### Requirement 4: Remove Hardcoded Test Coupon Logic

**User Story:** As a developer, I want the cart page to use only the backend coupon validation, so that the system behaves consistently with admin-created coupons.

#### Acceptance Criteria

1. THE Cart_Page SHALL remove all hardcoded test coupon codes (SAVE10, CARWASH50, PROMO20) from the frontend JavaScript
2. THE Cart_Page SHALL rely exclusively on the Coupons_Validate_API for all coupon validation logic
3. WHEN no authentication token is available, THE Coupon_Validator SHALL display an error message prompting the user to log in

### Requirement 5: Apply Sidebar Color to Invoices Page Buttons

**User Story:** As an admin, I want the Invoices page buttons to match my business theme color, so that the UI looks consistent across all pages.

#### Acceptance Criteria

1. WHEN the Invoices_Page loads, THE Invoices_Page SHALL read the Sidebar_Color from the active theme CSS custom property
2. THE Invoices_Page SHALL apply the Sidebar_Color as the background color of the "Create Invoice" button
3. THE Invoices_Page SHALL apply the Sidebar_Color as the background color of all "PDF" download buttons in the invoice table
4. WHEN the active theme changes, THE Invoices_Page SHALL reflect the updated Sidebar_Color on the affected buttons without requiring a page reload

### Requirement 6: Apply Sidebar Color to Order Management Stat Widgets

**User Story:** As an admin, I want the Order Management page stat cards to match my business theme color, so that the dashboard feels cohesive with the sidebar.

#### Acceptance Criteria

1. WHEN the Order_Management_Page loads, THE Order_Management_Page SHALL read the Sidebar_Color from the active theme CSS custom property
2. THE Order_Management_Page SHALL apply the Sidebar_Color as the background color of the order card header gradient (replacing the hardcoded `#667eea` to `#764ba2` gradient)
3. THE Order_Management_Page SHALL ensure white text remains readable against the Sidebar_Color background
4. WHEN the active theme changes, THE Order_Management_Page SHALL reflect the updated Sidebar_Color on the card headers without requiring a page reload
