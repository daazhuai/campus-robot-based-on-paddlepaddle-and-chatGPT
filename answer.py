import json
import random
import requests

client_id = "Lz6NYGjOnDnKStdUNGInLjKI"
client_secret = "HFGyYsrc5WzglwOlcSQvA8oTC0PsqlRd"

def unit_chat(chat_input, user_id="user"):
    # 设置默认回复
    chat_reply = "系统繁忙，请重新尝试，谢谢配合"
	# 固定的url格式
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id, client_secret)
    res = requests.get(url)
    access_token = eval(res.text)["access_token"]
    unit_chatbot_url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + access_token
    # 拼装聊天接口对应请求
    post_data = {
                    "log_id": str(random.random()),  #登陆的id，是什么不重要，我们用随机数生成一个id即可
                    "request": {
                        "query": chat_input,  #用户输入的内容
                        "user_id": user_id  #用户id
                    },
                    "session_id": "",
                    "service_id": "S76901",  #!!!!这个很重要，必须对应我们创建的机器人的id号，id号在百度大脑中我们创建的闲聊机器人中可见
                    "version": "2.0"
                }
    # 将聊天接口对应请求数据转为json数据
    res = requests.post(url=unit_chatbot_url, json=post_data)
    # 获取聊天接口返回数据
    unit_chat_obj = json.loads(res.content)
    # 判断聊天接口返回数据是否出错(error_code == 0则表示请求正确)
    if unit_chat_obj["error_code"] != 0:
        return chat_reply
    # 解析聊天接口返回数据，找到返回文本内容 result -> response_list -> schema -> intent_confidence(>0) -> action_list -> say
    unit_chat_obj_result = unit_chat_obj["result"]
    unit_chat_response_list = unit_chat_obj_result["response_list"]
    # 随机选取一个"意图置信度"[+response_list[].schema.intent_confidence]不为0的技能作为回答
    unit_chat_response_obj = random.choice(
        [unit_chat_response for unit_chat_response in unit_chat_response_list if
         unit_chat_response["schema"]["intent_confidence"] > 0.0])
    unit_chat_response_action_list = unit_chat_response_obj["action_list"]
    unit_chat_response_action_obj = random.choice(unit_chat_response_action_list)
    unit_chat_response_say = unit_chat_response_action_obj["say"]
    return unit_chat_response_say

if __name__ == "__main__":
    while True:
        chat_input = input("请输入:")
        if chat_input == 'Bye' or chat_input == "bye":
            break
        chat_reply = unit_chat(chat_input)
        print("Unit:", chat_reply)
