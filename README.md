Setup a FastAPI app with the following endpoints:

- Endpoints for creating/updating/deleting/getting list of groups


A group should be a document in MongoDB with a `name` field. All groups should have a corresponding node inside Neo4j which only has a `id` field. This field contains the `_id` field from the groups MongoDB document.

User
firstname lastname age birthdate

Role


LIKE THIS: {
    "name": "my-group-name"
}
