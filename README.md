# MSPR4_EISI

## Technical stack
- Docker
- NestJS

## Deployment
```
insert how to do it
```

## Miscellaneous 

- DB_Auth is accessible at  localhost:3306
- DB_Mock_Data is accessible at  localhost:6000

## Collaborators
-CHANELIERE Romain
- CASELLA Théo
- BOUKHEMIRI Rafik
- ROY Antoine

## GitFlow
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

## Connect NestJS to RabbitMQ
- In each API (clients, orders, product), update main.ts:
```javascript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.connectMicroservice<MicroserviceOptions>({
    transport: Transport.RMQ,
    options: {
      urls: ['amqp://user:password@rabbitmq:5672'],
      queue: 'your_service_queue', // unique for each service
      queueOptions: {
        durable: false
      },
    },
  });

  await app.startAllMicroservices();
  await app.listen(3000);
}
bootstrap();
```

- Each service should use a different queue name (clients_queue, orders_queue, etc.).

- To verify if RabbitMQ is working, there is the management UI : http://localhost:15672
- Login: user / password


# MSPR4_EISI – Data Import Guide

This project includes a mock data importer service (`db_mock_import`) that populates the `db_mock_data` MariaDB instance with fake data from an external API.

By default, the importer **does not run** when starting the application stack. It is **opt-in** via Docker Compose profiles.

---

## 📦 Available Services

| Service           | Description                                | Auto-start with `up` |
|-------------------|--------------------------------------------|-----------------------|
| `db_auth`         | Main MariaDB instance for auth data        | ✅ Yes                |
| `db_mock_data`    | MariaDB for mock data                      | ✅ Yes                |
| `backend_clients` | Backend microservice for clients           | ✅ Yes                |
| `backend_orders`  | Backend microservice for orders            | ✅ Yes                |
| `backend_product` | Backend microservice for products          | ✅ Yes                |
| `db_mock_import`  | **Data importer (mock API → MariaDB)**     | ❌ No (requires profile) |

---

## 🚀 Starting the Application

### 🟢 Start all main services:

```
docker-compose up
```

### 🟡 Run the importer manually:

This starts **only the importer** (and its dependencies like `db_mock_data`):

```
docker-compose --profile importer up db_mock_import
```

You can use this after the DB is up or anytime you want to re-import mock data.

### 🔵 Run everything (including importer):

```
docker-compose --profile importer up
```

---

## 🧼 Stop and clean up

### Stop everything:

```
docker-compose down
```

### Stop only importer-related containers:

```
docker-compose --profile importer down
```

---

## 🔧 Changing Mock API or DB Settings

Environment variables are configured in the `.env` file:

```
MARIADB_MOCK_DATABASE=mockapi_db
MARIADB_MOCK_USER=mockapi_user
MARIADB_MOCK_PASSWORD=mockapiuserpass
MARIADB_MOCK_EXPOSE_PORT=6000
```

Edit these if you need to customize database credentials or ports.

---

## 💡 Tip: One-liner to run importer cleanly

Use this to run the importer in one go and remove the container afterward:

```
docker-compose --profile importer run --rm db_mock_import
```


# Services comunication
```

                 [ CLIENT API ]
                        |
                        v
                    [ Traefik ]
                        |
                        +------------------> [ Keycloak ]
                        |                       (Auth OIDC)
                        |
                        |
            +----------------+------------------+
            |                |                  |
            v                v                  v

+---------------------+   +--------------------+   +----------------------+
|     API CLIENT      |   |    API PRODUIT     |   |    API COMMANDE      |
| - Gestion client    |   | - Catalogue café   |   | - Création commande  |
| - CRUD profils      |   | - Prix, stock      |   | - Suivi des statuts  |
+---------------------+   +--------------------+   +----------------------+
            |                |                  |
            +--------+-------+--------+---------+
                             |
                             v
                       +-----+-----+
                       | RabbitMQ  |
                       +-----------+
                             |
              +--------------+--------------+
              |                             |
       +------+-------+                 +-------+------+
       | Consommateurs | ← événements → | Autres APIs |
       |  internes ou  |                | abonnés (ex.|
       |   externes    |                | facturation)|
       +--------------+                +-------------+

```
