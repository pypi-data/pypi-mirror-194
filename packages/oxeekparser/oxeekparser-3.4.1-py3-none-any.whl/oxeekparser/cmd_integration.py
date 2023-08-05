import os
import sys
import json
from parser import Parser

try:
    chrome_path = sys.argv[1]
    profile_path = sys.argv[2]
    sleep = int(sys.argv[3])
    url = sys.argv[4]
    in_container = True

    if len(sys.argv) > 5:
        in_container = int(sys.argv[5]) == 1 if True else False

    parser = Parser(chrome_path, profile_path, sleep=sleep, in_container=in_container)
    html = parser.handle(url).get_html()
    response_code = parser.get_response()

    result = {'html': html, 'response_code': response_code}
except:
    result = {}

os.system('cls||clear')
print(json.dumps(result))
