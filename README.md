# Bank transaction website

## Overview
A full stack web application for tracking bank transactions. Uses Plaid to retrieve banking information. Split into a React frontend and a FastAPI backend.

## Features
- Sign up users
- Link bank accounts using Plaid
- View transactions

## Tech stack

- [Docker](https://www.docker.com/) - Runs both frontend and backend 

### Frontend
- [Typescript](https://www.typescriptlang.org/) - Language
- [React](https://react.dev/) - Web framework
- [Plaid Link](https://plaid.com/docs/link/) - Setup bank accounts with plaid

### Backend
- [Python](https://www.python.org/) - Language
- [FastAPI](https://fastapi.tiangolo.com/) - Manages API routes
- [PostgreSQL](https://www.postgresql.org/) -  Database
- [SQLModel](https://sqlmodel.tiangolo.com/) - Manage Database in Python
- [Plaid](https://plaid.com/) - Retrieves bank information for users
- [AuthLib](https://authlib.org/) - OAuth OpenID Connect library
  - [Microsoft Entra](https://www.microsoft.com/en-gb/security/business/microsoft-entra) - IDP
  - [Google](https://docs.cloud.google.com/architecture/identity/overview-google-authentication) - IDP
- [Pytest](https://docs.pytest.org/) - Testing library

## Build and run

### Requirements
- [Docker](https://www.docker.com/)

### Frontend
``` bash
cd frontend
docker compose up --build
```
To view the application open: http://localhost:3000/ 

### Backend

``` bash
cd backend
docker compose up --build
```
The routes are accessible at: http://localhost:8000/.
Swagger API docs at: http://localhost:8000/docs.
## Project structure
The project is divided into two sections: frontend & backend.

### Frontend
 - /components - Custom React components
 - /pages - React components which act as pages
 - /serverConnect - Handles API calls to the server

### Backend
 - /app/database - Manages database connection
 - /app/services/auth_service.py - Manages user authentication within the app
 - /app/services/idp_service.py - Manages IDPs when users log in
 - /app/services/plaid_service.py - Manages Plaid API requests
 - /app/config.py - Environment variables
 - /app/main.py - FastAPI routes
 - /tests - PyTest tests

## Testing

Tests for the backend use [Pytest](https://docs.pytest.org/).

To run tests make sure the docker container is running and run the following command:
``` bash
docker exec -it fastapi_app pytest tests
```


