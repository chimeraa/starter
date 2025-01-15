import json

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
    databases = Databases(client)
    database_id = "6729f7e30033d3541307"  # ID del database

    try:
        # Decodifica del corpo della richiesta
        try:
            body = json.loads(context.req.body) if context.req.body else {}
        except json.JSONDecodeError:
            return context.res.json({"error": "Il corpo della richiesta non è un JSON valido."}, status=400)

        if context.req.path == "/":
            # Recupera i documenti dalla collection
            collection_id = body.get("collection_id")

            if not collection_id:
                return context.res.json({"error": "collection_id è obbligatorio."}, status=400)

            documents = databases.list_documents(database_id=database_id, collection_id=collection_id)
            return context.res.json({"documents": documents})

        elif context.req.path.startswith("/update/"):
            # Estrae l'ID della collection dall'URL
            collection_id = context.req.path.split("/update/")[1]

            # Estrae i dati dal corpo della richiesta
            document_id = body.get("document_id")
            field_name = body.get("field_name")
            new_value = body.get("new_value")

            if not document_id or not field_name or new_value is None:
                return context.res.json(
                    {"error": "document_id, field_name e new_value sono obbligatori."},
                    status=400,
                )

            # Aggiorna il documento
            updated_data = {field_name: new_value}
            response = databases.update_document(
                database_id=database_id,
                collection_id=collection_id,
                document_id=document_id,
                data=updated_data
            )
            return context.res.json({"message": "Documento aggiornato con successo!", "response": response})

        else:
            return context.res.json({"message": "Endpoint non valido."}, status=404)

    except AppwriteException as err:
        return context.res.json({"error": repr(err)}, status=500)