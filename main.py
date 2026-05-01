from storage import save_result
from graph import compiled_graph

brand = input("Nom de la marque : ",)
#result = compiled_graph.invoke({"brand": brand})
#save_result(brand=brand, result=result)

for update in compiled_graph.stream({"brand":brand}, stream_mode="updates"):
    print(update)