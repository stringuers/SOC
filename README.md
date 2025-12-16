# SecureWatch - AI-Powered SOC Automation Platform

An intelligent security monitoring and incident response platform that automatically detects, analyzes, and responds to cybersecurity threats in real-time.

## 🚀 Features

- **Real-time Log Ingestion**: Aggregate logs from multiple sources
- **ML-based Anomaly Detection**: Automatic threat identification using machine learning
- **Threat Intelligence Integration**: Enrich alerts with external threat data
- **Automated Incident Response**: Execute playbooks for common threat types
- **Interactive Dashboard**: Comprehensive security visibility and management
- **Alert Management**: Track, assign, and resolve security alerts
- **Live Log Stream**: Real-time monitoring of security events

## 🏗️ Architecture

```
Data Sources → Log Collector → Processing Pipeline → ML Engine → Alert System → Dashboard
                                       ↓
                                  Data Storage (PostgreSQL + Elasticsearch)
```

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

## 🛠️ Installation

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clonehttps://github.com/stringuers/SOC.git
   cd SOC
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
  
   ```

3. **Train the ML model** (optional, but recommended)
   ```bash
   cd ml-engine
   python train_model.py
   cd ..
   ```

4. **Start all services**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Elasticsearch: http://localhost:9200

### Manual Setup

#### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   ```bash
   # Make sure PostgreSQL is running
   # Update DATABASE_URL in .env
   python -c "from database import init_db; init_db()"
   ```

4. **Train ML model**
   ```bash
   cd ../ml-engine
   python train_model.py
   cd ../backend
   ```

5. **Start backend**
   ```bash
   uvicorn main:app --reload
   ```

6. **Start Celery worker** (in separate terminal)
   ```bash
   celery -A celery_app worker --loglevel=info
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

## 📊 Services

### Backend Services

- **FastAPI**: REST API server (port 8000)
- **Celery**: Background task processing
- **PostgreSQL**: Structured data storage
- **Redis**: Task queue and caching
- **Elasticsearch**: Log search and indexing

### Frontend

- **React + TypeScript**: Modern UI framework
- **Tailwind CSS**: Styling
- **React Query**: Data fetching and caching
- **Recharts**: Data visualization

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://admin:securepass@localhost:5432/securewatch

# Redis
REDIS_URL=redis://localhost:6379/0

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200

# Threat Intelligence (Optional)
ABUSE_IPDB_KEY=your_key_here
VIRUSTOTAL_KEY=your_key_here
```

## 📡 API Endpoints

### Logs
- `POST /api/logs/ingest` - Ingest a new log entry
- `GET /api/logs` - Get logs with filtering
- `GET /api/logs/{id}` - Get specific log

### Alerts
- `GET /api/alerts` - Get alerts with filtering
- `GET /api/alerts/{id}` - Get specific alert
- `PATCH /api/alerts/{id}` - Update alert
- `PATCH /api/alerts/{id}/resolve` - Resolve alert
- `GET /api/alerts/stats/summary` - Get alert statistics

### Incidents
- `GET /api/incidents` - Get incidents
- `POST /api/incidents` - Create incident

### WebSocket
- `WS /ws` - Real-time updates

## 🧪 Testing

### Generate Test Logs

Use the log simulator to generate test data:

```bash
cd scripts
python log_simulator.py
```

This will send logs to the API at regular intervals, including both normal and suspicious traffic.

## 🔐 Security Features

- **Anomaly Detection**: ML-based detection of suspicious patterns
- **Threat Intelligence**: IP reputation checking
- **Automated Response**: Playbooks for common threats
- **Real-time Monitoring**: Live log streaming and alerting

## 📈 ML Model

The platform uses an Isolation Forest model for anomaly detection. Features include:
- Time-based patterns (hour, day of week)
- IP address analysis
- Log content analysis (SQL injection, XSS, etc.)
- Failed login detection

Train the model:
```bash
cd ml-engine
python train_model.py
```

## 🚨 Incident Response Playbooks

Automated playbooks are available for:
- SQL Injection
- Brute Force Attacks
- Data Exfiltration
- Port Scanning

Playbooks can:
- Block IP addresses
- Rate limit connections
- Alert administrators
- Create incidents
- Capture network traffic

## 📝 Development

### Project Structure

```
SOC/
├── backend/           # FastAPI backend
│   ├── routers/       # API routes
│   ├── services/     # Business logic
│   ├── tasks/        # Celery tasks
│   └── models.py     # Database models
├── frontend/         # React frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       └── lib/
├── ml-engine/        # ML model training
├── scripts/          # Utility scripts
└── docker-compose.yml
```

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

### Redis Connection Issues
- Ensure Redis is running
- Check REDIS_URL in .env

### Elasticsearch Issues
- Ensure Elasticsearch is running
- Check ELASTICSEARCH_URL in .env
- The system will continue without Elasticsearch (degraded search functionality)

### ML Model Not Found
- Train the model: `cd ml-engine && python train_model.py`
- The system will use rule-based detection as fallback

## 📚 Documentation

- API Documentation: http://localhost:8000/docs (Swagger UI)
- API ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License

## 🎯 Roadmap

- [ ] JWT Authentication
- [ ] Role-Based Access Control (RBAC)
- [ ] Advanced ML models
- [ ] Integration with SIEM systems
- [ ] Mobile app
- [ ] Advanced reporting
- [ ] Multi-tenant support

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ for security operations teams
