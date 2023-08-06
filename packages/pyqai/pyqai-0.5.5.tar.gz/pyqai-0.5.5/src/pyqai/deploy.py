DEBUG = False

from platform import platform
import docker
import requests
import os
import re
import json
import argparse
import sys
from time import sleep
import logging

if DEBUG:
    import localCloudFunctions.createDeploymentService as createDeploymentService
    import localCloudFunctions.writeModels as writeModelFunction
    import localCloudFunctions.createRepo as createRepoFunction

project_name = "knuth33"
docker_artifact_repository_loc = "us-central1-docker.pkg.dev"

def printError(text):
    print(f"\033[0;31mERROR: {text}\033[00m")

def printInfo(text):
    print(f"INFO: {text}")

def printWarning(text):
    print(f"\033[0;33mWARNING: {text}\033[00m")

def buildDocker(app_folder_path):
    py_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
    docker_string = f"""FROM python:{py_version}
COPY . .

RUN pip3 install -r requirements.txt && pip3 install python-multipart && pip3 install uvicorn

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
"""
    with open(app_folder_path+ "/Dockerfile", 'w') as f:
        f.write(docker_string)

def check_string(testString):
    # NOTE: the regex for pods and for services are different.  services are more restrictive (have to start with a letter)
    # so that is the one we are using here.
    matched = re.fullmatch('[a-z]([-a-z0-9]*[a-z0-9])', testString)
    return(bool(matched))

# NOTE: requirements is an optional parameter - if you specify it, we won't make you one. Also note that if we make one it'll
# go next to your dockerfile, so make sure that the dockerfile knows where to find its requirements regardless 
def deployModel(model_name, version_name, project_directory, number_pods, requirementsFile, dockerFile, memoryLimit, verbose_logging, keep_alive):
    # TODO: consider doing this AFTER we successfully upload the model
    # TODO: look up model type 
    # TODO: return namespace name when we write it successfully

    try:
        homeDir = os.path.expanduser( '~' )
        f = open(f"{homeDir}/pyqai.config")
        configObj = json.load(f)
        api_token = configObj["api_token"]
        account_name = configObj["account_name"]
        account_id = configObj["account_id"]
    except Exception as e: 
        logging.error(e, exc_info=True)
        printError("ERROR. Unable to verify credentials; re-run pyqai-init to reset user credentials.")
        return 

#region Input Santizing
    if memoryLimit < 0.0 and memoryLimit != -999.9:
        printError(f"Error. You must provide a memory limit that is greater than 0. You provided {memoryLimit}")
        return(False)
    if(check_string(model_name)==False):
        printError("Error. The model name you provided, "+model_name+", does not match our naming convention. Please check our documentation for instructions: https://docs.pyqai.com/pyq/fundamentals/naming-conventions")
        return(False)
    if(check_string(version_name)==False):
        printError("Error. The version name you provided, "+version_name+", does not match our naming convention. Please check our documentation for instructions: https://docs.pyqai.com/pyq/fundamentals/naming-conventions")
        return(False)
#endregion

#region Authentication
    printInfo("Authenticating...")
    
    requestBodyGetToken = {"account_id": account_id}
    getToken = requests.post('https://get-deploy-credentials-fgkue36c2q-uc.a.run.app', json = requestBodyGetToken, headers={'Authorization': api_token})

    gcp_token = ''

    # TODO: maybe don't be casting args to bools?
    verbose_logging = verbose_logging == "True"

    try:
        getTokenJson = json.loads(getToken.text)
        getTokenResponse = getTokenJson["response"]

        if not DEBUG:
            gcp_token = getTokenResponse
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=json.dumps(gcp_token)
        else:
            with open("gcp_token.json", "r") as read_file:
                gcp_token = json.load(read_file)

        if(getToken.status_code != 200):
            printError(f"ERROR. Deployment failed. Authentication failed with error code: {getToken.status_code} and message: {getTokenResponse}")
            return
    except Exception as e:
        logging.error(e, exc_info=True)
        printError(f"ERROR. Deployment failed. Authentication failed with error: {getToken.text} {e}")
        return

    printInfo("Authentication successful.")
