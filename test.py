import json
# serializing JSON / making data dump / save
# python objs ==> JSON objs



json_string = """
{
    "researcher": {
        "name": "Ford Prefect",
        "species": "Betelgeusian",
        "relatives": [
            {
                "name": "Zaphod Beeblebrox",
                "species": null
            }
        ]
    }
}
"""
# loads from JSON encoded data ==> python objects
# deserializing JSON / read
data = json.loads(json_string)
print(type(data))
print(data)