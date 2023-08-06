import mimetypes
import os
import traceback
import uuid
import socket
import urllib.parse
import hashlib
from wsgiref.util import FileWrapper

from pathlib import Path

import requests
from user_agents import parse
from django.conf import settings
from netifaces import interfaces, ifaddresses, AF_INET

from application import dispatch
from dvadmin.system.views.user import UserCreateSerializer
from dvadmin.system.models import LoginLog, Users
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.request_util import get_request_ip, get_ip_analysis, get_browser, get_os
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin_third.models import ThirdUsers
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken


class ThirdUsersSerializer(CustomModelSerializer):
    """
    第三方登录-序列化器
    """

    class Meta:
        model = ThirdUsers
        exclude = ['session_key']
        read_only_fields = ["id"]


class ThirdUsersViewSet(CustomModelViewSet):
    """
    第三方登录接口
    """
    queryset = ThirdUsers.objects.all()
    serializer_class = ThirdUsersSerializer


def static(request):
    path = os.path.join(Path(__file__).resolve().parent.parent, "templates", "h5", "static",
                        request.path_info.replace('/api/dvadmin_third/index/static/', ''))
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    return resp


def index(request):
    return render(request, 'h5/index.html')


def check_file(request, file_name):
    txt = ''
    if file_name:
        wx_check_file_list = dispatch.get_system_config_values("third.wx_check_file")
        for ele in wx_check_file_list:
            if ele.get('key') == file_name:
                txt = ele.get('value')
                break
    return HttpResponse(txt)


def get_local_ip():
    address = [
        ifaddresses(ifacename).setdefault(AF_INET, [{'addr': '127.0.0.1'}])[0]['addr']
        for ifacename in interfaces()
    ]
    print('the IP addresses of this computer has: ', address)
    for i in address:
        if i.startswith('192.168'):
            return i
    else:
        return '127.0.0.1'
    # return socket.gethostbyname(socket.gethostname())


class ThirdUsersLoginViewSet(CustomModelViewSet):
    """
    第三方登录接口
    """
    queryset = ThirdUsers.objects.all()
    serializer_class = ThirdUsersSerializer
    authentication_classes = []

    @action(methods=["GET"], detail=False, permission_classes=[])
    def scan_login_url(self, request):
        """
        获取扫码地址，一次性的，一次一个
        :param request:
        :return:
        """
        login_uid = uuid.uuid4().hex
        ip = get_request_ip(request=self.request)
        data = {
            "ip": ip,
            "browser": get_browser(request),
            "os": get_os(request)
            # "state": 1
        }
        cache.set(f"third_login_uid_{login_uid}", data, 12000)
        # 0 无效，1 未扫，2 已扫，3 扫码完成,并返回token
        cache.set(f"third_login_uid_{login_uid}_state", 1, 12000)
        url = f"api/dvadmin_third/index/#/?t=0login_uid={login_uid}"
        login_type = int(self.request.query_params.get('login_type', 0))
        local_ip = get_local_ip()
        if login_type == 0:
            # 微信扫码登录
            api_option = settings.THIRD_TYPE_CONFIG["wx"]
            url = f"http://{local_ip}:{api_option['port']}/api/dvadmin_third/index/?t={login_type}#/?login_uid={login_uid}"
        elif login_type == 1:
            # 微信公众号扫码登录
            api_option = settings.THIRD_TYPE_CONFIG["wx_official"]
            url = api_option["api"].format(
                appid=api_option["appid"],
                redirect_uri=urllib.parse.quote(api_option["confirm"].format(local_ip=local_ip).encode('utf-8')),
                # scope="snsapi_base",
                # scope="snsapi_userinfo",
                scope=api_option["scope"],
                state=login_uid
            )
        else:
            pass
        return DetailResponse(data={"url": url, "login_uid": login_uid}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[])
    def get_scan_info(self, request):
        """
        获取扫码登录页面详情，可重复查询的
        :param request:
        :return:
        """
        print('get scan info')
        login_uid = request.GET.get('login_uid')
        if not login_uid:
            return ErrorResponse(msg="无效二维码")
        login_data = cache.get(f"third_login_uid_{login_uid}")
        if not login_data:
            return ErrorResponse(msg="二维码已过期，请重新扫码")
        analysis_data = get_ip_analysis(login_data.get('ip'))
        cache.set(f"third_login_uid_{login_uid}_state", 2)
        return DetailResponse(data={"analysis_data": analysis_data, "login_data": login_data})

    @action(methods=["POST"], detail=False, permission_classes=[])
    def verify_whether_scan(self, request):
        """
        校验是否被扫，轮询的
        :param request:
        :return:
        """
        login_uid = self.request.data.get('login_uid')
        if not login_uid:
            return DetailResponse(data={"state": 0}, msg="无效二维码")
        login_state = cache.get(f"third_login_uid_{login_uid}_state")
        if not login_state:
            return DetailResponse(data={"state": 0}, msg="二维码已过期请重新扫码")
        # 如果 state == 3，进行登录，
        token = ''
        if login_state == 3:
            token = cache.get(f"third_login_uid_{login_uid}_token")
        return DetailResponse(data={"state": login_state, "token": token}, msg="获取成功")


