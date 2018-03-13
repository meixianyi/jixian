# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from config import Config
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from flask import request
import re
from modes import User
from flask import jsonify

app = Flask(__name__)


app.config.from_object(Config)
db = SQLAlchemy(app)

# 创建管理者工具对象
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
Session(app)

@app.route("/register",methods=["POST"])
def register():
    """用户注册"""
    # 接收前端返回的数据
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    username = req_dict.get('username')
    password = req_dict.get('password')

    # 校验参数
    if not all([mobile,username,password])
        resp={
            "errno":"01",
            "errmsg":"参数不完整"
        }
        return jsonify(resp)
    # 验证手机格式
    if not re.match(r"1[34578]\d{9}",mobile):
        resp = {
            "errno": "02",
            "errmsg": "手机格式不对"
        }
        return jsonify(resp)
    # 验证手机是否注册
    user = User.query.filter_by(mobile=mobile)
    if user is not None:
        resp = {
            "errno": "03",
            "errmsg": "手机已经注册"
        }
        return jsonify(resp)
    #保存用户的数据到数据库
    user = User(username=mobile,mobile=mobile,password=password)
    db.session.add(user)
    db.session.commit()



@app.route("/login", methods=["POST"])
def login():
    """登录"""
    # 获取参数、用户手机号  密码
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    # 检验参数
    if not all([mobile, password]):
        return jsonify(errno='04', errmsg="参数不完整")

    # 判断手机号格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno='05', errmsg="手机号格式不正确")

    session["user_id"] = user.id
    session["user_name"] = user.name
    session["mobile"] = user.mobile

    expire_time = 3*24*60*60

    # redis中设置过期时间
    redis_store.expire(session,expire_time)
    return jsonify(errno='00', errmsg="用户登录成功")


@app.route("/login_info", methods=["GET"])
def login_info():
    """检查登陆状态"""
    try:
    # 尝试从session中获取用户的名字
        name = session.get("user_name")
    except Exception as e:
        current_app.logger.error(e)
    else:
        mobile = session["mobile"]
        resp={
            'name' :name,
            'mobile':mobile
        }
        return jsonify(resp)


@app.route("/change_info", methods=["POST"])
def change_info():
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    username = req_dict.get('username')
    password = req_dict.get('password')

    if mobile not None:
        user = User.query.filter_by(mobile=mobile).first()
        user.password = "newpassword"
        db.session.commit()

        pass

    resp = {
        'name': '00',
        'mobile': '修改成功'
    }
    return jsonify(resp)



@api.route("/loginout", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(errno='00', errmsg="OK")







