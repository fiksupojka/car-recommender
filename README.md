# Repository Code Information

The code in this repository is primarily for demonstration purposes and not intended for real usage, as it has not been containerized.

## Environment and Compatibility

- Python version: 3.13
- PostgreSQL version: 12
- Environment tested: Local installation

## Preparations Before Running Tests

### Database Setup

1. Create a user named `recommender` with no password:
   ```sql
   CREATE USER recommender;
   
2. Create a database named recommender:
   
   ```sql
   CREATE DATABASE recommender;

3. Grant all privileges on the database recommender to the user recommender:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE recommender TO recommender;

### Virtual Environment Setup
   
1. Create a virtual environment:
    ```bash
    python3 -m venv myenv

2. Activate the virtual environment:
    ```bash
    source myenv/bin/activate

3. Install all necessary libraries:
    ```bash
    pip3 install -r requirements.txt

### Running the Server

1. In the virtual environment, start the server using Uvicorn:

    ```bash
    uvicorn main:app --reload

### Running Tests

1. In the virtual environment, execute the tests:
    ```bash
    pytest -s test_api.py