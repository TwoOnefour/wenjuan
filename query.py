import requests
import json
import random
import datetime
import urllib3
import time
import os
import copy

urllib3.disable_warnings()
# with open("./query.json", "r", encoding="utf-8") as f:
#     result = json.loads(f.read())
url = "https://www.wenjuan.com/api/rspd/s/UZBZJvzGbXK/"  # 填入问卷url
my_times = 100  # 指定问卷数量
n = 1  # 指定前几个选项频繁选

if not os.path.exists(os.getcwd() + "/query.json"):
    with open("./query.json","w",encoding="utf-8") as f:
        html = requests.get(url, verify=False,headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    }).text
        html = html.split("var project = ")[1].split("var")[0].strip("\n").strip(";")
        f.write(html)
    # print(requests.get(url, verify=False,headers={         "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"     }).text)
else:
    with open("./query.json","r",encoding="utf-8") as f:
        html = f.read()
js = json.loads(html)
last_time = False
count = 0
while True:
    result = copy.deepcopy(js)
    answer = {}
    for i in result["questionpage_list"][0]["question_list"]:
        per_answer = []
        if i["question_type"] != 3:
            if not last_time:
                per_answer.append(i["option_list"][random.randint(0, min(n, len(i["option_list"]) - 1))]["_id"]["$oid"])
                answer[i["_id"]["$oid"]] = per_answer
            else:
                per_answer.append(i["option_list"][random.randint(n, len(i["option_list"]) - 1)]["_id"]["$oid"])
                answer[i["_id"]["$oid"]] = per_answer
        else:
            if 1 == len(i["option_list"]):
                loop = 1
            else:
                loop = random.randint(1, len(i["option_list"]))
            for j in range(loop):
                if not last_time:
                    last = random.randint(0, min(n, len(i["option_list"]) - 1))
                    per_answer.append([i["option_list"][last]["_id"]["$oid"]])
                    answer[i["_id"]["$oid"]] = per_answer
                    i["option_list"].pop(last)
                else:
                    if n >= len(i["option_list"]) - 1:
                        last = len(i["option_list"]) - 1
                    else:
                        last = random.randint(n, min(n, len(i["option_list"]) - 1))
                    per_answer.append([i["option_list"][last]["_id"]["$oid"]])
                    answer[i["_id"]["$oid"]] = per_answer
                    i["option_list"].pop(last)

    result = requests.post(url, json = {
        "total_answers_str": json.dumps(answer),
        "finish_status": "1",
        "timestr": str(datetime.datetime.now())[:-7],
        "idy_uuid": "",
        "project_version": 1,
        "question_captcha_map_str": "{}",
        "wx_user_info_str": "{}",
        "auto_submit_post": False,
        "question_ids_skipped_by_time": "{}",
        "appkey": "",
        "web_site": "wenjuan_web",
        "timestamp": int(time.time()*1000),
        "signature": ""
    },verify=False, headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    })
    # time.sleep(1)
    result2 = json.loads(result.text)["seq"]
    count += 1
    if count > int(my_times / 3 * 2):
        last_time = True  # 使得达到2/3的数量后改变选题策略
    if count >= my_times:
        print("已经达到指定问卷数量")
        break
