# Degaan Real Estate - Backend

Django REST Framework backend for Degaan Real Estate platform.

## Features

- Property management API
- Lead capture and CRM
- Project management
- Admin dashboard
- Email notifications
- PostgreSQL database
- RESTful API endpoints

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Create `.env` file:

```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
SENDGRID_API_KEY=your-sendgrid-key
FRONTEND_URL=https://degaanrealestate.com
```

## Running Locally

```bash
python manage.py migrate
python manage.py runserver
```

Visit http://localhost:8000/api/

## Admin Dashboard

```bash
python manage.py createsuperuser
```

Access at http://localhost:8000/admin/

## API Endpoints

### Properties
- `GET /api/properties/` - List properties
- `GET /api/properties/{id}/` - Get property detail
- `GET /api/properties/featured/` - Get featured properties
- `GET /api/properties/{id}/similar/` - Get similar properties
- `POST /api/properties/` - Create property (admin only)

### Leads
- `GET /api/leads/` - List leads
- `POST /api/leads/` - Submit lead form (public)
- `GET /api/leads/stats/` - Get lead statistics
- `POST /api/leads/bulk_status_update/` - Bulk update lead status

### Projects
- `GET /api/projects/` - List projects
- `GET /api/projects/{id}/` - Get project detail
- `GET /api/projects/{id}/properties/` - Get project properties

## Database Models

### Property
- Address, location, price, size
- Bedrooms, bathrooms, type
- Description, features, images
- Status (available, sold, construction)

### Lead
- Name, email, phone
- Interest type, message
- Status tracking
- Source tracking

### Project
- Name, description, budget
- Timeline, units count
- Structural specs, certifications
- Progress tracking

## Deployment on Railway

```bash
git push  # Pushes to GitHub
# Railway auto-builds from requirements.txt
# Runs: gunicorn degaan.wsgi:application
```

## Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing

```bash
python manage.py test
```
