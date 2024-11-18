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
   - Run the `.docker/db/init.sql` file to set up the required database structure:

     ```bash
     mysql -u user -p < ".docker/db/init.sql"
     ```

6. Run the application in `Local debug` mode using **VSCode** to start the `uvicorn` server. Dont forget to specify your connection settings in the `.env` file.

## How to Run in Docker

1. Start the application using Docker:

   ```bash
   docker-compose up
   ```

## Run tests

Tests for this project are defined in the ``tests/`` folder.

To make the single endpoint test, simply run the ``./run_tests.sh`` script

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

