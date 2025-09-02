# Keycloak Documentation
doc based mainly on : https://www.geeksforgeeks.org/keycloak-create-realm-client-roles-and-user/

## Enter Keyclaok
Admin console > default id/password = `admin` `admin`

## Create a realm
This means the whole app configuration  
On `Realm name` = `PayeTonKawa`

## Create 3 clients
One client for each API which will allow to separate the APIs in different roles (RBAC)
On the left panel `Clients` > click on the `Create Client` button > fill `Client ID` and `Name` with `ptk-<api_name>` > Next > `Client authentication` and `authorization` ON > Next > `Valid redirect URIs` fill with `http://localhost:<api_port>/*` > Save

## Creating client roles
On the left panel `Clients` > select your client (one of the `ptk-<api_name>`) > `Roles` tab > `Create role` > in `Role name` fill with `ptk-<api_name>-role` > Save

## Create a user
### Create user
On the left panel `Users` > `Add user` > enter at least `Username` (`test-user`) > Create
### Assign user a role
On the left panel `Users` > select your user > `Role mapping` tab > `Assign role` > filter with `Filter by clients` on the top left of the openning window > select a `ptk-<api_name>-role` corresponding to the API the user must access
### Set password to user (optionnal)
On the left panel `Users` > select your user > `Credential` tab > Set password > Save

## Curl / Postman Keycloak
Adapter les informations suivantes :
- client_id : keycloak client name
- client_secret : left panel `Clients` > tab `Credentials` > attribute `Client secret`
- grant_type : if `Direct access grants` checked in Client's config
- username : one of Keycloak user's username
- password : Keycloak user's password (**beware NO one time password**)

Example curl :  
```
curl -X POST "http://localhost:8080/realms/PayeTonKawa/protocol/openid-connect/token" \  -H "Content-Type: application/x-www-form-urlencoded" \  -d "client_id=ptk-clients" \  -d "client_secret=***" \  -d "grant_type=password" \  -d "username=test-user" \  -d "password=test1234"
```

## Import or Export a Keycloak realm
Select the realm you want to import or export
### Export a Keycloak realm
On the left panel select `Realm settings` > on the top right corner click on `Action` > select `Partial export` > select `Include groups and roles` and `Include clients` > Press `Export` 
### Import a Keycloak realm
On the left panel select `Realm settings` > on the top right corner click on `Action` > select `Partial import` > select `Browse...` > select your file > select all users, clients, realm roles and client roles > select `Skip` on the dropdown menu > `Import`  