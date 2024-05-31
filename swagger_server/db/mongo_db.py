import logging

from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# create logger
LOGGER = logging.getLogger(__name__)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3").propagate = False

logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename='mongodb',
        filemode='w'
    )

# ----> console info messages require these lines <----
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(level=logging.WARNING)

# add ch to logger
LOGGER.addHandler(ch)
# -----------------------------------------------------

# Connessione a MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client["mining"]
collection_repo = db["repositories"]
collection_issues = db["issues"]
collection_prs = db["pullRequests"]
collection_workflows = db["workflows"]

#######################################################################
''' METHOD COLLECTION REPOSITORY '''

def exist_repository(key):
    result = collection_repo.find_one({"_id": key})
    return result is not None


def get_repository_by_id(key):
    return collection_repo.find_one({"_id": key})


#######################################################################

''' METHOD COLLECTION ISSUE '''

def get_repository_issues(key):
    return collection_issues.find({"_id": key})


#######################################################################

''' METHOD COLLECTION PULLREQUEST '''

def get_repository_prs(key):
    return collection_prs.find_one({"_id": key})


#############################################################

''' METHOD COLLECTION WORKFLOWS '''

def get_repository_workflow(key):
    return collection_workflows.find_one({"_id": key})


def get_repository_workflow_by_id(key, id):
    return collection_workflows.find_one({"_id": key}, {"workflows": {"$elemMatch": {"id": id}}})
