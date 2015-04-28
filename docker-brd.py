#!/usr/bin/python

import readline
import sys
import yaml
import validator

from constants import Command, Path, DeploymentConfigKey
from executor import Executor


class Config(object):
    """ Represents a config file written in yaml 

        The config files used here are all maps, 
        hence the implimentation of getConfig().
    """
    def __init__(self, configPath):
        validator.validatePath(configPath)
        configFile = open(configPath)
        self.config = yaml.load(configFile.read())
        configFile.close()
        
    def getConfig(self, key):
        """ Takes a key and returns the associated config """
        if key in self.config:
            return self.config[key]
        return None


class DeploymentConfig(Config):
    """ Represents a deployment config

        Config is expected to be in the form:
        command:
            options:
                map of options
            args:
                - list of args
            preTasks:
                - list of pre-tasks
            postTasks:
                - list of post-tasks
    """
    def __init__(self, configPath):
        super().__init__(configPath)

    def getOptions(self, command):
        if command.value in self.config and DeploymentConfigKey.OPTIONS.value in self.config[command.value]:
            return self.config[command.value][DeploymentConfigKey.OPTIONS.value]
        return None

    def getArgs(self, command):
        if command.value in self.config and DeploymentConfigKey.ARGS.value in self.config[command.value]:
            return self.config[command.value][DeploymentConfigKey.ARGS.value]
        return None

    def getPreTasks(self, command):
        if command.value in self.config and DeploymentConfigKey.PRE_TASKS.value in self.config[command.value]:
            return self.config[command.value][DeploymentConfigKey.PRE_TASKS.value]
        return None

    def getPostTasks(self, command):
        if command.value in self.config and DeploymentConfigKey.POST_TASKS.value in self.config[command.value]:
            return self.config[command.value][DeploymentConfigKey.POST_TASKS.value]
        return None


def main(args):
    # validate file containing valid docker-brd deployments
    validator.validatePath(Path.DEPLOYMENTS.value)
    deployments = Config(Path.DEPLOYMENTS.value)

    # validate args
    args = validator.validateArguments(args, deployments)

    # set up config and executor
    deploymentConfig = DeploymentConfig(args['deploymentConfigPath'])
    executor = Executor(deploymentConfig)

    # run the supplied command
    executor.execute(args['command'])


if __name__ == "__main__":
    main(sys.argv[1:])
