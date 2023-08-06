import json
import sys

import codefast as cf
import ast
from rich import print


def jsonify() -> dict:
    if len(sys.argv) > 1:
        cf.info("formatting {}".format(sys.argv[1]))
        jsf = sys.argv[1]
        assert cf.io.exists(jsf), "file {} not found".format(jsf)
        js = cf.eval(cf.io.reads(jsf).lstrip().rstrip())
        cf.js.write(js, jsf + '-formated.json')
        from dofast.scripts.pyoss import Client as PyossClient
        client = PyossClient()
        url = client.upload(jsf + '-formated.json')
        from dofast.network import bitly
        url = bitly(url, printout=False)
        cf.info('online url : "{}"'.format(url))
    else:
        _stdin = sys.stdin
        x = _stdin.buffer.read().decode('utf-8')
        x = ast.literal_eval(x)
        _dict = json.dumps(x, indent=4)
        print(_dict)
