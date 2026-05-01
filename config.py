import os
import sys
from groq import Groq
import chromadb
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("GROQ_API_KEY") is None :
    print(os.environ.get("GROQ_API_KEY"))
    print('Erreur dans la clé api GROQ')
    sys.exit()
if os.environ.get("SERPER_API_KEY") is None :
    print('Erreur dans la clé api SERPER')
    sys.exit()
    
url = "https://google.serper.dev/search"
model = "llama-3.1-8b-instant"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient("./chroma_db")

collection = chroma_client.get_or_create_collection(
	name="MyCollection",
)