class ConfirmLoginViewSet(CustomModelViewSet):
    """
    第三方登录接口-确认登录接口
    """
    queryset = ThirdUsers.objects.all()
    serializer_class = ThirdUsersSerializer

    @action(methods=["POST"], detail=False, permission_classes=[])
    def confirm_login(self, request):
        """
        扫码确认
        :param request:
        :return:
        """
        login_uid = self.request.data.get('login_uid')
        if not login_uid:
            return DetailResponse(data={"state": 0}, msg="无效二维码")
        login_state = cache.get(f"third_login_uid_{login_uid}_state")
        if not login_state:
            return DetailResponse(data={"state": 0}, msg="二维码已过期请重新扫码")
        if login_state == 3:
            return DetailResponse(data={"state": 3}, msg="二维码已扫过")
        cache.set(f"third_login_uid_{login_uid}_state", 3)
        # 进行颁发token，并记录登录日志
        ip = get_request_ip(request=request)
        analysis_data = get_ip_analysis(ip)
        analysis_data['username'] = request.user.username
        analysis_data['ip'] = ip
        analysis_data['agent'] = str(parse(request.META['HTTP_USER_AGENT']))
        analysis_data['browser'] = get_browser(request)
        analysis_data['os'] = get_os(request)
        analysis_data['creator_id'] = request.user.id
        analysis_data['dept_belong_id'] = getattr(request.user, 'dept_id', '')
        analysis_data['login_type'] = 2
        LoginLog.objects.create(**analysis_data)

        refresh = RefreshToken.for_user(self.request.user)
        cache.set(f"third_login_uid_{login_uid}_token", str(refresh.access_token), 20)
        return DetailResponse(msg="确认完成!")

    @action(methods=["GET"], detail=False, permission_classes=[])
    def wx_official_confirm_login(self, request):
        """
        微信公众号扫码确认
        :param request:
        :return:
        """
        code = self.request.GET.get('code')
        login_uid = self.request.GET.get('state')
        api_option = settings.THIRD_TYPE_CONFIG["wx_official"]
        login_status_url = api_option["loginStatus"]
        addr = api_option["uniapp_address"]
        if api_option["dev"]:
            login_status_url = api_option["loginStatusDev"]

        if not login_uid:
            return redirect(login_status_url["invalid"].format(address=addr))
        login_state = cache.get(f"third_login_uid_{login_uid}_state")
        if not login_state:
            return redirect(login_status_url["pastdue"].format(address=addr))
        if login_state == 3:
            return redirect(login_status_url["scanned"].format(address=addr))

        cache.set(f"third_login_uid_{login_uid}_state", 2)
        try:
            # 获取access_token
            res = requests.get(api_option["token_api"].format(
                appid=api_option["appid"],
                secret=api_option["appsecret"],
                code=code
            ))
            if res.status_code == 200:
                res_json = res.json()
                print(1, res_json)
                if 'errcode' not in res_json:
                    # 获取用户信息
                    res = requests.get(api_option["userinfo_api"].format(
                        access_token=res_json["access_token"],
                        openid=res_json["openid"],
                        lang=api_option["userinfo_lang"]
                    ))
                    if res.status_code == 200:
                        res_json = res.json()
                        print(2, res_json)
                        ip = get_request_ip(request=request)
                        analysis_data = get_ip_analysis(ip)

                        user_qs = Users.objects.filter(username=res_json["openid"])
                        if user_qs.exists():
                            # 用户已存在
                            user = user_qs.first()
                        else:
                            user_data = {
                                "username": res_json["openid"],
                                "name": res_json["nickname"].encode('iso-8859-1').decode('utf-8'),
                                "gender": res_json["sex"],
                                "password": hashlib.md5(res_json["openid"].encode(encoding="UTF-8")).hexdigest()
                            }
                            user_serializer = UserCreateSerializer(data=user_data)
                            user_serializer.is_valid(raise_exception=True)
                            user_serializer.save()
                            user = user_serializer.instance

                            thirduser_data = {
                                "users": user.id,
                                "platform": "wxofficial",
                                "open_id": res_json["openid"],
                                # "union_id": res_json["unionid"],
                                "openname": res_json["nickname"].encode('iso-8859-1').decode('utf-8'),
                                "login_ip": ip,
                                "country": res_json["country"].encode('iso-8859-1').decode('utf-8'),
                                "province": res_json["province"].encode('iso-8859-1').decode('utf-8'),
                                "city": res_json["city"].encode('iso-8859-1').decode('utf-8'),
                                "avatar_url": res_json["headimgurl"]
                            }
                            thirduser_serializer = ThirdUsersSerializer(data=thirduser_data)
                            thirduser_serializer.is_valid(raise_exception=True)
                            thirduser_serializer.save()

                        # 登录记录
                        analysis_data['username'] = user.username
                        analysis_data['ip'] = ip
                        analysis_data['agent'] = str(parse(request.META['HTTP_USER_AGENT']))
                        analysis_data['browser'] = get_browser(request)
                        analysis_data['os'] = get_os(request)
                        analysis_data['creator_id'] = user.id
                        analysis_data['dept_belong_id'] = getattr(request.user, 'dept_id', '')
                        analysis_data['login_type'] = 2
                        LoginLog.objects.create(**analysis_data)

                        # 颁发token
                        refresh = RefreshToken.for_user(user)
                        cache.set(f"third_login_uid_{login_uid}_state", 3)
                        cache.set(f"third_login_uid_{login_uid}_token", str(refresh.access_token), 20)

                        return redirect(login_status_url["success"].format(address=addr))
        except:
            print(traceback.format_exc())

        return redirect(login_status_url["fail"].format(address=addr))

