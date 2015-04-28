from enum import Enum


class Command(Enum):
    """ Represents valid commands """
    BUILD = 'build'
    RUN = 'run'


class Option(Enum):
    """ Maps options to their flag equivilent """
    tag = '--tag='
    config = '--file='
    path = ''

    name = '--name='
    detach = '--detach='
    rm = '--rm='
    publish = '--publish='
    dns = '--dns='
    image = ''


class DeploymentConfigKey(Enum):
    OPTIONS = 'options'
    ARGS = 'args'
    PRE_TASKS = 'preTasks'
    POST_TASKS = 'postTasks'

class Path(Enum):
    """ Stores system paths """
    DEPLOYMENTS = '/home/mryachanin/.config/docker-brd/deployments.yaml'
