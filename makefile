# Fichier : Makefile

# Charger le fichier .env
include .env
export $(shell sed 's/=.*//' .env)

SQL_TEMPLATE=./mock_mariaDB/init/setup-users.sql.template
SQL_OUTPUT=./mock_mariaDB/init/setup-users.sql

.PHONY: all init-sql up importer down clean

# Par défaut : initialise le SQL puis lance tous les services
all: init-sql up

# Injecte les variables dans le fichier SQL
init-sql:
	@echo "📄 Génération du script SQL à partir du template..."
	cat $(SQL_TEMPLATE) | \
		CLIENTS_DB_USER=$(CLIENTS_DB_USER) CLIENTS_DB_PASS=$(CLIENTS_DB_PASS) \
		ORDERS_DB_USER=$(ORDERS_DB_USER)   ORDERS_DB_PASS=$(ORDERS_DB_PASS) \
		PRODUCTS_DB_USER=$(PRODUCTS_DB_USER) PRODUCTS_DB_PASS=$(PRODUCTS_DB_PASS) \
		envsubst '$$CLIENTS_DB_USER $$CLIENTS_DB_PASS $$ORDERS_DB_USER $$ORDERS_DB_PASS $$PRODUCTS_DB_USER $$PRODUCTS_DB_PASS' \
		> $(SQL_OUTPUT)
	@echo "✅ Fichier généré : $(SQL_OUTPUT)"

# Lance tous les services (par défaut)
up:
	@echo "🚀 Démarrage des services..."
	docker compose up -d

# Lance seulement les services du profil 'importer'
importer:
	@echo "🚀 Lancement des services du profil importer..."
	docker compose --profile importer up

# Stoppe les containers
down:
	@echo "🛑 Arrêt des containers..."
	docker compose down

# Supprime les fichiers générés
clean:
	@echo "🧹 Nettoyage..."
	rm -f $(SQL_OUTPUT)
