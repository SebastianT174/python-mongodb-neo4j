import json

import pymongo
import uvicorn
from uuid import uuid4
from bson import ObjectId
from bson.json_util import dumps
from fastapi import FastAPI
from neo4j import GraphDatabase
from pymongo import MongoClient

app = FastAPI()

mongo_client = MongoClient("mongodb://root:password@localhost:27017/?authMechanism=DEFAULT")
neo4j_client = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# GROUPS
# CREATE A NEW GROUP


@app.post("/create-group")
async def create_group(input: dict):
    db = mongo_client["Assets"]
    collection = db["Groups"]

    result = collection.insert_one(input)

    with neo4j_client.session() as session:
        session.run("CREATE (g:Group {id: $id})", {"id": str(result.inserted_id)})


# DELETE A GROUP


@app.delete("/delete-node/{node_id}")
async def delete_node(node_id):
    db = mongo_client["Assets"]
    collection = db["Groups"]

    collection.delete_one({"_id": ObjectId(node_id)})

    with neo4j_client.session() as session:
        session.run("MATCH (n) WHERE n.id = $node_id DETACH DELETE n", {"node_id": node_id})


# GET A LIST OF ALL GROUPS

@app.get("/get-all-groups")
async def get_all_groups():
    db = mongo_client["Assets"]
    collection = db ["Groups"]

    result = collection.find()

    return json.loads(dumps(result))

# UPDATE EXISTING GROUPS


@app.put("/update-groups/{group_id}")
async def update_groups(group_id, updated_group: dict):
    db = mongo_client["Assets"]
    collection = db["Groups"]

    collection.update_one({"_id": ObjectId(group_id)}, {"$set": updated_group})



# USERS

@app.post("/create-user")
async def create_user(firstname: dict):



# Request body
# body = {
#     "first_name": "hfsiuhf",
#     "last_name": "iaushfiaf",
#     "age": 35
# }

# session.run("CREATE (n:LABEL {id: $id, first_name: $first_name, last_name: $last_name})", {**body, "id": "fakhfs"})

# node_uuid = str(uuid4())

obj = {
    "a": 1
}

obj2 = {
    "id": "id",
    **obj
}

{"id": "id", "a": 1}