#endregion

#region Namespace creation
    requestBodyWriteModel = {"account_id": account_id, "account_name": account_name, "model_name" : model_name, "model_type" : 1}

    try:
        if not DEBUG:
            writeModels = requests.post('https://write-models-fgkue36c2q-uc.a.run.app', json = requestBodyWriteModel, headers={'Authorization': api_token})
       
            writeModelsJson = json.loads(writeModels.text)
            writeModelsResponse = writeModelsJson["response"]
            if verbose_logging : printInfo("Write models reponse: " + writeModels.text)

            model_id = writeModelsResponse

            if(writeModels.status_code != 200):
                printError(f"ERROR. Deployment failed. Attempt to create user namespace failed with error code: {writeModels.status_code} and message: {writeModelsResponse}")
                return
        else:
            writeModels = writeModelFunction.createModelTest(requestBodyWriteModel, api_token)
            model_id = writeModels[0]["response"]

        if verbose_logging : printInfo("Model id: " + str(model_id))

    except Exception as e:
        logging.error(e, exc_info=True)
        printError(f"ERROR. Deployment failed. Attempt to create user namespace failed with error: {e}")
        return
#endregion

#region Version Uniqueness check
    versionUniquenessJson = {"account_id": account_id, "model_id": model_id, "version_name": version_name}
    isUnique = requests.post('https://version-uniqueness-fgkue36c2q-uc.a.run.app', json = versionUniquenessJson, headers={'Authorization': api_token})
    if(isUnique.status_code != 200):
        isUniqueJson = json.loads(isUnique.text)
        isUniqueResponse = isUniqueJson["response"]
        printError(f"ERROR. Deployment failed. Could not ensure version name uniqueness under the model with error code: {isUnique.status_code} and message: {isUniqueResponse}")
        return(False)
    else:
        if verbose_logging : printInfo("Version name unique under model id: " + str(model_id))
#endregion

#region Dockerfile and requirements file handling
    
    if(dockerFile == "False"):
        try:
            printInfo("Building dockerfile...")
            buildDocker(project_directory)
            printInfo("Dockerfile created successfully.")
        except Exception as e:
            logging.error(e, exc_info=True)
            printError(f"ERROR. Deployment failed. Failed to create Dockerfile with error: {e}")
            return(False)

    # TODO: this will cause problems if you don't have pipreqs installed - I think we can set that as a dependency in 
    # a python package?
    # Dockerfile MUST start with FROM python:3.10

    if(requirementsFile == "False"):
        try: 
            printInfo("Building requirements.txt...")
            os.system(f'pipreqs --force {project_directory}')
            printInfo("requirements.txt created successfully")
        except Exception as e:
            logging.error(e, exc_info=True)
            printError(f"ERROR. Deployment failed. Failed to create requirements.txt with error: {e}")
            return(False)
#endregion

#region create/get user artifact registry
    # Get this users repository, if it doesn't exist this funciton will create it.
    try: 
        requestBodyCreateRepo = {"account_id": account_id}
        if not DEBUG:
            callCreateRepo = requests.post('https://create-repo-fgkue36c2q-uc.a.run.app', json = requestBodyCreateRepo, headers={'Authorization': api_token})

            json_repo = json.loads(callCreateRepo.text)
            repo_location = json_repo["response"]
            if verbose_logging : printInfo("Create repository response: " + callCreateRepo.text)

            if(callCreateRepo.status_code != 200):
                printError(f"ERROR. Deployment failed. Attempt to create artifact repository failed with error code: {callCreateRepo.status_code} and message: {repo_location}")
                return
        else:
            callCreateRepo = createRepoFunction.getRepoNameTest(requestBodyCreateRepo, api_token)
            repo_location = callCreateRepo[0]["response"]

            if verbose_logging : printInfo("Create repository response: " + repo_location)
    except Exception as e:
            logging.error(e, exc_info=True)
            printError(f"ERROR. Deployment failed. Attempt to create artifact repository failed with error: {e}")
            return
