import os

from application import settings

# ================================================= #
# ***************** 插件配置区开始 *******************
# ================================================= #
# 路由配置
plugins_url_patterns = [
    {"re_path": r'api/dvadmin_third/', "include": "dvadmin_third.urls"}
]
# app 配置
apps = ['dvadmin_third']
# ================================================= #
# ******************* 插件配置区结束 *****************
# ================================================= #
if not hasattr(settings, 'REDIS_URL'):
    raise Exception("请配置redis地址，否则第三方登录无法使用！")

if not hasattr(settings, 'CACHES'):
    _DEFAULT_CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f'{settings.REDIS_URL}/1',
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }
else:
    _DEFAULT_CACHES = settings.CACHES

# ********** 赋值到 settings 中 **********
settings.CACHES = _DEFAULT_CACHES
settings.INSTALLED_APPS += [app for app in apps if app not in settings.INSTALLED_APPS]
from pathlib import Path
# 添加前端模板
settings.TEMPLATES[0]["DIRS"].append(os.path.join(Path(__file__).resolve().parent, "templates"))
settings.STATICFILES_DIRS.append(os.path.join(Path(__file__).resolve().parent, "templates",  "h5", "static"))

# ********** 注册路由 **********
settings.PLUGINS_URL_PATTERNS += plugins_url_patterns


# 第三方API配置
THIRD_TYPE_CONFIG = {
    "wx": {
        # 后端启动的端口
        "port": 8000
    },

    # 微信公众号扫码登录配置
    "wx_official": {
        # 是否使用开发模式的配置，开发者模式需要另启一个uniapp的服务，在./template/dvadmin_third/目录下
        "dev": False,
        # 如果dev是True，则该键值必须填写
        "uniapp_address": "",

        # 微信公众号的appid
        "appid": "xxxxxxxxxxxxxxxxxx",

        # 微信公众号的appsecret
        "appsecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",

        # 获取微信公众号登录授权的地址（微信的）
        "api": "https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}#wechat_redirect",

        # 登录方式，snsapi_base不弹窗直接登录|snsapi_userinfo弹窗用户确认登录
        "scope": "snsapi_base",

        # 确认登录的跳转地址（自己的）
        "confirm": "http://{local_ip}/api/dvadmin_third/confirm/wx_official_confirm_login/",

        # 获取用户token的地址（微信的）
        "token_api": "https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code",

        # 获取用户信息的地址（微信的）
        "userinfo_api": "https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang={lang}",

        # 拉取用户信息的语言，zh_CN简中(默认)|zh_TW繁中|en英文
        "userinfo_lang": "zh_CN",

        # 登录后的提示跳转地址（开发时的配置，uniapp的地址）（自己的）
        "loginStatusDev": {
            "success": "http://{address}/#/pages/loginstatus/success/", # 登录成功提示地址
            "fail": "http://{address}/#/pages/loginstatus/fail/", # 登录失败提示地址
            "invalid": "http://{address}/#/pages/loginstatus/invalidcode/", # 无效二维码提示地址
            "pastdue": "http://{address}/#/pages/loginstatus/pastduecode/", # 过期二维码提示地址
            "scanned": "http://{address}/#/pages/loginstatus/scannedcode/", # 二维码已扫过提示地址
        },

        # 登录后的提示跳转地址（uniapp编译后的配置，静态文件地址）（自己的）
        "loginStatus": {
            "success": "/api/dvadmin_third/index/#/pages/loginstatus/success/", # 登录成功提示地址
            "fail": "/api/dvadmin_third/index/#/pages/loginstatus/fail/", # 登录失败提示地址
            "invalid": "/api/dvadmin_third/index/#/pages/loginstatus/invalid/", # 无效二维码提示地址
            "pastdue": "/api/dvadmin_third/index/#/pages/loginstatus/pastdue/", # 过期二维码提示地址
            "scanned": "/api/dvadmin_third/index/#/pages/loginstatus/scanned/", # 二维码已扫过提示地址
        }
    }
}
