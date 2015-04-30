import subprocess
import validator

from constants import Command, Option


def execute(commandName, deploymentConfigObj):
    """ Executes a command and associated tasks """
    # validate command
    validator.validateCommand(commandName)
    validator.checkIfCommandInDeploymentConfig(deploymentConfigObj, commandName, True)

    # Execute pre-tasks
    preTasks = deploymentConfigObj.getPreTasks(commandName)
    if preTasks != None:
        for task in preTasks:
            print('Executing: ' + task)
            subprocess.call(task, shell=True)

    # Execute docker command
    command = generateCommand(commandName, deploymentConfigObj)
    print('Executing: ' + command)
    subprocess.call(command, shell=True)

    # Execute post-tasks
    postTasks = deploymentConfigObj.getPostTasks(commandName)
    if postTasks != None:
        for task in postTasks:
            print('Executing: ' + task)
            subprocess.call(task, shell=True)


def generateCommand(commandName, config):
    """ Generates a command by appending relevant options to a base command """
    newCommand = 'docker ' + commandName + ' '
    for key, value in config.getOptions(commandName).items():
        # used for options like 'publish'
        if isinstance(value, list):
            for option in value:
                newCommand += Option[key].value + option + ' '
        # regular options
        else:
            newCommand += Option[key].value + str(value) + ' '

    for arg in config.getArgs(commandName):
        newCommand += arg + ' '

    return newCommand