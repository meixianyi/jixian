import redis
import nginx

class Config(object):
    DEGUG =True
    SQLALCHEMY_DATABASE_URI= 'mysql://root:mysql@127.0.0.1:3306/Flask_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = '6379'

    # session
    SESSION_TYPE = "redis"  # 保存到redis中


# 打开nginx.conf文件
"""location{
   include  uwsgi_params,
   usgi_pass 127.0.0.1:8080
}"""
