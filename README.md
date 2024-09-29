# Django Project with Docker

This is a Django project that uses Docker to streamline the setup and running of the development environment.

## Requirements

- [Docker](https://docs.docker.com/get-docker/) (Make sure you have Docker and Docker Compose installed)

## Running the Project

To get started with this project, follow these steps:

### 1. Clone the repository.

```bash
git clone https://github.com/Vsiprobihy/backend.git
cd backend
```
### 2. Create a `.env` file.
Create a `.env` file in the root directory of your project and add any environment variables that the project needs, such as:
```makefile
GOOGLE_OAUTH_CLIENT_ID=883340219680-mj2cqr29c5009i11aafp4g61sm1hfj29.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=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
SECRET_KEY=RANDOM_SECRET_KEY
```
### 3. Build and run the Docker containers.
To build the Docker containers and start the Django development server, run the following command:
```bash
docker-compose up --build
```
### 4. Useful Docker Commands.
- Rebuild the containers:
```bash
docker-compose up --build
```
- View the logs:
```bash
docker-compose logs -f
```
- Stop the Docker containers:
```bash
docker-compose down
```
