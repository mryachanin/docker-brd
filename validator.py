import os
import sys

from constants import Command


def validateArguments(args, deployments):
    """ Validates invocation arguments

        args: [command-name, deployment-name]

        return: {
            command: (Command),
            configPath: (str)
        }
    """
    # validate number of arguments
    numArgs = len(args)
    if numArgs != 2:
        __printUsageAndExit('Invalid number of arguments.')

    # validate command
    command = None
    try:
        command = Command(args[0])
    except:
        message = 'Invalid command. Valid commands are: '
        for command in Command:
            message += command.value + ', '
        __printUsageAndExit(message)

    # validate deployment config
    deploymentConfigPath = deployments.getConfig(args[1])
    if deploymentConfigPath == None:
        __printUsageAndExit('Deployment - ' + args[1] + ' - not found.')

    return {'command': command, 'deploymentConfigPath': deploymentConfigPath}


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
