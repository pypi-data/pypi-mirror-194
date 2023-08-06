# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvadmin-third",
    version="2.0.0",
    author="李强",
    author_email="1206709430@qq.com",
    include_package_data=True,
    description="dvadmin-third 插件是dvadmin的一个第三方用户管理插件，支持微信、企业微信、钉钉、飞书、H5页面扫码登录，支持扩展微信、企业微信、钉钉、飞书等用户信息类，以及SSO单点登录等功能(部分功能开发中)。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/huge-dream/dvadmin-third",
    packages=setuptools.find_packages(),
    python_requires='>=3.6, <4',
    install_requires=["netifaces>=0.11.0",
                      "django-redis>=5.0.0",
                      "netifaces>=0.11.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # data_files=[
    #     ('', ['./dvadmin_third/fixtures/init_menu.json', './dvadmin_third/fixtures/init_systemconfig.json']),
    # ],
    packace_data={
        '': ['*.json'],
        'fixtures': ['*.json'],
    }
)
