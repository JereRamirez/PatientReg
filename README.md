# PatientReg
Patient Registration Application

PatientReg is a FastAPI-based application that allows the registration of patients, validating their data, storing it in a PostgreSQL database, and sending an asynchronous confirmation email.

## Features
- Collects patient information: name, email address, phone number, and document photo.
- Validates the provided data.
- Stores the patient data in a PostgreSQL database.
- Sends an asynchronous email confirmation after successful registration.
- Uses Docker and Docker Compose to set up the development environment.

## Requirements
1. Docker
2. Docker Compose

## Setup and Running the Application

### 1. Clone the repository:
```bash
git clone https://github.com/JereRamirez/PatientReg.git
cd PatientReg
```

### 2. Create an .env file:
Create a .env file in the root of the project with the following structure:
```bash
# PostgreSQL Configuration
POSTGRES_DB=<placeholder>
POSTGRES_USER=<placeholder>
POSTGRES_PASSWORD=<placeholder>

# Application Settings
DATABASE_URL=<placeholder>

# Email Configuration
EMAIL_HOST=<placeholder>
EMAIL_PORT=<placeholder>
EMAIL_USER=<placeholder>
EMAIL_PASSWORD=<placeholder>
EMAIL_FROM=<placeholder>
```

Make sure to fill the placeholders with your actual values for the email and PostgreSQL configuration.

### 3. Build and start the containers:
Make sure Docker and Docker Compose are installed, then run the following command to build and start the containers:
docker-compose up --build

This will:
- Build the Docker image for the FastAPI application (api).
- Start the PostgreSQL database (db).
- Set up volumes for database data and file uploads.

### 4. Access the application:
Once the containers are running, you can access the FastAPI application at:
http://localhost:8000

You can use the Swagger UI to interact with the API at:
http://localhost:8000/docs

### 5. Stopping the application:
To stop the application and remove the containers, run:
docker-compose down 

### Database Configuration:
The database URL is configured using the DATABASE_URL environment variable, which uses the PostgreSQL configuration from the .env file.

### Email Configuration:
The email service configuration is set through the environment variables EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, and EMAIL_FROM, which are all required for sending the confirmation emails.

License:
MIT License
