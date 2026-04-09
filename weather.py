import json
# def d'une fonction fictive pour récupérer la météo

def get_weather(city):
    # ici on simule une réponse de l'API météo
    return f"La météo à {city} est nuageuse avec une température de 25°C."

# Tool schema pour cette fonction

weather_schema = {
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the current weather for a given city",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "The name of the city to get the weather for"
        }
      },
      "required": ["city"]
    }
  }
}

available_function = {
    "get_weather" : get_weather
}

def execute_tool_call(tool_call) :
    """Parse and execute a single tool call"""
    function_name = tool_call.function.name 
    function_to_call = available_function[function_name]
    function_args = json.loads(tool_call.function.arguments)
    
    return function_to_call(**function_args)
