import json

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import os


# Questa funzione Appwrite verrà eseguita ogni volta che la funzione è attivata
def main(context):
    # Crea il client per interagire con Appwrite
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(
            "standard_9094aed773b56d8af3557aae5bf3dff3741bb11d78152ce195242c437ea0b35dab28a474fe341d38bbe80dd92ac48d0172e7a3135774dbba22cf50bd270162f3b6ad4f4cd79fe25637c283e5c55b3da2b28866e53f25adca5454a02de4f9964b3d9abce2a18c765898671b9c0ad962745f4740cc0fd32984e4492b7020fad8df")
    )
    databases = Databases(client)
    database_id = "6729f7e30033d3541307"  # ID del database

    try:
        # Decodifica del corpo della richiesta
        try:
            body = json.loads(context.req.body) if context.req.body else {}
        except json.JSONDecodeError:
            context.log({"error": "Il corpo della richiesta non è un JSON valido."})
            return context.res.json({"error": "Il corpo della richiesta non è un JSON valido."}, status=400)

        # Se la richiesta è per l'endpoint "/"
        if context.req.path == "/":
            collection_id = body.get("collection_id")

            if not collection_id:
                context.log({"error": "collection_id è obbligatorio."})
                return context.res.json({"error": "collection_id è obbligatorio."}, status=400)

            # Recupera i documenti dalla collection
            try:
                documents = databases.list_documents(database_id=database_id, collection_id=collection_id)
                context.log({"action": "list_documents", "collection_id": collection_id,
                             "documents_count": len(documents["documents"])})
                return context.res.json({"documents": documents["documents"]})
            except AppwriteException as err:
                context.log({"error": f"Errore nel recupero dei documenti: {repr(err)}"})
                return context.res.json({"error": "Errore nel recupero dei documenti."}, status=500)

        # Se la richiesta è per l'endpoint "/update/<id>"
        elif context.req.path.startswith("/update/"):
            collection_id = context.req.path.split("/update/")[1]
            document_id = body.get("document_id")
            field_name = body.get("field_name")
            new_value = body.get("new_value")

            # Verifica che i dati obbligatori siano presenti
            if not document_id or not field_name or new_value is None:
                context.log({"error": "document_id, field_name e new_value sono obbligatori."})
                return context.res.json({"error": "document_id, field_name e new_value sono obbligatori."}, status=400)

            try:
                # Aggiorna il documento
                updated_data = {field_name: new_value}
                response = databases.update_document(
                    database_id=database_id,
                    collection_id=collection_id,
                    document_id=document_id,
                    data=updated_data
                )
                context.log({"action": "update_document", "collection_id": collection_id, "document_id": document_id,
                             "updated_data": updated_data})
                return context.res.json({"message": "Documento aggiornato con successo!", "response": response})
            except AppwriteException as err:
                context.log({"error": f"Errore nell'aggiornamento del documento: {repr(err)}"})
                return context.res.json({"error": "Errore nell'aggiornamento del documento."}, status=500)

        # Se la richiesta è per l'endpoint "/create"
        elif context.req.path == "/create":
            collection_id = body.get("collection_id")
            document_data = body.get("document_data")

            if not collection_id or not document_data:
                context.log({"error": "collection_id e document_data sono obbligatori."})
                return context.res.json({"error": "collection_id e document_data sono obbligatori."}, status=400)

            try:
                # Crea un nuovo documento
                response = databases.create_document(
                    database_id=database_id,
                    collection_id=collection_id,
                    document_id="unique()",  # Genera un ID univoco per il documento
                    data=document_data
                )
                context.log({"action": "create_document", "collection_id": collection_id, "document_data": document_data})
                return context.res.json({"message": "Documento creato con successo!", "response": response})
            except AppwriteException as err:
                context.log({"error": f"Errore nella creazione del documento: {repr(err)}"})
                return context.res.json({"error": "Errore nella creazione del documento."}, status=500)

        # Endpoint non valido
        else:
            context.log({"error": "Endpoint non valido."})
            return context.res.json({"message": "Endpoint non valido."}, status=404)

    except AppwriteException as err:
        context.log({"error": f"Errore generico: {repr(err)}"})
        return context.res.json({"error": repr(err)}, status=500)

    # Risposta predefinita se nessuna delle condizioni viene soddisfatta
    context.log({"error": "Nessuna risposta definita per questa richiesta."})
    return context.res.json({"error": "Endpoint non definito"}, status=404)
