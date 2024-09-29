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
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@db:5432/dbname
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
