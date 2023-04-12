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
my_times = 30  # 指定问卷数量
n = 1  # 指定前几个选项频繁选

if not os.path.exists(os.getcwd() + "/query.json"):
    with open(os.getcwd() + "/query.json","w",encoding="utf-8") as f:
        html = requests.get(url, verify=False,headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
    }).text
        html = html.split("var project = ")[1].split("var")[0].strip("\n").strip(";")
        html = json.dumps(json.loads(html)["questionpage_list"][0]["question_list"])
        f.write(html)
    # print(requests.get(url, verify=False,headers={         "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"     }).text)
else:
    with open(os.getcwd() + "/query.json","r",encoding="utf-8") as f:
        html = f.read()
js = json.loads(html)
last_time = False
count = 0
while True:
    result = copy.deepcopy(js)
    answer = {}
    for i in result:
        per_answer = []
        if i["question_type"] != 3:
            if i["cid"][1:] == "19" or i["cid"][1:] == "2": # 指定题目
                per_answer.append(i["option_list"][random.randint(0, min(n, len(i["option_list"]) - 1))]["_id"]["$oid"])
                continue
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
                if i["cid"][1:] == "6":  # 指定题目
                    per_answer.append(i["option_list"][random.randint(0, min(n, len(i["option_list"]) - 1))]["_id"]["$oid"])
                    continue
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
        # "total_answers_str":"{\"643557a9bac485447e367943\":[\"643557a9bac485447e367941\"],\"643557f0d0af582fc9aaed65\":[\"643557f0d0af582fc9aaed63\"],\"64356581fb0723422a84d2eb\":[[\"64356581fb0723422a84d2e9\"]],\"643564b15d2f8241da591309\":[\"643564b15d2f8241da591307\"],\"643565bd5d2f8241d5932f01\":[[\"643565bd5d2f8241d5932efd\"]],\"643565bd5d2f8241d5932f02\":[[\"643565bd5d2f8241d5932eff\"]],\"643566f6bac485486f205f8e\":[[\"643566f6bac485486f205f89\"]],\"643566f9bac485486e980fbb\":[[\"643566f9bac485486e980fb9\"]],\"643567535d2f8242aeb5fb0a\":[\"64356cc0388b9d659ee7023e\"],\"643567535d2f8242aeb5fb09\":[[\"643567535d2f8242aeb5fb07\"]],\"643568fbbac485486f205f9e\":[\"64356934bac48548696a6bc7\"],\"643568febac485487211be8b\":[\"64356967d0af5833e13467f7\"],\"643568febac485487211be8c\":[\"6435699afb07234230d0c266\"],\"643568febac485487211be8d\":[\"643569b2d0af583398800fa6\"],\"643569dcbac485486df8a0d4\":[[\"64356a645d2f8241d5932faf\"]],\"643569dcbac485486df8a0d5\":[[\"64356a76d0af58339401a808\"]],\"643569dcbac485486df8a0d3\":[\"64356a8ed0af5833e1346818\"],\"643569dcbac485486df8a0d6\":[\"64356aa0d0af583399a00366\"],\"643569dffb0723422a84d346\":[\"64356aaffb0723422ecc85c3\"],\"643569dffb0723422a84d345\":[\"64356ad6bac485486f205fba\"]}",
        "finish_status": "1",
        "timestr": str(datetime.datetime.now())[:-7],
        "idy_uuid": "",
        "project_version": 1,  # 如果问卷修改了，那么要填上修改的次数，比如第一次发布就是1，修改一次就是2
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
