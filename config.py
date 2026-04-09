import os
import sys
from groq import Groq

if os.environ.get("GROQ_API_KEY") is None :
    print('Erreur dans la clé api')
    sys.exit()
if os.environ.get("SERPER_API_KEY") is None :
    print('Erreur dans la clé api SERPER')
    sys.exit()
    
url = "https://google.serper.dev/search"
model = "llama-3.3-70b-versatile"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))