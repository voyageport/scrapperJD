import json

CABINS = open('internal_cabins.json', 'r')
CABINS = CABINS.read()
CABINS = json.loads(CABINS)

COMPLETE_JSON = {
    '3' : {}
    }