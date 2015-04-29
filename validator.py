import os
import sys

from constants import Command


def checkIfCommandInDeploymentConfig(deploymentConfigObj, commandName, assertTrue=False):
    """ Make sure the deployment config contains the command passed in """
    deploymentConfig = deploymentConfigObj.getConfig(commandName)
    if deploymentConfig == None:
        if assertTrue:
            __printUsageAndExit('No config provided for command: ' + commandName)
        return False
    return True


def validateNumArgs(args):
    """ Validates number of arguments """
    if len(args) != 2:
        __printUsageAndExit('Invalid number of arguments.')


def validateDeploymentsConfig(deploymentsConfigObj, deploymentName):
    """ Make sure a deployment config path exists in the deployments config file"""
    deploymentConfigPath = deploymentsConfigObj.getConfig(deploymentName)
    if deploymentConfigPath == None:
        __printUsageAndExit('Deployment not found: ' + deploymentName)
    return deploymentConfigPath


def validateCommand(commandName):
    """ Make sure a command name is valid """
    try:
        command = Command(commandName)
    except:
        message = 'Invalid command: ' + commandName + '.\nValid commands are: '
        for command in Command:
            message += command.value + ', '
        __printUsageAndExit(message)
    return command


def validatePath(path):
    """ Validates a system path """
    if not os.path.exists(path):
        __printUsageAndExit('Path does not exist: ' + path)


def __printUsageAndExit(message=''):
    """ Prints an optional message, usage statement, and exits with status code of 1 """
    if message != '':
        print(message)
    print('Usage: ./docker-brd  command  deployment-name')
    sys.exit(1)
