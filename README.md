# Introduction

This exercise reflects the typical devops tasks when launching a new micro-service.  
Your are tasked with creating a docker compose based development environment and a 
initial pipeline for linting and build the project.

To be able to complete this exercise you need to setup a [bitbucket trial account](https://www.atlassian.com/software/bitbucket/bundle) and a [dockerhub account](https://hub.docker.com/signup) to be able to push and release your image. After you have created a bitbucket account and logged in you can clone this repository by clicking the 3 dots beside the Invite and Clone buttons.

References:  
[Getting started with bitbucket pipelines](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)  
[Bitbucket pipeline reference documentation](https://support.atlassian.com/bitbucket-cloud/docs/bitbucket-pipelines-configuration-reference/)  
[Docker How to containerize an application](https://docs.docker.com/get-started/02_our_app/)

# Creating a developer environment using docker and docker-compose

You are tasked with creating a docker compose based developer environment.  
The goal is that our python developer should be able to run **docker compose up** and be able to start writing beautiful code,  
while his code changes are reflected in the running container, without rebuilding or restarting the container.  
In the src/ directory you will find a small prototype application that needs to containerized and build in the pipeline.  
The same dockerFile should be used for the development environment and later used in the pipeline to build new releases.

## DockerFile

First you need to create a dockerFile that is able to run the python application using gunicorn.
The dockerFile needs to do the following:

* should have python-3.12.x available for executing the code
* should install all current and future dependencies using the provided requirements.txt, as the project grows the application developer will extend the file while the project grows.
* should be able to reflect code changes using gunicorns hot-reload feature while running in the development environment.

To execute the application using gunicorn you can use the following command in the same directory as main.py.

```bash
gunicorn --reload --access-logfile - --error-logfile - --capture-output main:app
```  

Argument explanation:

* **--reload**, enables hot reloading of code changes.
* **--access-logfile -**, sends the access log to stdout.
* **--error-logfile -**, sends the error log to stdout.
* **--capture-output -**, sends output such as print statements to stdout.
* **main:app**, main is the name of the wsgi_application and app is the name of the function to execute.

By default gunicorn will listen on port 8000 using http.

## Docker compose

You need to create a development environment using docker-compose.yml that uses the developed dockerFile
and allows hot-reloading of the code.  
Effectively you should be able to make code changes in the src/main.py file
directly from the host using your favorite editor/IDE and code changes should trigger gunicorn to hot-reload
the code changes.

Normally a full blown development environment would also include backend services such as a database, caching layer etc.

# Creating a pipeline to ensure code quality and building images

In your bitbucket project you need to create a pipeline by creating a **bitbucket-pipelines.yml**
in the root of your project that does the following:

* Whenever a **push** to **any branch** happens the code is linted using the [pycodestyle](https://pypi.org/project/pycodestyle/) package.
* Whenever a **commit/merge/push** happens to the default branch (main),
the pipeline lints the code but also runs a build and release step.  

The build step should ensure the following:

* Build the image using the developed dockerFile.
* The image should be tagged with the git commit hash as the tag.
* The following [pipeline variables](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/)
needs to be injected into the image as environment variables with the following mapping:

    * BITBUCKET_COMMIT <> app_commit
    * BITBUCKET_BRANCH <> app_branch

The release step should ensure the following

* The build image is pushed to dockerHub.
* The latest tag is updated to point to the new release on dockerHub.

If done correctly and you pull down the image and run a request against localhost:8000 or similar  
it should return the commit hash and branch name that generated the image.
