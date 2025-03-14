# Requirements
- Docker v.27.3.1
- Docker Compose version v2.29.7
- Git version 2.34.1
 
# Installation guide (Dev)

1. Clone repository

    `git clone https://github.com/Aarrtteemm123/Lucid-Financials.git`

2. Run the following command on the first project run to create all the necessary settings

    `docker compose up --build` or `docker-compose up --build`

App - http://localhost:8000/

# Docker Services Overview

| **Service**           | **Host**        | **Port** | **Description**                                 |
|-----------------------|-----------------|----------|-------------------------------------------------|
| **app**       | `localhost`     | `8000`   | Main application. Server handling web requests. |
| **db**       | `localhost`     | `3306`   | MySQL database for storing application data.    |
