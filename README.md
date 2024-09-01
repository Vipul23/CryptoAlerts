# CryptoAlerts

#  Steps to run the project
1. Clone the repository
    ```bash
     git clone https://github.com/Vipul23/CryptoAlerts
    ```
2. Make sure that port 8000 is available
    On unix systems, check if a process is using the port following command
    ```bash
    sudo lsof -i :8000
    ```
3. Create a file `docker.env` that holds the environment variables changed as per the requirement
    ```env
    IS_PROD_DEPLOYMENT=TRUE # Set to FALSE for development

    DJANGO_SECRET_KEY="7+20m*njaz9)2jhq(h!rue@y=m2nn@mh0x=^vj9gz3hbzb&gzd"  # Should be changed

    POSTGRES_DB_USER=postgres
    POSTGRES_DB_NAME=cryptoservice
    POSTGRES_DB_PASSWORD=password
    POSTGRES_DB_HOST=db
    POSTGRES_DB_PORT=5432

    REDIS_URL=redis://redis:6379/0
    REDIS_HOST=redis

    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=<email address>
    EMAIL_HOST_PASSWORD=< password >
    ```
    and create a file .env with the content which is used to create admin account (superuser)
    ```env
    DJANGO_SUPERUSER_PASSWORD=password
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_USERNAME=admin
    ```
4. Run `docker compose up --build` or `docker compose up --build -d` to not see logs
5. The apis will be available at `http://localhost:8000`

# Endpoints

- `/api/token/`
    - POST: To get the JWT token by providing the username and password
    - Request Body: 
        ```json
        {
            "username": "test",
            "password": "test"
        }
        ```
    - Response
- `/api/token/refresh/`
    - POST: To refresh the JWT token by providing the refresh token
    - Request Body: 
        ```json
        {
            "refresh": "refreshtoken"
        }
        ```
- `/api/users/`
    - POST: To create a user
    - Request Header: 
        ```json
        {
            "Authorization ": "Bearer <JWT Token>"
        }
        ```
    - Request Body: 
        ```json
        {
            "username": "test",
            "password": "test",
            "email": "example@example.com",
            "is_staff": false
        }
        ```
- `/api/users/`
    - GET: To get all the users
    - Request Header: 
        ```json
        {
            "Authorization ": "Bearer <JWT Token>"
        }
        ```
        

- `/api/alerts/`
    - GET: To get all the alerts
    - Request Header: 
        ```json
        {
            "Authorization ": "Bearer <JWT Token>" 
        }
        ```
    - Query Params:
        - `status`: To filter the alerts based on the status
        - `symbol`: To filter the alerts based on the coin symbol
- `/api/alerts/create/`
    - POST: To create an alert
    - Request Header: 
        ```json
        {
            "Authorization ": "Bearer <JWT Token>"
        }
        ```
    - Request Body: 
        ```json
        {
        "name":"Alert Name",
        "symbol":"Coin Symbol",
        "price":alert price
        }
        ```
- `/api/alerts/delete/<alert_id>/`
    - DELETE: To delete an alert
    - Request Header: 
        ```json
        {
            "Authorization ": "Bearer <JWT Token>"
        }
        ```

# Alerts
To send alerts, the Binance websocket is connected by a python script, this then saves the data to a redis cache. A Celery beat worker then checks the alerts every minute against the data. If the alert is triggered, SMTP is used to send an email to the user.

# Project Structure and Architecture
The docker compose file launches 6 services, 
1. Postgres
    - This is the database.
2. Redis
    - This is redis cache used for storing the coin prices from binance and the page caches for all alerts.
3. Django
    - This is the main application that serves the APIs.
    - It uses Django Rest Framework for the APIs and JWT for authentication.
    - It has separate paths for users and alerts at /api/users and /api/alerts
    - The users can only be modified or viewed by superuser admins
    - The alerts can be created, deleted and viewed by the user who created them
    - The alerts are also cached in redis for faster access
    - The alerts are also paginated
    - The alerts can also be filtered based on the status and the coin symbol
4. Celery Worker , Celery Beat Worker
    - These are celery workers that runs every minute to check the alerts against the coin prices.They then send mail if price is acheived
5. Binance API Script
    - This is a python script that connects to the binance websocket and saves the coin prices to the redis cache.It also has exponential backoff implemented in case of network failure or binance server failure.