#endregion

#region docker image build 
    printInfo("Building docker image..." )
    
    try:
        # TODO: if this fails, it probably means that your docker daemon isn't running.
        # TODO: move this to get the docker client from a server, eventually
        docker_client = docker.DockerClient()
        docker_client.login(username="_json_key",password=json.dumps(gcp_token),registry=f"https://us-central1-docker.pkg.dev")
    except Exception as e:
        logging.error(e, exc_info=True)
        printError(f"ERROR. Unable to configure Docker. You may need to have the docker client running. Please install Docker Desktop, open the app on your computer and try again. If that doesn't work, contact us at team@pyqai.com. \nDeployment Failed with error: {e}")
        return

    # create and tag the docker image
    try:
        # NOTE: you have to specify the platform when building the container.  If you build on a new macbook with the ARM
        # chip, your architecture will default to ARM which will NOT work once deployed. 
        push_tag = f"{docker_artifact_repository_loc}/{project_name}/{repo_location}/{model_name}:{version_name}"
        buildOutput = docker_client.images.build(path = project_directory, rm = True, tag = push_tag, platform="linux/amd64")
        if verbose_logging : printInfo(f"Docker build output: {buildOutput}")
    except Exception as e:
        logging.error(e, exc_info=True)
        printError(f"ERROR. Deployment failed, failed build docker image with exception {e}.")
        return

    printInfo("Docker image built successfully.")
#endregion

    docker_container = docker_client.images.get(push_tag)

#region Memory Determination
    # This is the total MEMORY size of the container
    memory_size = docker_container.attrs["VirtualSize"]
    membibytes_memory_size = memory_size / 1048576
    gibibytes_memory_size = membibytes_memory_size / 1024

    if verbose_logging : printInfo(f"Docker image memory size in gibibytes: {gibibytes_memory_size}")
    auto = 0
    calculated_mem_util = 0
    size = 0

    try:
        # run the container so that we can get some stats on it.
        if(memoryLimit == -999.9): # ie the user does not provide a memory limit

            printInfo("Running docker container to determine memory requirements...")

            if verbose_logging : printInfo("Running Docker image to identify memory limit")
            docker_run = docker_client.containers.run(push_tag, detach = True, ports = {8080:8080})
            if verbose_logging : printInfo(f"Results from running docker container: {docker_run}")
            sleep(3)
            stats = docker_run.stats(decode=None, stream = False)
            if verbose_logging : printInfo("Docker container stats: " + str(stats))
            #THIS IS IN BYTES, need to convert to MiB or GiB before passing into the yaml file
            mem_usage = stats['memory_stats']['usage']
            # TODO: don't use the magic numbers here, not optimal.
            membibytes_mem_usage = mem_usage / 1048576
            gibibytes_mem_usage = membibytes_mem_usage / 1024
            if verbose_logging : printInfo(f"Docker container memory usage in gibibytes: {gibibytes_mem_usage}")
            # Still unaware what unit this is in.
            cpu_usage = stats['cpu_stats']['system_cpu_usage']
            if verbose_logging : printInfo(f"Docker container cpu_usage in unknown units: {cpu_usage}")
            docker_run.stop()

            calculated_mem_util = gibibytes_mem_usage + gibibytes_memory_size

            printInfo(f"Memory requirement determined to be {calculated_mem_util}")

        if(calculated_mem_util==0):
            size = memoryLimit
        else:
            size = calculated_mem_util
            auto = 1
    except Exception as e:
        logging.error(e, exc_info=True)
        printError(f"ERROR. We were unable to determine the memory needs of your model, getting an error {e} \nPlease try and run your container locally to make sure it works, or provide a memory limit and redeploy.")
        return

