# Vendors_management
Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

# Setup Instructions

# Prerequisites
* Python 3.x installed
* Django and Django REST Framework installed

# Installation Steps
1.Clone the repository:
  git clone https://github.com/your-username/vendor-management-system.git
2.Navigate to the project directory:
  cd vendor-management-system
3.Install project dependencies:
  pip install -r requirements.txt
4.Apply database migrations:
  python manage.py makemigrations
  python manage.py migrate
5.Start the development server:
  python manage.py runserver

# API Endpoints

* POST /api/vendors/
  Create a new vendor.
  Request Body: JSON containing vendor details.
  Example: curl -X POST -H "Content-Type: application/json" -d '{"name": "VendorName", "email": "vendor@email.com"}' http://127.0.0.1:8000/api/vendors/
  
* GET /api/vendors/
  List all vendors.

* GET /api/vendors/{vendor_id}/
  Retrieve a specific vendor's details.
  Replace {vendor_id} with the ID of the vendor.
  Example:curl -X GET http://127.0.0.1:8000/api/vendors/1/

* PUT /api/vendors/{vendor_id}/
  Update a vendor's details.
  Replace {vendor_id} with the ID of the vendor.
  Request Body: JSON containing updated vendor details.
  Example:curl -X PUT -H "Content-Type: application/json" -d '{"name": "UpdatedName", "email": "updated@email.com"}' http://127.0.0.1:8000/api/vendors/1/

* DELETE /api/vendors/{vendor_id}/
  Delete a vendor.
  Replace {vendor_id} with the ID of the vendor.
  Example:curl -X DELETE http://127.0.0.1:8000/api/vendors/1/

# Purchase Order Tracking

Model Design
Track purchase orders with fields like PO number, vendor reference, order date, items, quantity, and status.

## API Endpoints

* POST /api/purchase_orders/
Create a purchase order.
Request Body: JSON containing purchase order details.

* GET /api/purchase_orders/
List all purchase orders with an option to filter by vendor.

* GET /api/purchase_orders/{po_id}/
Retrieve details of a specific purchase order.
Replace {po_id} with the ID of the purchase order.

* PUT /api/purchase_orders/{po_id}/
Update a purchase order.
Replace {po_id} with the ID of the purchase order.
Request Body: JSON containing updated purchase order details.

* DELETE /api/purchase_orders/{po_id}/
Delete a purchase order.
Replace {po_id} with the ID of the purchase order.

# Vendor Performance Evaluation
## Backend Logic for Performance Metrics

* On-Time Delivery Rate:
Calculated each time a PO status changes to 'completed'.
Logic: Count the number of completed POs delivered on or before delivery_date and divide by the total number of completed POs for that vendor.

* Quality Rating Average:
Updated upon the completion of each PO where a quality_rating is provided.
Logic: Calculate the average of all quality_rating values for completed POs of the vendor.

* Average Response Time:
Calculated each time a PO is acknowledged by the vendor.
Logic: Compute the time difference between issue_date and acknowledgment_date for each PO, then find the average of these times for all POs of the vendor.

* Fulfilment Rate:
Calculated upon any change in PO status.
Logic: Divide the number of successfully fulfilled POs (status 'completed' without issues) by the total number of POs issued to the vendor.

## API Endpoint Implementation

* Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance):
Retrieves the calculated performance metrics for a specific vendor.
Returns data including on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate.

* Update Acknowledgment Endpoint (POST /api/purchase_orders/{po_id}/acknowledge):
Endpoint for vendors to acknowledge POs.
Updates acknowledgment_date and triggers the recalculation of average_response_time.

Note: Replace http://127.0.0.1:8000 with the appropriate URL if deploying the application to a different environment.

