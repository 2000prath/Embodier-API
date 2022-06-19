from email.mime import base
from sre_constants import SUCCESS
from xmlrpc.client import Boolean, boolean

import json


class Response:
    data: list = []
    success: Boolean
    message: str
    
    def json(self, success:bool, message:str='', base64:str='') -> dict:
        result = {
            "success": success,
            "message": message
        }
        if base64: result['base64'] = base64
        return json.dumps(result)
        