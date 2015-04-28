import subprocess

from constants import Command, Option


class Deployment(object):
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
    def __init__(self, config):
        self.commands = {}

        for key, command in Command.__members__.items():
            if config.getConfig(command.value) != None:
                newCommand = self.generateCommand(command, config)
                self.commands[command] = Deployment(newCommand, config.getPreTasks(command), config.getPostTasks(command))


    def generateCommand(self, command, config):
        """ Generates a command by appending relevant options to a base command """
        newCommand = 'docker ' + command.value + ' '
        for key, value in config.getOptions(command).items():
            if isinstance(value, list):
                for option in value:
                    newCommand += Option[key].value + option + ' '
            else:
                newCommand += Option[key].value + str(value) + ' '
        
        for arg in config.getArgs(command):
            newCommand += arg + ' '

        return newCommand


    def execute(self, command):
        """ Takes a command enum and executes the command associated with that enum """
        deployment = self.commands[command]
        
        # Execute pre-tasks
        preTasks = deployment.getPreTasks()
        if preTasks != None:
            for task in preTasks:
                print('Executing: ' + task)
                subprocess.call(task, shell=True)

        # Execute docker command
        print('Executing: ' + deployment.getCommand())
        subprocess.call(deployment.getCommand(), shell=True)

        # Execute post-tasks
        postTasks = deployment.getPostTasks()
        if postTasks != None:
            for task in postTasks:
                print('Executing: ' + task)
                subprocess.call(task, shell=True)