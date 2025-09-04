# Developer documentation

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
