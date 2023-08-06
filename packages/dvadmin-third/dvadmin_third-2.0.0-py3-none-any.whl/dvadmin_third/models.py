from django.db import models

from dvadmin.system.models import Users
from dvadmin.utils.models import CoreModel

TABLE_PREFIX = 'third_'


class ThirdUsers(CoreModel):
    users = models.ForeignKey(to=Users, related_name="third_user", help_text="所属用户", verbose_name="关联用户",
                              on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    platform = models.CharField(max_length=50, default="wechat", help_text="应用平台", verbose_name="应用平台")
    open_id = models.CharField(max_length=50, help_text="open_id", verbose_name="open_id")
    union_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="union_id", help_text="union_id")
    openname = models.CharField(max_length=255, null=True, blank=True, verbose_name="用户昵称", help_text="用户昵称")

    tags = models.JSONField(verbose_name="TAG标签", help_text="用于存放用户标签(年龄段、性别、历史区域等)", null=True,
                            blank=True)
    login_ip = models.GenericIPAddressField(verbose_name="绑定ip", help_text="绑定ip", null=True, blank=True)
    latitude = models.CharField(max_length=50, help_text="绑定纬度", verbose_name="纬度", null=True, blank=True)
    longitude = models.CharField(max_length=50, help_text="绑定经度", verbose_name="经度", null=True, blank=True)
    country = models.CharField(max_length=50, help_text="绑定国家", verbose_name="绑定国家", null=True, blank=True)
    province = models.CharField(max_length=50, help_text="绑定省份", verbose_name="绑定省份", null=True, blank=True,
                                db_index=True)
    city = models.CharField(max_length=50, help_text="绑定城市", verbose_name="绑定城市", null=True, blank=True,
                            db_index=True)
    district = models.CharField(max_length=100, help_text="绑定县区", verbose_name="绑定县区", null=True, blank=True)
    address = models.CharField(max_length=200, help_text="详细地址", verbose_name="详细地址", null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="头像", help_text="头像")
    session_key = models.CharField(max_length=255, null=True, blank=True, verbose_name="session_key",
                                   help_text="session_key")

    class Meta:
        db_table = TABLE_PREFIX + "third_users"
        verbose_name = "第三方用户管理"
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
