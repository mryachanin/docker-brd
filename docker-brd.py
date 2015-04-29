#!/usr/bin/python

import readline
import sys
import yaml
import validator

from config import Config, DeploymentConfig
from constants import Path
from executor import Executor


def main(args):
    # validate number of args
    validator.validateNumArgs(args)

    # make sure deployments config contains the specified deployment
    deploymentName = args[1]
    deploymentsConfigObj = Config(Path.DEPLOYMENTS.value)
    deploymentConfigPath = validator.validateDeploymentsConfig(deploymentsConfigObj, deploymentName)
    deploymentConfigObj = DeploymentConfig(deploymentConfigPath)

    # run the supplied command
    commandName = args[0]
    executor = Executor(deploymentConfigObj)
    executor.execute(commandName)


if __name__ == "__main__":
    main(sys.argv[1:])
