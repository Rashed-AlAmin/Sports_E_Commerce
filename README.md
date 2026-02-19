# High-Performance E-Commerce API

A production-ready, asynchronous e-commerce backend built with FastAPI, PostgreSQL, and modern Python async/await patterns. Fully containerized with Docker for seamless deployment across any environment.

🚀 **Live API:** [https://sports-e-commerce.onrender.com](https://sports-e-commerce.onrender.com)  
📚 **Interactive Docs:** [https://sports-e-commerce.onrender.com/docs](https://sports-e-commerce.onrender.com/docs)

---

## 🎯 Project Overview

This is a fully functional e-commerce backend API featuring secure authentication, product management, shopping cart operations, and order processing. Built with enterprise-grade patterns and optimized for performance at scale.

**Key Highlights:**
- ⚡ Asynchronous architecture using FastAPI + SQLAlchemy 2.0
- 🔐 OAuth2 + JWT authentication with role-based access control
- 🗄️ PostgreSQL with async operations via asyncpg
- 🛡️ Comprehensive data validation using Pydantic V2
- 🐳 Fully Dockerized with Docker Compose for one-command deployment
- 📦 Redis integration for caching and session management
- 🚀 Deployed and tested in production environment
- 📊 Optimized queries with eager loading to prevent N+1 problems

---

## 🏗️ Technical Architecture

### Core Stack
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL (Neon)
- **ORM:** SQLAlchemy 2.0 (Async)
- **Caching:** Redis (Alpine)
- **Security:** JWT tokens, bcrypt password hashing
- **Validation:** Pydantic V2 schemas
- **Containerization:** Docker + Docker Compose
- **Deployment:** Render (with auto-scaling capabilities)

### Design Patterns
- **Layered Architecture:** Separation of routes, services, and data models
- **Async/Await:** Non-blocking I/O for concurrent request handling
- **Data Integrity:** Atomic transactions for cart-to-order conversion
- **Security Best Practices:** Password hashing, token expiration, admin authorization
- **Container Orchestration:** Multi-service Docker setup with volume persistence

---

## 📡 API Endpoints

### Authentication
- `POST /signup` - User registration
- `POST /login` - User authentication (returns JWT)
- `GET /me` - Get current user profile
- `GET /admin-only` - Admin-protected route example

### Product Management
- `GET /products/` - List all products (paginated)
- `POST /products/` - Create product (admin only)
- `GET /products/{product_id}` - Get single product
- `PUT /products/{product_id}` - Update product (admin only)
- `DELETE /products/{product_id}` - Delete product (admin only)

### Shopping Cart
- `POST /cart/add/{product_id}` - Add item to cart
- `GET /cart/` - View current cart with items

### Order Processing
- `POST /orders/checkout` - Convert cart to order
- `GET /orders/my` - View order history
- `GET /orders/{order_id}` - Get specific order details

**Try it live:** Visit the [Swagger UI](https://sports-e-commerce.onrender.com/docs) for interactive API testing

---

## 🔧 Key Technical Implementations

### 1. Asynchronous Database Operations
Utilizes SQLAlchemy 2.0's async engine with asyncpg driver for non-blocking database calls, enabling high concurrency.

### 2. Eager Loading Strategy
Implements `selectinload()` to fetch related data efficiently, avoiding the N+1 query problem common in ORMs.

### 3. Secure Authentication Flow
- Passwords hashed with bcrypt (cost factor: 12)
- JWT tokens with configurable expiration
- Role-based access control (user/admin)
- Token-based session management

### 4. Atomic Order Processing
Checkout operation uses database transactions to ensure:
- Cart items are atomically converted to order items
- Product prices are snapshotted at purchase time
- Cart is cleared only after successful order creation

### 5. Redis Caching Layer
- Product catalog caching for reduced database load
- Session management for improved performance
- Ready for rate limiting and background task queues

### 6. Containerized Deployment
- Docker multi-stage builds for optimized image size
- Docker Compose orchestration for local development
- Environment-based configuration for dev/staging/prod
- Volume mounting for hot-reloading during development

### 7. Data Validation & Security
- Pydantic schemas validate all incoming requests
- Response models prevent sensitive data leakage
- SQL injection protection via ORM parameterization

---

## 🐳 Docker Setup

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Quick Start with Docker

**Option 1: Using Docker Compose (Recommended)**
```bash
# Clone the repository
git clone https://github.com/Rashed-AlAmin/Sports_E_Commerce.git
cd Sports_E_Commerce

# Create .env file from example
cp .env.example .env
# Edit .env with your database credentials

# Build and run all services
docker-compose up --build

# API will be available at http://localhost:8000
# Redis at localhost:6379
```

**Option 2: Using Docker directly**
```bash
# Build the image
docker build -t sports-ecommerce-api .

# Run the container
docker run -p 8000:8000 --env-file .env sports-ecommerce-api
```

### Docker Services

The `docker-compose.yml` defines two services:

1. **web** (FastAPI application)
   - Port: 8000
   - Hot-reload enabled with volume mounting
   - Depends on Redis service

2. **redis** (Cache layer)
   - Port: 6379
   - Alpine-based for minimal footprint

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## 🚀 Performance Optimizations

### Completed
✅ Async/await architecture for concurrent handling  
✅ Database connection pooling  
✅ Efficient eager loading for related data  
✅ Indexed foreign keys and primary keys  
✅ Redis caching layer integrated  
✅ Docker containerization for consistent environments  

### Next Steps
- [ ] **Database Indexing** - Add composite indexes on frequently queried columns
- [ ] **Query Optimization** - Implement cursor-based pagination
- [ ] **Background Tasks** - Celery integration for email notifications
- [ ] **Rate Limiting** - Redis-backed API rate limiter
- [ ] **Monitoring & Logging** - Structured logging with APM tools
- [ ] **Load Testing** - Benchmark with 10K+ products and concurrent users
- [ ] **CI/CD Pipeline** - GitHub Actions for automated testing and deployment

---

## 🛠️ Development Roadmap

### Phase 1: Backend Core ✅ (Current)
- [x] User authentication system
- [x] Product CRUD operations
- [x] Shopping cart functionality
- [x] Order management
- [x] Production deployment
- [x] Docker containerization
- [x] Redis integration

### Phase 2: Performance & Scale (In Progress)
- [x] Redis integration for caching
- [ ] Advanced database indexing
- [ ] Background job processing with Celery
- [ ] API rate limiting
- [ ] Comprehensive test coverage
- [ ] Load testing and benchmarking

### Phase 3: Frontend & Integration
- [ ] React/Next.js frontend
- [ ] Payment gateway integration (Stripe)
- [ ] Real-time inventory updates
- [ ] Admin dashboard

### Phase 4: Advanced Features
- [ ] Product recommendations engine
- [ ] Search with Elasticsearch
- [ ] Image upload & CDN integration
- [ ] Analytics dashboard

---

## 🧪 Testing the API

### Quick Start (Using cURL)

**1. Register a new user:**
```bash
curl -X POST "https://sports-e-commerce.onrender.com/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepass123","full_name":"John Doe"}'
```

**2. Login to get JWT token:**
```bash
curl -X POST "https://sports-e-commerce.onrender.com/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepass123"
```

**3. Access protected endpoints:**
```bash
curl -X GET "https://sports-e-commerce.onrender.com/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Or use the interactive Swagger UI:** [https://sports-e-commerce.onrender.com/docs](https://sports-e-commerce.onrender.com/docs)

---

## 🏃 Local Development Setup

### Method 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Rashed-AlAmin/Sports_E_Commerce.git
cd Sports_E_Commerce

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and secrets

# Start all services
docker-compose up --build

# Access the API at http://localhost:8000
# Access docs at http://localhost:8000/docs
```

### Method 2: Traditional Setup

```bash
# Clone the repository
git clone https://github.com/Rashed-AlAmin/Sports_E_Commerce.git
cd Sports_E_Commerce

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and secrets

# Run database migrations
alembic upgrade head

# Start Redis (if not using Docker)
redis-server

# Start the development server
uvicorn backend.main:app --reload
```

---

## 📊 Database Schema

**Core Entities:**
- **Users** - Authentication and profile data
- **Products** - Catalog with pricing and inventory
- **Cart Items** - User shopping carts (temporary)
- **Orders** - Completed purchases (permanent)
- **Order Items** - Product snapshots at purchase time

**Relationships:**
- User → Cart Items (One-to-Many)
- User → Orders (One-to-Many)
- Order → Order Items (One-to-Many)
- Product → Cart Items (One-to-Many)

---

## 🔐 Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/dbname

# Security
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis (optional, defaults to localhost)
REDIS_URL=redis://localhost:6379
```

---

## 📈 Why This Architecture?

This project demonstrates understanding of:

1. **Async Programming** - Essential for I/O-bound web applications
2. **Database Design** - Normalized schema with proper relationships
3. **Security** - Industry-standard authentication patterns
4. **Containerization** - Docker for consistent development and deployment
5. **Caching Strategies** - Redis for performance optimization
6. **Scalability** - Architecture ready for load balancing and microservices
7. **Production Readiness** - Deployed, tested, and documented

The codebase follows principles that scale from MVP to millions of users.

---

## 🚢 Deployment

### Current Deployment
- **Platform:** Render
- **Database:** Neon (PostgreSQL)
- **Caching:** Redis (included in docker-compose for local dev)

### Alternative Deployment Options
- **AWS:** ECS with RDS and ElastiCache
- **DigitalOcean:** App Platform with Managed Database
- **Heroku:** Container deployment with Redis add-on
- **Railway:** One-click Docker deployment

---

## 🤝 Contributing

This is a portfolio/learning project, but suggestions and feedback are welcome! Feel free to open issues or submit pull requests.

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**MD Rashed Al Amin**  
- GitHub: [Rashed-AlAmin](https://github.com/Rashed-AlAmin)
- LinkedIn: [md-rashed-al-amin](https://www.linkedin.com/in/md-rashed-al-amin/)
- Email: rashedalamin4@gmail.com

---

## 🎓 Learning Resources

This project was built using best practices from:
- FastAPI Official Documentation
- SQLAlchemy 2.0 Documentation
- PostgreSQL Performance Tuning guides
- Docker and Container Orchestration patterns
- Asyncio Python patterns

---

## 📂 Project Structure

```
Sports_E_Commerce/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic validation schemas
│   ├── routes/              # API endpoint definitions
│   ├── services/            # Business logic layer
│   └── core/                # Configuration and dependencies
├── alembic/                 # Database migrations
├── Dockerfile               # Container definition
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # Project documentation
```

---

**Status:** 🟢 Active Development | Production Deployment Live | Dockerized

**Last Updated:** February 2026