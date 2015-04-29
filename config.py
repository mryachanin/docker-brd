import yaml
import validator

from constants import DeploymentConfigKey

class Config(object):
    """ Represents a config file written in yaml

        The config files used here are all maps,
        hence the implementation of getConfig().
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

    def getOptions(self, commandName):
        """ Returns options (optional) """
        if DeploymentConfigKey.OPTIONS.value in self.config[commandName]:
            return self.config[commandName][DeploymentConfigKey.OPTIONS.value]
        return None

    def getArgs(self, commandName):
        """ Returns args (required) """
        return self.config[commandName][DeploymentConfigKey.ARGS.value]

    def getPreTasks(self, commandName):
        """ Returns pre-tasks (optional) """
        if DeploymentConfigKey.PRE_TASKS.value in self.config[commandName]:
            return self.config[commandName][DeploymentConfigKey.PRE_TASKS.value]
        return None

    def getPostTasks(self, commandName):
        """ returns post-tasks (optional) """
        if DeploymentConfigKey.POST_TASKS.value in self.config[commandName]:
            return self.config[commandName][DeploymentConfigKey.POST_TASKS.value]
        return None