# Xianju-admin-service

This repository contains a admin backend service implemented using Flask framework. The service provides various endpoints to perform specific tasks and can be deployed using Docker or manually. This README file provides an introduction to the repository and instructions for deployment.



There is an implemented web-based app in xianju-admin-frontend repo. 

The service also provide APIs, see API doc for more information: https://www.apifox.cn/apidoc/shared-75b228ec-c55b-4115-84c1-9dbcdb11ed5b

## Introduction

This repository serves as a API server for Xianju App management platform.

## Feature

+ Restful
+ API version control
+ API role authentication control


## Deployment

### Default `.env` Content

```shell
DATABASE_BASE_URI=<necessery>
APP_DATABASE_BASE_URI=<necessery>
FLASK_APP=admin-service.py
FLASK_PORT=3000
SECRET_KEY='testing'
FLASK_DEBUG=1
SALT = 'SALT'
```



### Docker Deployment

> Notice: Replace labels concluded with `<>` with custom content.

To deploy the Service using Docker, follow these steps:

1. Ensure that Docker is installed on your system. You can download Docker from the official website: [https://www.docker.com](https://www.docker.com).

2. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/west2-xianju/admin-service
   ```

3. Navigate to the project directory:

   ```shell
   cd admin-service
   ```

4. Build the Docker image:

   ```shell
   docker build -t <custom-tag-name> .
   ```

5. Run the Docker container:

   ```shell
   docker run -p <outside-port>:3000 <custom-tag-name>
   ```

   The backend service will now be running on `http://localhost:<outside-port>`.

### Manual Deployment

To manually deploy the Python Flask Backend Service, follow these steps:

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/west2-xianju/admin-service
   ```

2. Navigate to the project directory:

   ```shell
   cd admin-service
   ```

3. Create a virtual environment:

   ```shell
   python -m venv env
   ```

4. Activate the virtual environment:

   - On macOS and Linux:

     ```shell
     source env/bin/activate
     ```

   - On Windows:

     ```shell
     .\env\Scripts\activate
     ```

5. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

6. Tweak configurations

   You can set `config.py` and `.env` as you want.

   In most cases, you must configurate `DATABASE_BASE_URL`  in the `.env` file to the database currently running on your machine

7. Start the backend service:

   ```shell
   python admin-service.py
   ```

   The backend service will now be running on `http://localhost:3000`(default 3000 port, you can change it in `.env` file).

## Usage

Once the backend service is deployed, you can access the API endpoints to interact with the service. Use tools like cURL, Postman, or any HTTP client library to send requests to the desired endpoints. The available endpoints and their functionality can be found in the source code or documented separately.



There is also some integrated functions you may need.

To initialize database and fill it with some forgery data, you can run 

```powershell
flask fill-db
```

To clean database

```powershell
flask clean-db
```

To run service

```powershell
python chat-service.py
```



## Contact

If you have any questions, suggestions, or feedback, please feel free to reach out to us at [zenor0@outlook.com](mailto:zenor0@outlook.com). We appreciate your interest and participation in this project.