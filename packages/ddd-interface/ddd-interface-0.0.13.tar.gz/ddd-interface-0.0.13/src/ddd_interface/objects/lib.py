import json
from base64 import b64encode, b64decode



def serialize(model):
    s = str(b64encode(model.json().encode()))
    return s[2:-1]



def deserialize(s):
    s = f"b'{s}'"
    return json.loads(b64decode(eval(s)))