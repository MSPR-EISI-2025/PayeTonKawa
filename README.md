# MSPR4_EISI

## Technical stack
- Docker
- NestJS

## Deployment
```
insert how to do it
```

## Miscellaneous 

 - DB is accessible at  localhost:3306

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
- feature/*: used for developing new features. Created from develop, merged back into develop.

- release/*: used to prepare a new production release. Created from develop, merged into both main and develop.

- hotfix/*: used to fix critical bugs in production. Created from main, merged into both main and develop.

### Examples:
New feature:
- git checkout -b feature/"source_branch"/"my_ticket" develop

Preparing a release:
- git checkout -b release/1.0.0 develop

Urgent fix:
- git checkout -b hotfix/"source_branch"/"my_ticket" main
