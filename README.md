# CryptoAlerts

# tanx.fi Assignment

#  Steps to run the project
1. Clone the repository
2. Make sure that port 8000 is available
3. Create a file `docker.env` that holds the environment variables changed as per the requirement
    ```env
    IS_PROD_DEPLOYMENT=FALSE

    DJANGO_SECRET_KEY=7+20m*njaz9)2jhq(h!rue@y=m2nn@mh0x=^vj9gz3hbzb&gzd  # Should be changed

    POSTGRES_DB_USER=postgres
    POSTGRES_DB_NAME=cryptoservice
    POSTGRES_DB_PASSWORD=password
    POSTGRES_DB_HOST=db
    POSTGRES_DB_PORT=5432

    ENABLE_CELERY=TRUE
    REDIS_URL=redis://redis:6379/0
    REDIS_HOST=redis

    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=email@example.com
    EMAIL_HOST_PASSWORD=passwordtosmtp

    DJANGO_SUPERUSER_PASSWORD=password
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_USERNAME=admin
    ```
4. Run `docker compose up --build`
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
- `/api/token/refresh`
    - POST: To refresh the JWT token by providing the refresh token
    - Request Body: 
        ```json
        {
            "refresh": "refreshtoken"
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