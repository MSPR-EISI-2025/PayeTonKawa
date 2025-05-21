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
- CHANELIERE Romain
- CASELLA Théo
- BOUKHEMIRI Rafik
- ROY Antoine


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

