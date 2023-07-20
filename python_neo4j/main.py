import json
from uuid import uuid4

import pymongo
import uvicorn
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
# CREATING NEW USERS


@app.post("/create-user")
async def create_user(body: dict):

    myuuid = uuid4()

    with neo4j_client.session() as session:
        session.run("CREATE (n:Person {id: $id, firstname: $firstname, lastname: $lastname, age: $age, birthdate: $birthdate})",
        {"id": str(myuuid), "firstname": body["firstname"], "lastname": body["lastname"],
        "age": body["age"], "birthdate": body["birthdate"]})


# GET A LIST OF ALL USERS


@app.get("/get-list-of-users")
async def get_list_of_users():

    with neo4j_client.session() as session:
        result = session.run("MATCH (n:Person) return n.id, n.firstname, n.lastname")
        return result.values()


# UPDATE A USER

@app.put("/update-user/{user_id}")
async def update_user(user_id, updated_username: dict):
    with neo4j_client.session() as session:
        session.run("MATCH (n:Person) WHERE n.id = $user_id SET n.firstname = $firstname, n.lastname = $lastname",
        {"user_id": user_id, "firstname": updated_username["firstname"], "lastname": updated_username["lastname"]})



# DELETE A USER


@app.delete("/delete-user/{user_id}")
async def delete_user(user_id):
    with neo4j_client.session() as session:
        session.run("MATCH (n:Person) WHERE n.id = $user_id DETACH DELETE n", {"user_id": user_id})


