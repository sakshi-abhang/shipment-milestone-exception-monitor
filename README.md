Shipment Milestone & Exception Monitor
An intermediate shipping and logistics project built to track shipment milestones, detect ETA delays, manage operational exceptions, and provide shipment visibility through a dashboard.

Features
Create, view, update, and delete shipments
Track shipment milestone events
View shipment timelines
Compare planned arrival with predicted arrival
Automatically detect ETA delays
Classify exceptions as MEDIUM, HIGH, or CRITICAL
Resolve shipment exceptions
Filter shipments by status, origin, and destination
View shipment information in a Streamlit dashboard
Test APIs using Bruno
Automated testing using Pytest
Continuous Integration using GitHub Actions
Technology Stack
Python
FastAPI
SQLite
SQLAlchemy
Pydantic
Streamlit
Bruno
Pytest
Git
GitHub
GitHub Actions
Project Flow
Shipment Created
      ↓
Milestones Recorded
      ↓
ETA Monitored
      ↓
Delay Detected
      ↓
Exception Generated
      ↓
Dashboard Shows Alert
Shipment Milestones
Example shipment journey:

BOOKING_CONFIRMED
        ↓
CONTAINER_PICKED_UP
        ↓
GATE_IN
        ↓
LOADED_ON_VESSEL
        ↓
VESSEL_DEPARTED
        ↓
VESSEL_ARRIVED
        ↓
DISCHARGED
        ↓
GATE_OUT
        ↓
DELIVERED
ETA Exception Logic
ETA Delay	Result
Less than 24 hours	No exception
24 to less than 48 hours	MEDIUM
48 to 72 hours	HIGH
More than 72 hours	CRITICAL
Example:

Planned Arrival:   20 Nov 2026
Predicted Arrival: 22 Nov 2026

Delay: 48 hours
Result: HIGH ETA_DELAY
API Endpoints
Shipments
POST   /shipments
GET    /shipments
GET    /shipments/{shipment_id}
PUT    /shipments/{shipment_id}
DELETE /shipments/{shipment_id}
Shipment Events
POST /shipments/{shipment_id}/events
GET  /shipments/{shipment_id}/events
Exceptions
GET   /shipments/{shipment_id}/delay-status
POST  /shipments/{shipment_id}/exceptions/detect
GET   /exceptions
GET   /shipments/{shipment_id}/exceptions
PATCH /exceptions/{exception_id}/resolve
Dashboard
The Streamlit dashboard provides:

Total shipment count
Open exception count
High/Critical exception count
Shipment filters
Shipment details
Milestone timeline
Operational exception information
Shipment Monitor Dashboard

Run the Project
Create the virtual environment:

python -m venv venv
Activate it on Windows:

venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Start FastAPI:

uvicorn app.main:app --reload
FastAPI documentation:

http://127.0.0.1:8000/docs
Start Streamlit:

python -m streamlit run app/dashboard/streamlit_app.py
Dashboard:

http://localhost:8501
Automated Testing
Run:

python -m pytest -v
The project contains automated tests for API endpoints and ETA exception logic.

Current test suite:

10 tests passed
Continuous Integration
GitHub Actions automatically:

Code Push
   ↓
GitHub Actions
   ↓
Set Up Python
   ↓
Install Dependencies
   ↓
Run Pytest
   ↓
PASS / FAIL
Data Privacy
All shipment IDs, booking numbers, container numbers, locations, milestones, and operational information used in this project are synthetic and created only for demonstration and learning.

No confidential company, customer, or production shipment data is included.

Future Improvements
Missing milestone detection
Vessel arrival delay detection
Reefer temperature alerts
Email or Teams notifications
Authentication and authorization
PostgreSQL database support
Docker deployment
Advanced analytics and dashboards