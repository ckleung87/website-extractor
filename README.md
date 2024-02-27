# Website Extractor
An application to extract html content recursively

## Techology
* Beautifulsoup

## Deployment
* Docker
* Kubernetes
* CI/CD (gitLab)

## Local Development Env Setup

### 1. Install python dependency package
Create python3 virtualenv at project root
```
# <project_root>/
virtualenv -p python3 VENV
```

Use virtualenv
```
# <project_root>/
source ./VENV/bin/activate
```

### 2. Create .env config
Create .env config in project root
```
# <project_root>/
cp ./env/example.env ./src/.env 
```

Modifiy .env config
| Parmemeter  | Description | Default|
| ------------- |:-------------:|:-------------:|
|LOG_LEVEL|Logging level|INFO|
|WEBSITE_URL|Website url||
|RECURSIVE_LEVEL_LIMIT|Website extraction depth|0|
|EXTRACT_PAGE_SLEEP_SEC|Sleep interval per extraction|0.2|
```
ENV=DEV
SERVICE_NAME=WEBSITE-EXTRACTOR
LOG_LEVEL=INFO
WEBSITE_URL=<website_url>
RECURSIVE_LEVEL_LIMIT=0
EXTRACT_PAGE_SLEEP_SEC=0.2
```

### 3. Run Test
```
# <project_root>/
source ./VENV/bin/activate
cd src
python tests.py
```

### 4. Run Application
Ouput log is in contents/app.log
```
# <project_root>/
source ./VENV/bin/activate
cd src
python app.py
```

## Run Service with Docker Compose

### 1. Create Contents dir
```
# <project_root>/
mkdir contents
```

### 2. Update docker-compose config
| Parmemeter  | Description | Default|
| ------------- |:-------------:|:-------------:|
|LOG_LEVEL|Logging level|INFO|
|WEBSITE_URL|Website url||
|RECURSIVE_LEVEL_LIMIT|Website extraction depth|0|
|EXTRACT_PAGE_SLEEP_SEC|Sleep interval per extraction|0.2|

### 3. Execute
```
# <project_root>/
docker-compose -f docker-compose.yml up -d --force-recreate --build
```

# Logging
Application logs are written into /contents folder

# CI/CD
An gitLab config example is provided in .gitlab-ci.yml It consist 3 stages
* test
* build
* deploy

## Test
Run python unit test

## Build
Build backed service as a docker image with amd64 and arm64 architecture and then upload to docker repo (e.g. AWS ECR)

## Deploy 
Deploy the docker image.
* AWS ECS
* Kubernetes

### AWS ECS

1. Create ECS cluster and service in AWS
2. Create ECS Task Definition Template
3. In Extractor deploy stage, create the latest ECS Task Definition by the template
4. Push the Latest ECS Task Definition to AWS
5. Update the ECS Service Task Definition Version

### Kubernetes

1. Create a seperate infra git repo. 
2. In Extractor deploy stage, checkout the infra repo, update the image version in the helm template config.
3. Push the changes
4. CI/CD of infra repo will execute helm update to deploy the latest version to the cluster

## Run Service with Kubernetes
Document is in /k8s/README.md