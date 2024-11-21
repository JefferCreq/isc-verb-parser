from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables del entorno
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
cluster_url = os.getenv('MONGO_CLUSTER_URL')

# Construir la URI de MongoDB usando las variables del entorno
uri = f"mongodb+srv://{username}:{password}@{
    cluster_url}/test?retryWrites=true&w=majority"

# Intentar conectar a la base de datos MongoDB Atlas
try:
    client = MongoClient(uri)
    # Probar la conexión listando las bases de datos disponibles
    databases = client.list_database_names()
    print("Conexión exitosa a MongoDB Atlas. Bases de datos disponibles:", databases)
except Exception as e:
    print("Error al conectar a MongoDB Atlas:", e)
