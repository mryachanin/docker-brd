import subprocess
import validator

from constants import Command, Option


class Deployment(object):
    """ Stores the command, pre-tasks, and post-tasks for a deployment """
    def __init__(self, command, preTasks, postTasks):
        self.command = command
        self.preTasks = preTasks
        self.postTasks = postTasks

    def getCommand(self):
        return self.command

    def getPreTasks(self):
        return self.preTasks

    def getPostTasks(self):
        return self.postTasks


class Executor(object):
    def __init__(self, deploymentConfigObj):
        """ Generates deployment objects for all commands present in the deployment config """
        self.commands = {}
        self.deploymentConfigObj = deploymentConfigObj

        for key, commandEnum in Command.__members__.items():
            commandName = commandEnum.value
            if validator.checkIfCommandInDeploymentConfig(deploymentConfigObj, commandName):
                newCommand = self.generateCommand(commandName, deploymentConfigObj)
                self.commands[commandName] = Deployment(newCommand, deploymentConfigObj.getPreTasks(commandName), deploymentConfigObj.getPostTasks(commandName))


    def getValidCommands(self):
        """ Returns all commands that are present in the deployment config """
        return self.commands


    def generateCommand(self, commandName, config):
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


    def execute(self, commandName):
        """ Executes a command and associated tasks """
        # validate command
        validator.validateCommand(commandName)
        validator.checkIfCommandInDeploymentConfig(self.deploymentConfigObj, commandName, True)

        deploymentObj = self.commands[commandName]

        # Execute pre-tasks
        preTasks = deploymentObj.getPreTasks()
        if preTasks != None:
            for task in preTasks:
                print('Executing: ' + task)
                subprocess.call(task, shell=True)

        # Execute docker command
        print('Executing: ' + deploymentObj.getCommand())
        subprocess.call(deploymentObj.getCommand(), shell=True)

        # Execute post-tasks
        postTasks = deploymentObj.getPostTasks()
        if postTasks != None:
            for task in postTasks:
                print('Executing: ' + task)
                subprocess.call(task, shell=True)
