import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import json_util

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables del entorno
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
cluster_url = os.getenv('MONGO_CLUSTER_URL')

# Construir la URI de MongoDB usando las variables del entorno
uri = f"mongodb+srv://{username}:{password}@{cluster_url}/"

# Obtener la ruta absoluta del directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas absolutas a los archivos JSON
verbs_data_path = os.path.join(script_dir, "../json/isc_verbs_data.json")
references_data_path = os.path.join(script_dir, "../json/isc_references.json")

# Read the data from the JSON file
df_verbs_data = pd.read_json(verbs_data_path)
df_references_data = pd.read_json(references_data_path)

# Connect to MongoDB
client = MongoClient(uri)
db = client['iskonawa_db']  # Database name
verbs_collection = db['verbs']  # Collection name
verbs_references_collection = db['references']  # Collection name

# Drop the collection if it already exists
verbs_collection.drop()
verbs_references_collection.drop()


verbs_data = df_verbs_data.to_dict(orient='records')
references_data = df_references_data.to_dict(orient='records')

# Insert the data into MongoDB
verbs_references_collection.insert_many(references_data)

# Obtener los datos de verbs_references_collection
references_data = list(verbs_references_collection.find())

# Crear diccionario de referencias id -> _id
references_dict = {}
for reference in references_data:
    references_dict[reference['id']] = reference['_id']

# Recorrer verbs_data y reemplazar el campo reference por el _id de la referencia correspondiente
for verb in verbs_data:
    verb['reference'] = references_dict[verb['reference']]
    for inflected_form in verb['inflected_forms']:
        inflected_form['reference'] = references_dict[inflected_form['reference']]


verbs_collection.insert_many(verbs_data)

print("Data inserted into MongoDB successfully!")
