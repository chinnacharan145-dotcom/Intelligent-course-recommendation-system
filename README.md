# IntelliCourse AI — Personal Academic Operating System for Engineering Students

## Overview
**IntelliCourse AI** is a production-quality, full-stack academic intelligence and career guidance platform built for engineering students. It moves beyond standard Learning Management Systems (LMS) by continuously answering the student's central question: **"What should I do next?"**

The platform calculates skill proficiencies, evaluates career readiness against target career profiles, identifies missing skills, maps prerequisites, ranks recommendations using a 7-factor model, and presents an actionable **Next Best Action**.

---

## Technology Architecture

### Backend
* **Language/Framework**: Python 3.12+ / Django 5.1 / Django REST Framework
* **Authentication**: JWT (`djangorestframework-simplejwt`)
* **Database**: PostgreSQL (configured with SQLite local fallback)
* **Async Workers & Broker**: Celery + Redis
* **API Documentation**: OpenAPI 3 / Swagger (`drf-spectacular`)

### Frontend
* **Core**: Modern HTML5, CSS3, Vanilla ES6 JavaScript (Single Page Application SPA Architecture)
* **Visual Theme**: "Academic Intelligence / Future Campus"
* **Data Visualizations**: Chart.js (Skill Radar & Readiness Trends), Lucide Icons, GSAP

---

## Specification Documents
Detailed architectural specs and engineering plans are documented in the specification artifacts:
* `MASTER_REQUIREMENTS.md`
* `SYSTEM_ARCHITECTURE.md`
* `DATABASE_SPECIFICATION.md`
* `API_SPECIFICATION.md`
* `INTELLIGENCE_ENGINE_SPECIFICATION.md` / `AI_RECOMMENDATION_LOGIC_SPECIFICATION.md`
* `FRONTEND_IMPLEMENTATION_SPECIFICATION.md`
* `TESTING_SPECIFICATION.md`
* `DEPLOYMENT_SPECIFICATION.md`
* `OPEN_DECISIONS.md`
* `PROJECT_DEVELOPMENT_ROADMAP.md`

---

## Quick Start (Development Setup)

### 1. Environment Setup
```bash
# Copy environment variables template
cp .env.example .env

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run Database Migrations & System Checks
```bash
python manage.py check
python manage.py migrate
```

### 3. Run Development Server
```bash
python manage.py runserver
```

* Application Frontend: `http://127.0.0.1:8000/`
* Swagger UI Docs: `http://127.0.0.1:8000/api/docs/`
* OpenAPI Schema: `http://127.0.0.1:8000/api/schema/`
* Admin Portal: `http://127.0.0.1:8000/admin/`

---

## Development Roadmap Status
- [x] **Phase 1**: Project Foundation (Django setup, DRF, JWT, OpenAPI Swagger, Celery & Redis config)
- [ ] **Phase 2**: Database Architecture & Django Domain Apps
- [ ] **Phase 3**: Authentication & Role-Based Authorization
- [ ] **Phase 4**: Academic Master Data & Student Profile
- [ ] **Phase 5**: Skill Intelligence Engine
- [ ] **Phase 6**: Career Intelligence & Readiness Engine
- [ ] **Phase 7**: Course Catalog & Skill Mapping
- [ ] **Phase 8**: 7-Factor Recommendation Engine & Explainability
- [ ] **Phase 9**: Next Best Action Engine
- [ ] **Phase 10**: Personalized Career Roadmap Engine
- [ ] **Phase 11**: Assessment Engine & Skill Update Cascade
- [ ] **Phase 12**: Learning Progress & Activity Tracking
- [ ] **Phase 13**: Signature Dashboard Aggregation API
- [ ] **Phase 14**: Grounded AI Advisor
- [ ] **Phase 15**: Notifications & Analytics Engine
- [ ] **Phase 16**: Vanilla JS SPA Frontend Integration
- [ ] **Phase 17**: Comprehensive Automated Testing Suite
- [ ] **Phase 18**: Security Hardening
- [ ] **Phase 19**: Production Docker Deployment
