from flask import Flask, render_template, request, session, redirect, jsonify
from flask_cors import CORS

from DB import Mysql
import os

import openai
openai.api_key = "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"

from answer import unit_chat

app = Flask(__name__)
# 使用session时必须设置SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(30)
CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # GET 请求，展示静态页面
    if request.method == 'GET':
        return render_template('index.html')

    # POST 处理登录逻辑
    # 获取用户名和密码
    user_name = request.json.get('username')
    password = request.json.get('password')

    sql = f'select * from message where username = "{user_name}"  and password = "{password}"'
    db = Mysql()
    db.cursor.execute(sql)
    user = db.cursor.fetchone()

    # 说明用户名或密码错误
    if user is None:
        return jsonify({"code": "0", "msg": '用户名或密码错误'})

    session['userinfo'] = user
    return jsonify({"code": "1", "msg": '注册成功'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 1 展示注册页面 GET (获取)
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # 接受表单提交过来的 账号和密码
        username = request.json.get('new_username')
        password = request.json.get('new_password')
        college = request.json.get('college')
        id_number = request.json.get('id_number')
        # 判断用户名是否已经被使用
        db = Mysql()
        sql = f'select * from message where username = "{username}"'
        db.cursor.execute(sql)
        user = db.cursor.fetchone()
        # 如果用户不为 None 说明用户名已经被使用了。
        # 需要停止程序的运行，并告诉用户
        if user is not None:
            return jsonify({"code": "0", "msg": '用户名已被注册'})

        # 拼凑 sql 语句
        sql = f'insert into message (username,password,college,id_number) values ("{username}","{password}","{college}","{id_number}")'
        # 执行 sql 语句
        add_result = db.cursor.execute(sql)
        # 保存数据库的修改
        db.conn.commit()
        if add_result > 0:
            return jsonify({"code": "1", "msg": '注册成功'})
        else:
            return jsonify({"code": "0", "msg": '注册失败'})



@app.route('/find', methods=['POST', 'GET'])
def find_back():
    if request.method == 'GET':
        return render_template('find.html')
    else:
        username = request.json.get('username')
        college = request.json.get('college')
        id_number = request.json.get('id_number')
        new_password = request.json.get('new_password')
        sql = f'select * from message where username = "{username}" and id_number = "{id_number}" and college = "{college}"'
        db = Mysql()
        db.cursor.execute(sql)
        user = db.cursor.fetchone()
        print(user)
        if user is None:
            return jsonify({"code": "0", "msg": '信息有误'})
        else:
            sql = f'UPDATE message SET password = "{new_password}" WHERE username = "{username}"'
            db.cursor.execute(sql)
            db.conn.commit()
            return jsonify({"code": "1", "msg": '修改成功'})

@app.route('/user/talk', methods=['GET','POST'])
def usr_talk():
    # 验证Cookie中携带的SessionID有效性
    # 如果有效，返回talk页面
    print("ok")
    key = session.get('userinfo')
    if (key):
        return render_template('talk.html')
    else:
        return redirect("/")

@app.route('/user/talk/answer', methods=['POST', 'GET'])
def answer():
    question = request.json.get("contest")
    print(question)
    reply_wx = unit_chat(question)
    if reply_wx == "我不知道该怎样答复您。":
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        reply_gpt = response.choices[0].text
        return reply_gpt
    else:
        return reply_wx
if __name__ == '__main__':
    app.run()
