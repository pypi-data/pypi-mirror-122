# -*- coding: future_fstrings -*-
import json


def get_body(data, jsondump=True):
    if isinstance(data, list):
        if jsondump:
            out = [json.dumps(d, ensure_ascii=False).encode('utf-8') for d in data]
        else:
            out = data
        body = b'\n'.join(out)
        del out
    else:
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')

    del data
    return body
