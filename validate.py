from jsonschema import validate
import json
import sys

f = open("./dev/schema.json", "r")
schema = json.load(f)
f.close()

f = open(sys.argv[1], "r")
data = json.load(f)
f.close()

validate(data, schema)
