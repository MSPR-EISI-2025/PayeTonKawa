# MSPR4_EISI

## Technical stack
- Docker
- NestJS

## Deployment

### Prérequis
- Docker + Docker Compose
- Un fichier `.env` à la racine

### Étapes de déploiement

1. `cp .env.prod.sample .env`
2. compléter les variables vides
3. **Générer le script SQL avec les utilisateurs pour la db :**

```bash
make init-sql
```

### Lancer tous les services en arrière-plan :

```bash
make up
```

### Importer les données mock :

```bash
make importer
```
### Arrêter les services :

```bash
make down
```

### Nettoyer le fichier SQL généré :

```bash
make clean
```

## Miscellaneous 

 - DB is accessible at  localhost:3306

## Collaborators
- CHANELIERE Romain
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
