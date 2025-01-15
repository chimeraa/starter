
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
import os

# This Appwrite function will be executed every time your function is triggered
def main(context):
    # You can use the Appwrite SDK to interact with other services
    # For this example, we're using the Users service
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key("standard_9094aed773b56d8af3557aae5bf3dff3741bb11d78152ce195242c437ea0b35dab28a474fe341d38bbe80dd92ac48d0172e7a3135774dbba22cf50bd270162f3b6ad4f4cd79fe25637c283e5c55b3da2b28866e53f25adca5454a02de4f9964b3d9abce2a18c765898671b9c0ad962745f4740cc0fd32984e4492b7020fad8df")
    )
    users = Users(client)
    databases = Databases(client)
    try:
        response = databases.get(database_id="6729f7e30033d3541307")
        # Log messages and errors to the Appwrite Console
        # These logs won't be seen by your end users
        context.log(response)
    except AppwriteException as err:
        context.error("Could not list databases: " + repr(err))

    # The req object contains the request data
    if context.req.path == "/ping":
        # Use res object to respond with text(), json(), or binary()
        # Don't forget to return a response!
        return context.res.text("Pong")

    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
