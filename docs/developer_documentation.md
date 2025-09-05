# Developer Documentation - PayeTonKawa

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Development Environment Setup](#development-environment-setup)
5. [API Documentation](#api-documentation)
6. [Database Schema](#database-schema)
7. [Authentication & Security](#authentication--security)
8. [Message Broker Integration](#message-broker-integration)
9. [Docker Configuration](#docker-configuration)
10. [CI/CD Pipeline](#cicd-pipeline)
11. [Testing Strategy](#testing-strategy)
12. [Monitoring & Logging](#monitoring--logging)
13. [Deployment Guide](#deployment-guide)
14. [Development Guidelines](#development-guidelines)
15. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

PayeTonKawa is built using a microservices architecture with the following components:

### System Architecture
```
[Client] → [Traefik Reverse Proxy] → [Microservices]
                    ↓
            [Keycloak Auth Provider]
                    ↓
        [RabbitMQ Message Broker] ← → [MariaDB Database]
```

### Core Services
- **API Gateway (Traefik)**: Entry point, routing, TLS termination, authentication middleware
- **Auth Provider (Keycloak)**: Identity provider, OAuth2/OIDC, JWT token management
- **API Client**: Client management service
- **API Product**: Product catalog and inventory management
- **API Order**: Order processing and management
- **Message Broker (RabbitMQ)**: Asynchronous communication between services
- **Database (MariaDB)**: Shared database with service-specific user permissions

### Design Principles
- **Single Responsibility**: Each microservice handles one business domain
- **Loose Coupling**: Services communicate via REST APIs and async messaging
- **High Cohesion**: Related functionality grouped within services
- **Fault Tolerance**: Services can operate independently
- **Scalability**: Individual services can be scaled based on demand

---

## Technology Stack

### Backend Technologies
- **Runtime**: Node.js 20.x
- **Framework**: NestJS (TypeScript-based)
- **Language**: TypeScript 5.x
- **Database**: MariaDB 10.x
- **Message Broker**: RabbitMQ 3.x
- **Authentication**: Keycloak
- **API Gateway**: Traefik 2.x

### Development Tools
- **Package Manager**: npm
- **Testing**: Jest
- **Code Quality**: ESLint, SonarCloud
- **API Documentation**: Swagger/OpenAPI
- **API Testing**: Postman/Newman

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Registry**: Docker Hub
- **Monitoring**: Prometheus, Grafana, Loki
- **Version Control**: Git (GitFlow)

---

## GitFlow
Developers who need to create a branch to work on a task, please follow these guidelines to maintain a clear and structured gitflow

### Main Branches:

- main: contains the stable version deployed to production.

- develop: contains the code currently in development, ready for integration.

### Supporting Branches:

- feature/*: used for developing new features. Created from `develop`, merged back into `develop`.

- release/*: used to prepare a new production release. Created from `develop`, merged into both `main` and `develop`.

- hotfix/*: used to fix critical bugs in production. Created from `main`, merged into both `main` and `develop`.

### Examples:

- New feature:
  `git checkout -b feature/develop/"my_ticket" develop`

- Preparing a release:
  `git checkout -b release/1.0.0 develop`

- Urgent fix:
  `git checkout -b hotfix/"source_branch"/"my_ticket" main`

##CI/CD
### Sonarscans et Code Coverage (+linting)
These jobs are available on the repositories of each APIs and on the main repository. They are launch on the main branch (free subscription only allow one branch).
The secrets used for are also stored on each repositories.

### Units Tests and API Tests
The jobs that launch the units tests and API tests are located on the main repository (PayeTonKawa).
The units tests are launched at each commit/MR on the main or develop branches.
The API test are manually launched on the version running on the production server.

###Images Build
The job to build the container images for the project is located on the main repository and is launched 
at each commit/push on the main branch.
The images are then stored in the dockerhub registry. The secrets are stored on PAyeTonKawa repository.

###Deployment
The job to deploy a version on the production server is also located on the PayeTonKawa repository.
It uses a ssh connexion to access the production server and the pull the images from the dockerhub registry
to deploy the app using docker-compose. Be careful not to modify the .env or deploy a new .env to avoid breaking the production.
Secrets are stored on the main repository. 

##Monitoring
For all developers who wants to watch in real time the health of the application, please go to the grafana dashboard.
If you want to add new targets to monitor, please connect to the production serveur and edit the prometheus.yml.
If you want to edit the grafana dashboard, please ask an admin to give you the rights.

---

## Project Structure

### Repository Organization
The project uses a multi-repository approach:

```
payetonkawa/
├── api-client/              # Client management service
├── api-products/            # Product catalog service  
├── api-orders/              # Order processing service
├── infrastructure/          # Docker configs, deployment scripts
└── documentation/           # Project documentation
```

### Service Structure (NestJS)
```
api-{service}/
├── src/
│   ├── controllers/         # HTTP request handlers
│   ├── services/           # Business logic
│   ├── entities/           # Database entities
│   ├── dto/                # Data Transfer Objects
│   ├── guards/             # Authentication guards
│   ├── middleware/         # Custom middleware
│   ├── modules/            # NestJS modules
│   └── main.ts             # Application entry point
├── test/                   # Test files
├── docker/                 # Dockerfile and configs
├── .github/workflows/      # CI/CD workflows
├── package.json
├── tsconfig.json
└── README.md
```

---

## Development Environment Setup

### Prerequisites
```bash
# Required software
node --version    # v20.x or higher
npm --version     # v10.x or higher  
docker --version  # v24.x or higher
git --version     # v2.x or higher
```

### Local Development Setup

1. **Clone Repositories**
```bash
git clone https://github.com/payetonkawa/api-client.git
git clone https://github.com/payetonkawa/api-products.git
git clone https://github.com/payetonkawa/api-orders.git
git clone https://github.com/payetonkawa/infrastructure.git
```

2. **Install Dependencies**
```bash
cd api-client && npm ci
cd api-products && npm ci  
cd api-orders && npm ci
```

3. **Environment Configuration**
Create `.env` files in each service:
```bash
# .env example
NODE_ENV=development
PORT=3000
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=payetonkawa_client
DATABASE_PASSWORD=secure_password
DATABASE_NAME=payetonkawa
RABBITMQ_URL=amqp://localhost:5672
JWT_SECRET=your_jwt_secret
```

4. **Start Infrastructure Services**
```bash
cd infrastructure
docker-compose up -d mariadb rabbitmq keycloak
```

5. **Database Initialization**
```bash
# Run migration scripts
npm run migration:run
npm run seed:dev
```

6. **Start Development Services**
```bash
# Terminal 1
cd api-client && npm run start:dev

# Terminal 2  
cd api-products && npm run start:dev

# Terminal 3
cd api-orders && npm run start:dev
```

---

## API Documentation

### Base URLs
- **API Client**: `http://localhost:3000`
- **API Products**: `http://localhost:3002`  
- **API Orders**: `http://localhost:3001`

### Common Headers
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
Accept: application/json
```

### Client API Endpoints

#### GET /clients
Retrieve all clients
```http
GET /clients
Response: 200 OK
[
  {
    "id": "client-uuid",
    "name": "Coffee Shop Inc",
    "contact": "John Doe",
    "email": "john@coffeeshop.com",
    "phone": "+1234567890",
    "address": "123 Main St",
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  }
]
```

#### POST /clients
Create new client
```http
POST /clients
Content-Type: application/json

{
  "name": "New Coffee Shop",
  "contact": "Jane Smith", 
  "email": "jane@newcoffee.com",
  "phone": "+1987654321",
  "address": "456 Oak Ave"
}

Response: 201 Created
{
  "id": "new-client-uuid",
  "name": "New Coffee Shop",
  "contact": "Jane Smith",
  "email": "jane@newcoffee.com", 
  "phone": "+1987654321",
  "address": "456 Oak Ave",
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-01-01T00:00:00Z"
}
```

#### PUT /clients/:id
Update existing client
```http
PUT /clients/client-uuid
Content-Type: application/json

{
  "name": "Updated Coffee Shop",
  "phone": "+1111111111"
}

Response: 200 OK
{
  "id": "client-uuid",
  "name": "Updated Coffee Shop",
  "contact": "John Doe",
  "email": "john@coffeeshop.com",
  "phone": "+1111111111",
  "address": "123 Main St",
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-01-02T00:00:00Z"
}
```

#### DELETE /clients/:id
Soft delete client
```http
DELETE /clients/client-uuid
Response: 204 No Content
```

### Product API Endpoints

#### GET /products
Retrieve all products
```http
GET /products
Response: 200 OK
[
  {
    "id": "product-uuid",
    "name": "Premium Coffee Blend",
    "description": "High-quality coffee blend",
    "reference": "PCB-001",
    "price": 24.99,
    "stock": 100,
    "category": "Coffee",
    "unit": "kg",
    "active": true,
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  }
]
```

#### POST /products
Create new product
```http
POST /products
Content-Type: application/json

{
  "name": "Espresso Beans",
  "description": "Premium espresso beans",
  "reference": "ESP-001", 
  "price": 29.99,
  "stock": 50,
  "category": "Coffee",
  "unit": "kg"
}

Response: 201 Created
```

### Order API Endpoints

#### GET /orders
Retrieve all orders
```http
GET /orders
Response: 200 OK
[
  {
    "id": "order-uuid",
    "clientId": "client-uuid",
    "status": "validated",
    "totalAmount": 149.95,
    "items": [
      {
        "productId": "product-uuid",
        "quantity": 5,
        "unitPrice": 24.99,
        "totalPrice": 124.95
      }
    ],
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  }
]
```

#### POST /orders
Create new order
```http
POST /orders
Content-Type: application/json

{
  "clientId": "client-uuid",
  "items": [
    {
      "productId": "product-uuid",
      "quantity": 3
    }
  ]
}

Response: 201 Created
```

### Error Responses
```http
400 Bad Request
{
  "statusCode": 400,
  "message": "Validation failed",
  "errors": ["name should not be empty"]
}

401 Unauthorized  
{
  "statusCode": 401,
  "message": "Unauthorized"
}

404 Not Found
{
  "statusCode": 404,
  "message": "Resource not found"
}

409 Conflict
{
  "statusCode": 409,
  "message": "Insufficient stock"
}

500 Internal Server Error
{
  "statusCode": 500,
  "message": "Internal server error"
}
```

---

## Database Schema

### Database Design
Single MariaDB database with service-specific users and permissions.

### Database Users
```sql
-- Client service user
CREATE USER 'payetonkawa_client'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON payetonkawa.clients TO 'payetonkawa_client'@'%';

-- Product service user  
CREATE USER 'payetonkawa_product'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON payetonkawa.products TO 'payetonkawa_product'@'%';

-- Order service user
CREATE USER 'payetonkawa_order'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON payetonkawa.orders TO 'payetonkawa_order'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON payetonkawa.order_items TO 'payetonkawa_order'@'%';
GRANT SELECT ON payetonkawa.clients TO 'payetonkawa_order'@'%';
GRANT SELECT ON payetonkawa.products TO 'payetonkawa_order'@'%';
```

### Table Schemas

#### Clients Table
```sql
CREATE TABLE clients (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_clients_email (email),
    INDEX idx_clients_active (active)
);
```

#### Products Table
```sql
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    reference VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    category VARCHAR(100),
    unit VARCHAR(50) DEFAULT 'piece',
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_products_reference (reference),
    INDEX idx_products_category (category),
    INDEX idx_products_active (active)
);
```

#### Orders Table
```sql
CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    client_id VARCHAR(36) NOT NULL,
    status ENUM('in_progress', 'validated', 'shipped', 'delivered', 'cancelled') DEFAULT 'in_progress',
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (client_id) REFERENCES clients(id),
    INDEX idx_orders_client (client_id),
    INDEX idx_orders_status (status),
    INDEX idx_orders_created (created_at)
);
```

#### Order Items Table
```sql
CREATE TABLE order_items (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    order_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_order_items_order (order_id),
    INDEX idx_order_items_product (product_id)
);
```

---

## Authentication & Security

### Keycloak Configuration

#### Realm Setup
```json
{
  "realm": "payetonkawa",
  "enabled": true,
  "sslRequired": "external",
  "registrationAllowed": false,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "resetPasswordAllowed": true,
  "editUsernameAllowed": false,
  "bruteForceProtected": true
}
```

#### Client Configuration
```json
{
  "clientId": "payetonkawa-api",
  "enabled": true,
  "clientAuthenticatorType": "client-secret",
  "redirectUris": ["http://localhost:3000/*"],
  "webOrigins": ["http://localhost:3000"],
  "protocol": "openid-connect",
  "publicClient": false,
  "bearerOnly": false,
  "standardFlowEnabled": true,
  "serviceAccountsEnabled": true
}
```

### JWT Token Structure
```json
{
  "exp": 1735689600,
  "iat": 1735686000,
  "jti": "jwt-id",
  "iss": "http://localhost:8080/realms/payetonkawa",
  "aud": "payetonkawa-api",
  "sub": "user-uuid",
  "typ": "Bearer",
  "azp": "payetonkawa-api",
  "preferred_username": "john.doe",
  "email": "john@example.com",
  "realm_access": {
    "roles": ["admin", "user"]
  },
  "resource_access": {
    "payetonkawa-api": {
      "roles": ["client-manager", "order-manager"]
    }
  }
}
```

### Traefik Middleware Configuration
```yaml
# traefik.yml
http:
  middlewares:
    keycloak-auth:
      forwardAuth:
        address: "http://keycloak:8080/realms/payetonkawa/protocol/openid-connect/auth"
        authResponseHeaders:
          - "X-User-Id"
          - "X-User-Email"
          - "X-User-Roles"
```

### NestJS Authentication Guard
```typescript
// auth.guard.ts
@Injectable()
export class JwtAuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);
    
    if (!token) {
      throw new UnauthorizedException();
    }
    
    try {
      const payload = this.jwtService.verify(token);
      request.user = payload;
      return true;
    } catch {
      throw new UnauthorizedException();
    }
  }
  
  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
```

---

## Message Broker Integration

### RabbitMQ Setup

#### Exchange and Queue Configuration
```typescript
// rabbitmq.config.ts
export const rabbitMQConfig = {
  exchanges: [
    {
      name: 'payetonkawa.events',
      type: 'topic',
      options: { durable: true }
    }
  ],
  queues: [
    {
      name: 'client.events',
      options: { durable: true },
      routingKey: 'client.*'
    },
    {
      name: 'order.events', 
      options: { durable: true },
      routingKey: 'order.*'
    },
    {
      name: 'product.events',
      options: { durable: true }, 
      routingKey: 'product.*'
    }
  ]
};
```

### Event Publishing

#### Client Service Event Publisher
```typescript
// client.service.ts
@Injectable()
export class ClientService {
  constructor(
    @Inject('RABBITMQ_SERVICE') private readonly client: ClientProxy
  ) {}
  
  async updateClient(id: string, updateData: UpdateClientDto): Promise<Client> {
    const updatedClient = await this.clientRepository.update(id, updateData);
    
    // Publish event
    this.client.emit('client.updated', {
      clientId: id,
      data: updatedClient,
      timestamp: new Date()
    });
    
    return updatedClient;
  }
}
```

### Event Consumption

#### Order Service Event Listener
```typescript
// order.service.ts
@Injectable()
export class OrderService {
  constructor(private readonly cacheManager: Cache) {}
  
  @EventPattern('client.updated')
  async handleClientUpdated(data: any) {
    const { clientId, data: clientData } = data;
    
    // Update local cache
    await this.cacheManager.set(`client:${clientId}`, clientData, 3600);
    
    console.log(`Client ${clientId} updated in cache`);
  }
  
  @EventPattern('order.created')
  async handleOrderCreated(data: any) {
    const { orderId, items } = data;
    
    // Update product stocks
    for (const item of items) {
      await this.updateProductStock(item.productId, -item.quantity);
    }
    
    console.log(`Order ${orderId} processed, stocks updated`);
  }
}
```

### Message Patterns
- **client.updated**: Published when client data changes
- **client.deleted**: Published when client is soft deleted
- **order.created**: Published when new order is created
- **order.validated**: Published when order status changes to validated
- **order.cancelled**: Published when order is cancelled
- **product.stock.updated**: Published when product stock changes

---

## Docker Configuration

### Service Dockerfile Example
```dockerfile
# api-client/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .
RUN npm run build

FROM node:20-alpine AS production

WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

EXPOSE 3000

USER node
CMD ["node", "dist/main.js"]
```

### Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

  keycloak:
    image: quay.io/keycloak/keycloak:23.0
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin123
      KC_DB: mariadb
      KC_DB_URL: jdbc:mariadb://mariadb:3306/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: keycloak123
    command: start-dev
    ports:
      - "8081:8080"
    depends_on:
      - mariadb

  mariadb:
    image: mariadb:10.11
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: payetonkawa
      MYSQL_USER: payetonkawa
      MYSQL_PASSWORD: payetonkawa123
    ports:
      - "3306:3306"
    volumes:
      - mariadb_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  rabbitmq:
    image: rabbitmq:3.12-management
    environment:
      RABBITMQ_DEFAULT_USER: payetonkawa
      RABBITMQ_DEFAULT_PASS: rabbitmq123
    ports:
      - "5672:5672"
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  api-client:
    build: ./api-client
    environment:
      NODE_ENV: production
      DATABASE_HOST: mariadb
      DATABASE_USER: payetonkawa_client
      DATABASE_PASSWORD: client123
      RABBITMQ_URL: amqp://payetonkawa:rabbitmq123@rabbitmq:5672
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api-client.rule=PathPrefix(`/clients`)"
      - "traefik.http.services.api-client.loadbalancer.server.port=3000"
    depends_on:
      - mariadb
      - rabbitmq

  api-products:
    build: ./api-products
    environment:
      NODE_ENV: production
      DATABASE_HOST: mariadb
      DATABASE_USER: payetonkawa_product
      DATABASE_PASSWORD: product123
      RABBITMQ_URL: amqp://payetonkawa:rabbitmq123@rabbitmq:5672
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api-products.rule=PathPrefix(`/products`)"
      - "traefik.http.services.api-products.loadbalancer.server.port=3000"
    depends_on:
      - mariadb
      - rabbitmq

  api-orders:
    build: ./api-orders
    environment:
      NODE_ENV: production
      DATABASE_HOST: mariadb
      DATABASE_USER: payetonkawa_order
      DATABASE_PASSWORD: order123
      RABBITMQ_URL: amqp://payetonkawa:rabbitmq123@rabbitmq:5672
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api-orders.rule=PathPrefix(`/orders`)"
      - "traefik.http.services.api-orders.loadbalancer.server.port=3000"
    depends_on:
      - mariadb
      - rabbitmq

volumes:
  mariadb_data:
  rabbitmq_data:
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

#### Service CI Pipeline
```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mariadb:
        image: mariadb:10.11
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
        options: >-
          --health-cmd="mysqladmin ping"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3
        ports:
          - 3306:3306

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run unit tests
        run: npm run test:cov

      - name: Run integration tests
        run: npm run test:e2e
        env:
          DATABASE_HOST: localhost
          DATABASE_PORT: 3306
          DATABASE_USER: root
          DATABASE_PASSWORD: root
          DATABASE_NAME: test_db

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            payetonkawa/api-client:latest
            payetonkawa/api-client:${{ github.sha }}
```

#### Main Repository CD Pipeline
```yaml
# .github/workflows/cd.yml
name: CD Pipeline

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types:
      - completed
    branches: [main]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    
    steps:
      - name: Checkout infrastructure
        uses: actions/checkout@v4

      - name: Setup environment
        run: |
          docker-compose up -d
          sleep 30

      - name: Run API tests
        run: |
          npm install -g newman
          newman run postman/PayeTonKawa_Collection.json \
            -e postman/PayeTonKawa_Environment.json \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export reports/newman-report.html

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: newman-report
          path: reports/

      - name: Cleanup
        if: always()
        run: docker-compose down -v

  deploy:
    needs: integration-test
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/payetonkawa
            docker-compose pull
            docker-compose up -d
            docker system prune -f
```

### SonarCloud Configuration
```yaml
# sonar-project.properties
sonar.projectKey=payetonkawa_api-client
sonar.organization=payetonkawa
sonar.sources=src
sonar.tests=test
sonar.exclusions=**/*.spec.ts,**/*.e2e-spec.ts,**/node_modules/**
sonar.test.inclusions=**/*.spec.ts,**/*.e2e-spec.ts
sonar.typescript.lcov.reportPaths=coverage/lcov.info
sonar.coverage.exclusions=**/*.spec.ts,**/*.e2e-spec.ts,**/main.ts
```

---

## Testing Strategy

### Unit Tests with Jest

#### Service Test Example
```typescript
// client.service.spec.ts
describe('ClientService', () => {
  let service: ClientService;
  let repository: Repository<Client>;
  let mockClient: DeepMocked<ClientProxy>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ClientService,
        {
          provide: getRepositoryToken(Client),
          useValue: createMock<Repository<Client>>(),
        },
        {
          provide: 'RABBITMQ_SERVICE',
          useValue: createMock<ClientProxy>(),
        },
      ],
    }).compile();

    service = module.get<ClientService>(ClientService);
    repository = module.get<Repository<Client>>(getRepositoryToken(Client));
    mockClient = module.get('RABBITMQ_SERVICE');
  });

  describe('createClient', () => {
    it('should create a client and emit event', async () => {
      const createClientDto: CreateClientDto = {
        name: 'Test Company',
        contact: 'John Doe',
        email: 'john@test.com',
        phone: '123456789',
        address: '123 Test St',
      };

      const savedClient = { id: 'uuid', ...createClientDto };
      repository.save = jest.fn().mockResolvedValue(savedClient);
      mockClient.emit = jest.fn();

      const result = await service.createClient(createClientDto);

      expect(result).toEqual(savedClient);
      expect(repository.save).toHaveBeenCalledWith(createClientDto);
      expect
```

## GitFlow
Developers who need to create a branch to work on a task, please follow these guidelines to maintain a clear and structured gitflow

### Main Branches:

- main: contains the stable version deployed to production.

- develop: contains the code currently in development, ready for integration.

### Supporting Branches:

- feature/*: used for developing new features. Created from `develop`, merged back into `develop`.

- release/*: used to prepare a new production release. Created from `develop`, merged into both `main` and `develop`.

- hotfix/*: used to fix critical bugs in production. Created from `main`, merged into both `main` and `develop`.

### Examples:

- New feature:
  `git checkout -b feature/develop/"my_ticket" develop`

- Preparing a release:
  `git checkout -b release/1.0.0 develop`

- Urgent fix:
  `git checkout -b hotfix/"source_branch"/"my_ticket" main`

##CI/CD
### Sonarscans et Code Coverage (+linting)
These jobs are available on the repositories of each APIs and on the main repository. They are launch on the main branch (free subscription only allow one branch).
The secrets used for are also stored on each repositories.

### Units Tests and API Tests
The jobs that launch the units tests and API tests are located on the main repository (PayeTonKawa).
The units tests are launched at each commit/MR on the main or develop branches.
The API test are manually launched on the version running on the production server.

### Images Build
The job to build the container images for the project is located on the main repository and is launched 
at each commit/push on the main branch.
The images are then stored in the dockerhub registry. The secrets are stored on PAyeTonKawa repository.

### Deployment
The job to deploy a version on the production server is also located on the PayeTonKawa repository.
It uses a ssh connexion to access the production server and the pull the images from the dockerhub registry
to deploy the app using docker-compose. Be careful not to modify the .env or deploy a new .env to avoid breaking the production.
Secrets are stored on the main repository. 

## Monitoring
For all developers who wants to watch in real time the health of the application, please go to the grafana dashboard.
If you want to add new targets to monitor, please connect to the production serveur and edit the prometheus.yml.
If you want to edit the grafana dashboard, please ask an admin to give you the rights.


## Keycloak Documentation
<!--doc based mainly on : https://www.geeksforgeeks.org/keycloak-create-realm-client-roles-and-user/ -->

### Enter Keyclaok
Admin console > default id/password = `admin` `admin`  

### Create a realm
This means the whole app configuration  
On `Realm name` = `PayeTonKawa`

### Create 3 clients
One client for each API which will allow to separate the APIs in different roles (RBAC)  
On the left panel `Clients` > click on the `Create Client` button > fill `Client ID` and `Name` with `ptk-<api_name>` > Next > `Client authentication` and `authorization` ON > Next > `Valid redirect URIs` fill with `http://localhost:<api_port>/*` > Save

### Creating client roles
On the left panel `Clients` > select your client (one of the `ptk-<api_name>`) > `Roles` tab > `Create role` > in `Role name` fill with `ptk-<api_name>-role` > Save

### Create a user
#### Create user
On the left panel `Users` > `Add user` > enter at least `Username` (`test-user`) > Create
#### Assign user a role
On the left panel `Users` > select your user > `Role mapping` tab > `Assign role` > filter with `Filter by clients` on the top left of the openning window > select a `ptk-<api_name>-role` corresponding to the API the user must access
#### Set password to user (optionnal)
On the left panel `Users` > select your user > `Credential` tab > Set password > Save

### Curl / Postman Keycloak
Adapter les informations suivantes :
- client_id : keycloak client name
- client_secret : left panel `Clients` > tab `Credentials` > attribute `Client secret`
- grant_type : if `Direct access grants` checked in Client's config
- username : one of Keycloak user's username
- password : Keycloak user's password (**beware NO one time password**)

Example curl : 
```
curl -X POST "https://keycloak.lucette-pomponette.fr/realms/PayeTonKawa/protocol/openid-connect/token" \  -H "Content-Type: application/x-www-form-urlencoded" \  -d "client_id=ptk-clients" \  -d "client_secret=***" \  -d "grant_type=password" \  -d "username=test-user" \  -d "password=test1234"
```
Vérification
```
curl -H "Authorization: Bearer $TOKEN" https://api.lucette-pomponette.fr/orders
```

### Import or Export a Keycloak realm
Select the realm you want to import or export
#### Export a Keycloak realm
On the left panel select `Realm settings` > on the top right corner click on `Action` > select `Partial export` > select `Include groups and roles` and `Include clients` > Press `Export` 
#### Import a Keycloak realm
On the left panel select `Realm settings` > on the top right corner click on `Action` > select `Partial import` > select `Browse...` > select your file > select all users, clients, realm roles and client roles > select `Skip` on the dropdown menu > `Import`  