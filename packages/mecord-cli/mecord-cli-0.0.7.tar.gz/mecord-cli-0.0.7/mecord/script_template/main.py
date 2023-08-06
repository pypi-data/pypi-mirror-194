import argparse
from run import *

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--run", type=str, default=None, help=("""请求参数, JSON格式如下: 
    {
        \"task_id\": [task_id],
        \"widget_id\": [widget_id],
        \"fn_name\": \"txt2img\",
        \"param\": {"
            \"prompt\":\"sample dog\",
            \"steps\": 20,
            \"wdith\": 512,
            \"height\": 512,
    }"""))
cmd_opts = parser.parse_args()

if __name__ == '__main__':
    runTask(cmd_opts)
