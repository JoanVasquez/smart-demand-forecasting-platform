# Smart Forecast

A microservices-based sales forecasting system that processes sales data and generates ML-powered forecasts using event-driven architecture.

## Architecture

- **Sale Service** (Java/Spring Boot) - Manages sales data and publishes events
- **ML Forecast Service** (Python/FastAPI) - Consumes sales events and generates forecasts using Prophet
- **Event Streaming** - Kafka with Avro schema registry
- **Databases** - PostgreSQL for both services
- **Task Queue** - Celery with Redis for async ML processing

## Services

| Service | Port | Technology |
|---------|------|------------|
| Sale API | 8000 | Spring Boot |
| ML Forecast API | 8080 | FastAPI |
| Kafka | 9092 | Confluent |
| Schema Registry | 8081 | Confluent |
| PostgreSQL (Sales) | 5432 | PostgreSQL 16 |
| PostgreSQL (Forecast) | 5433 | PostgreSQL 16 |
| Redis | 6379 | Redis |
| Flower (Celery UI) | 5555 | Celery |

## Quick Start

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```

2. Start all services:
   ```bash
   docker-compose up -d
   ```

3. Check service health:
   ```bash
   docker-compose ps
   ```

## Development

### Prerequisites
- Docker & Docker Compose
- Java 17+ (for local development)
- Python 3.8+ (for local development)

### Environment Setup
Configure `.env` file with your database credentials and Kafka settings.

### Local Development
Each service can be run independently for development. See individual service directories for specific setup instructions.

## API Examples

### Create Sales Data
```bash
POST http://localhost:8000/api/v1/sale
Content-Type: application/json

{
  "productId": "test123",
  "quantity": 9,
  "saleDate": "2025-07-05T11:00:00"
}
```

### Get Forecasts
```bash
GET http://localhost:8080/api/v1/forecast
```

Response:
```json
[
  {
    "ds": "2025-07-02T14:20:00",
    "trend": 3.920598,
    "yhat_lower": 7.999879365992028,
    "yhat_upper": 7.999879367271052,
    "yhat": 7.999879366596635
  }
]
```