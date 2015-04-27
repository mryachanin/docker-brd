import subprocess

from constants import Command, Option


class Executor(object):
    def __init__(self, config):
        self.commands = {}
        self.config = config.getConfig()

        # BUILD
        if self.config[Command.BUILD.value]:
            self.generateCommand(Command.BUILD)

        # RUN
        if self.config[Command.RUN.value]:
            self.generateCommand(Command.RUN)

    def generateCommand(self, command):
        """ Generates a command by taking a base command and appending relevant options """
        self.commands[command] = 'docker ' + command.value + ' '
        for option in self.config[command.value]:
            for key in option.keys():
                try:
                    if isinstance(option[key], list):
                        for listOption in option[key]:
                            self.commands[command] += Option[key].value + listOption + ' '
                    else:
                        self.commands[command] += Option[key].value + str(option[key]) + ' '
                except:
                    print('Invalid key: ' + key)


    def execute(self, command):
        """ Takes a command enum and executes the command associated with that enum """
        print('Executing command: ' + self.commands[command])
        subprocess.call(self.commands[command], shell=True)