#endregion

#region Push docker container
    printInfo("Pushing docker image to artifact registry...")
    
    # TODO: this doesn't throw, annoyingly.  Sort out how to parse the output for error messages.
    try: 
        didPrint = False
        for line in docker_client.images.push(push_tag, stream=True, decode=True):
            if('status' in line):
                status = line['status']
                if(status == "Layer already exists"):
                    if(not didPrint):
                        printWarning(f"Heyo just a heads up, this image already exists in your repo. Continuing.")
                        didPrint = True
            if('errorDetail' in line):
                printError(f"ERROR. Something went wrong when trying to push the docker image, error detail: {line['errorDetail']}")
                return
    except Exception as e:
        logging.error(e, exc_info=True)
        printError(f"ERROR.Deployment failed, unable push docker image with exception {e}")
        return
    
    printInfo("Docker image pushed successfully.")
#endregion

#region create and expose workload
    printInfo("Creating and exposing kubernetes workload...")
    # here we call into the google function that will create the deployment and expose the service.
    create_service_json = {"model_name":model_name, \
    "model_id":model_id,
    "version_name":version_name,
    "num_replicas":number_pods, \
    "account_name":account_name,
    "account_id": account_id,
    "size": size,
    "keep_alive": keep_alive,
    "repo": repo_location,
    "auto": auto}

    if verbose_logging : printInfo("Create Service JSON  " + json.dumps(create_service_json))

    if not DEBUG:
        create_service = requests.post('https://create-deployment-service-fgkue36c2q-uc.a.run.app', json = create_service_json, headers={'Authorization': api_token})
        create_service_json = json.loads(create_service.text)
        create_service_response = create_service_json["response"]

        if(create_service.status_code != 200):
            printError(f"ERROR. Deployment failed. Service creation failed with code {create_service.status_code} and message: {create_service_response}")
            return(False)       
        version_id = create_service_json["version_id"]
    else:
        create_service_json = createDeploymentService.mainTest(create_service_json, api_token)
        print(create_service_json)
        version_id = create_service_json[0]["version_id"]
#endregion
    
    print(f"\033[0;32mDeployment successful. Your new version ID is {version_id}, model ID is {model_id} and account ID is {account_id}. Please refer to our documentation for instructions on how to call it: https://docs.pyqai.com/pyq/guides/calling-a-deployment \033[00m" )
    return(True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", help="The name you want to give your model", required=True)
    parser.add_argument("--version-name", help="The name you want to give this version of your model", required=True)
    parser.add_argument("--project-directory", help="The directory of your project. Put only what you need to run predictions using your model in it.", required=True)
    parser.add_argument("--number-pods", help="The number of pods of your deployment if you are providing your own", required=False, default=1)
    parser.add_argument("--keep-alive", help="How many hours the model should remain active without any usage. Anything greater than 8 hours may incur additional cost. You will experience a cold start once this time period expires. Defaults to 8", required=False, default=8, type=int)
    parser.add_argument("--requirements", help="Did you create your own requirements.txt in your project directory or should we make you one? Answer True or False. Default False.", required=False, default="False", choices=["True","False"])
    parser.add_argument("--memory-limit", help="The memory limit for your deployment in Gi if you are providing your own, else we will attempt to guess. Provide only the number with decimals.", required=False, default=-999.9, type=float)
    parser.add_argument("--dockerfile", help="Did you create your own Dockerfile in your project directory or should we make you one? Answer True or False. Default False.", required=False, default="False", choices=["True","False"])
    parser.add_argument("--verbose-logging", help="Do you want a bunch of logs? Answer True or False. Default False.", required=False, default="False", choices=["True","False"])
    
    args = parser.parse_args()
    deployModel(args.model_name, args.version_name, args.project_directory, args.number_pods, args.requirements, args.dockerfile, args.memory_limit, args.verbose_logging, args.keep_alive)