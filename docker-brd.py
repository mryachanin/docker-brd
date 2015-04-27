#!/usr/bin/python

import readline
import sys
import yaml
import validator

from constants import Command, Path
from executor import Executor


class Config(object):
    """ Represents a config file written in yaml  """
    def __init__(self, configPath):
        validator.validatePath(configPath)
        configFile = open(configPath)
        self.config = yaml.load(configFile.read())
        configFile.close()

    def getConfig(self):
        return self.config


def main(args):
    # validate file containing valid docker-brd deployments
    validator.validatePath(Path.DEPLOYMENTS.value)
    deployments = Config(Path.DEPLOYMENTS.value)

    # validate args
    args = validator.validateArguments(args, deployments)

    # set up config and executor
    config = Config(args['configPath'])
    executor = Executor(config)

    # run the supplied command
    executor.execute(args['command'])
    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
