# Quick Start Guide

Get SecureWatch up and running in minutes!

## Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for frontend)
- Python 3.11+ (for ML model training and scripts)

## Option 1: Docker (Recommended)

### Step 1: Clone and Setup

```bash
cd SOC
cp .env.example .env
# Edit .env if needed
```

### Step 2: Train ML Model

```bash
cd ml-engine
python train_model.py
cd ..
```

### Step 3: Start Services

```bash
docker-compose up -d
```

Wait a few seconds for services to start, then:

### Step 4: Install Frontend Dependencies

```bash
npm install
```

### Step 5: Start Frontend

```bash
npm run dev
```

### Step 6: Access the Application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Step 7: Generate Test Data (Optional)

In a new terminal:

```bash
python scripts/log_simulator.py
```

## Option 2: Manual Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database (PostgreSQL must be running)
export DATABASE_URL="postgresql://admin:securepass@localhost:5432/securewatch"
python -c "from database import init_db; init_db()"

# Train ML model
cd ../ml-engine
python train_model.py
cd ../backend

# Start backend
uvicorn main:app --reload
```

In another terminal:

```bash
cd backend
source venv/bin/activate
celery -A celery_app worker --loglevel=info
```

### Frontend

```bash
npm install
npm run dev
```

## Verify Installation

1. Check backend health: http://localhost:8000/health
2. Check API docs: http://localhost:8000/docs
3. Open frontend: http://localhost:8080

## Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### Database connection errors

- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

### ML model not found

The system will use rule-based detection as fallback. To use ML:

```bash
cd ml-engine
python train_model.py
```

### Frontend can't connect to backend

- Check CORS settings in `backend/main.py`
- Verify backend is running on port 8000
- Check browser console for errors

## Next Steps

1. **Generate test data**: Run `python scripts/log_simulator.py`
2. **Explore the API**: Visit http://localhost:8000/docs
3. **Monitor alerts**: Watch the dashboard for real-time alerts
4. **Review logs**: Check the log stream for incoming events

## Stopping Services

```bash
# Docker
docker-compose down

# Manual
# Stop backend (Ctrl+C)
# Stop Celery (Ctrl+C)
# Stop frontend (Ctrl+C)
```

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review API docs at http://localhost:8000/docs
- Check service logs: `docker-compose logs [service-name]`

