import json
import sys

def runTask(cmd_opts):
    if (cmd_opts.run == None):
        return
    data = json.loads(cmd_opts.run)
    result = {
        "taskid" : "",
        "result" : [ 
                {
                    "type" : "image",
                    "url": [""],
                    "extention" : {
                        "info": "",
                        "cover_url": ""
                    }
                }
                
        ],
        "status" : 0,
        "message" : ""
    }
    sys.stdout.write(json.dumps(result))
