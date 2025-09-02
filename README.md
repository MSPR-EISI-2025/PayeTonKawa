# MSPR4_EISI

## Technical stack
- Docker
- DB : mariadb
- API : NestJS
- Auth provider : Keycloak

***insert archi shem - Miro***

KC DB has its own db compared to db used mariadb DB

## Deployment
```
git clone git@github.com:MSPR-EISI-2025/PayeTonKawa.git
git submodule update --init --recursive
docker compose up
```

## Miscellaneous 

 - DB is accessible at  localhost:3306

## GitFlow
## Branches principales :
- main : contient la version stable en production.

- develop : contient le code en cours de développement, prêt à être intégré.
## Branches de support :
- `feature/*` : pour le développement de nouvelles fonctionnalités. Créées depuis develop, fusionnées dans develop.

- `release/*` : pour préparer une nouvelle version. Créées depuis develop, fusionnées dans main et develop.

- `hotfix/*` : pour corriger des bugs en production. Créées depuis main, fusionnées dans main et develop.
## Exemples
- Nouvelle fonctionnalité : `git checkout -b feature/"branche d'origine"/"mon_ticket" develop`

- Préparation d’une release : `git checkout -b release/1.0.0 develop`

- Correction urgente : `git checkout -b hotfix/"branche d'origine"/"mon_ticket" main`

## Collaborators
- CHANELIERE Romain
- CASELLA Théo
- BOUKHEMIRI Rafik
- ROY Antoine