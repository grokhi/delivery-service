# Delivery Service

## Overview

This project is a parcel delivery service built using FastAPI. It allows users to create, view, and manage parcel deliveries with various endpoints supporting parcel registration and data retrieval.

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/grokhi/delivery-service
   cd delivery-service
   ```

2. Install dependencies:

   ```bash
   pip install poetry
   poetry install
   ```

3. Activate the virtual environment:

   ```bash
   poetry shell
   ```

4. Start the Redis server:

   ```bash
   redis-server --daemonize yes
   ```

5. Set up MySQL server:

   - Install and start MySQL server.
   - Create a user and database as needed, or use the default `root` user for simplicity.
   - Run the `.docker/init.sql` file to set up the required database structure:

     ```bash
     mysql -u user -p < ".docker/init.sql"
     ```

6. Run the application in `Local debug` mode using **VSCode** to start the `uvicorn` server.

## How to Run in Docker

1. Start the application using Docker:

   ```bash
   docker-compose up
   ```

**Warning**: MySQL may not recognize the database (fetching `localhost` instead of `delivery`) in some cases, causing errors for SQLAlchemy ORM to fetch data from the table. Docker support is not fully stable, so running the service locally is recommended.

## Run tests

Tests for this project are defined in the ``tests/`` folder.

<!-- Set up environment variable ``DATABASE_URL`` or set up ``database_url`` in ``src/core/settings/test.py`` -->

To make the single endpoint test, simply run the ``pytest tests/parcels/test_create_parcel.py`` command


## API Endpoints

### 1. Create a Parcel

**Endpoint**: `POST /create`  
**Description**: Registers a new parcel.  
**Response Model**: `ParcelCreateResponse`  
**Tags**: `parcels`

### 2. Get Parcel Types

**Endpoint**: `GET /types`  
**Description**: Retrieves all available parcel types.  
**Response Model**: `List[ParcelTypesResponse]`  
**Tags**: `parcels`

### 3. Get List of Parcels

**Endpoint**: `GET /list`  
**Description**: Retrieves a list of parcels with pagination and filtering options.  
**Response Model**: `ParcelListResponse`  
**Tags**: `parcels`

### 4. Get Parcel by ID

**Endpoint**: `GET /{parcel_id}`  
**Description**: Retrieves detailed data for a specific parcel by its ID.  
**Response Model**: `ParcelIdResponse`  
**Tags**: `parcels`

