import os
import sys
from weather import get_weather, weather_schema, execute_tool_call
from groq import Groq, APIError


if os.environ.get("GROQ_API_KEY") is None :
    print('Erreur dans la clé api')
    sys.exit()


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
def ask(prompt,messages):
    messages.append({"role": "user", "content": prompt})
    try:
        message = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[weather_schema]
        )
        messages.append(message.choices[0].message)
        
        if message.choices[0].message.tool_calls:
            for tool_call in message.choices[0].message.tool_calls:
                function_response = execute_tool_call(tool_call)
                
                messages.append({
                  "role": "tool",
                  "tool_call_id": tool_call.id,
                  "name": tool_call.function.name,
                  "content": str(function_response)
                })
            final = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages
            )
            return final.choices[0].message.content, messages
        else:
            return message.choices[0].message.content, messages
    
    except APIError:
        print("erreur dans l'appel API")
        sys.exit()
    
messages = []
    
while True:
    prompt = input('ville : ', )
    out = ask(prompt, messages)
    messages = out[1]
    print(out[0])
