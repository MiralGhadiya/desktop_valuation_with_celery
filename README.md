# Desktop Valuation Platform

**Desktop Valuation** is a comprehensive FastAPI-based platform that provides automated property valuation services with subscription management, payment processing, and administrative capabilities. The platform serves users across multiple countries with localized pricing, currency conversion, and property-specific valuations using AI/LLM integration.

## Key Features
- **User Authentication**: Email-based registration with verification and password management.
- **Property Valuations**: AI-powered property valuation generation with detailed PDF reports.
- **Subscription Management**: Multi-tier subscription plans with country-specific pricing.
- **Payment Processing**: Razorpay integration for secure payment handling.
- **Admin Dashboard**: Comprehensive admin panel for user, staff, subscription, inquiry, feedback, and valuation management.
- **Async Processing**: Celery-based background task processing for valuations and notifications.
- **Multi-Country Support**: Automatic IP-based country detection, localized pricing, and currency conversion.
- **Public Inquiries & Feedback**: Direct channels for users and visitors to communicate with administrators.

## Technology Stack
- **Backend**: FastAPI
- **Database**: PostgreSQL & SQLAlchemy (with Alembic for migrations)
- **Async Processing**: Celery & Redis
- **AI/LLM**: OpenAI
- **Payments**: Razorpay
- **PDF Generation**: Custom report builder

## Setup and Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- SMTP Server details
- API Keys: Razorpay, OpenAI

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository>
   cd desktop_valuation-miral
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory and add the following:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your-secret-key
   RAZORPAY_KEY_ID=your-key
   RAZORPAY_KEY_SECRET=your-secret
   OPENAI_API_KEY=your-key
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_EMAIL=your-email
   SMTP_PASSWORD=your-password
   ```

5. **Run Database Migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Initialize the Database:**
   ```bash
   python app/scripts/create_superuser.py
   python app/scripts/add_country.py
   ```

## Running the Application

Open separate terminals to run the various components of the architecture:

1. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start the Celery worker (for background tasks like valuations and emails):**
   ```bash
   celery -A app.celery_app worker -l info
   ```

3. **Start the Celery Beat scheduler (for subscriptions expiry and daily exchange rates):**
   ```bash
   celery -A app.celery_app beat -l info
   ```

## Documentation
- Detailed API Specs: see `API_DOCUMENTATION.md`
- Architecture & Models: see `PROJECT_ARCHITECTURE.md`
- Application Workflows: see `FLOW_DOCUMENTATION.md` and `PROJECT_FLOW_DOCUMENTATION.md`

