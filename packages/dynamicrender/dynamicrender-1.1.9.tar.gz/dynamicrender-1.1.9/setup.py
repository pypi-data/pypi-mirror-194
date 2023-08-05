# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamicrender']

package_data = \
{'': ['*']}

install_requires = \
['dynamicadaptor==0.3.7',
 'emoji>=2.2.0,<3.0.0',
 'fonttools>=4.38.0,<5.0.0',
 'httpx>=0.23.2,<0.24.0',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.24.1,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'qrcode>=7.3.1,<8.0.0']

setup_kwargs = {
    'name': 'dynamicrender',
    'version': '1.1.9',
    'description': "A package that transform bilibili's dynamic data to image",
    'long_description': '# DynamicRender\n\n用于将B站的动态渲染为图片（需要配合适配器将动态转化为特定格式）\n\n## 使用\n\n### 安装\n\n```bash\npip install dynamicrender\n```\n\n### 1. 格式化动态\n\n```python\n\n# 如果数据是grpc返回的数据\nfrom google.protobuf.json_format import MessageToDict\nfrom dynamicadaptor.DynamicConversion import formate_message\nfrom bilirpc.api import get_dy_detail\nimport asyncio\nfrom dynamicrender.Core import DyRender \n\nasync def sample1():\n    dynamic_grpc = await get_dy_detail("746530608345251842")\n    dynamic: dict = MessageToDict(dynamic_grpc[0])\n    dynamic_formate = formate_message("grpc", dynamic)\n    render = DyRender()\n    # DyRender 实例化时可以传两个参数\n    #1. data_path: {str} 为静态文件所在的位置，当data_path内不存在Static目录，则会自动解压自带的Static到data_path内\n    # 2.font_path: {str/dic}当font_path为str类型的时候必须为字体的路径，路径不存在的话会使用默认的字体\n    # 不建议使用传dict的方法修改字体\n    # 当font_path为dict的时候必须为如以下所示的dict:\n    """\n    {\n     text: str\n     extra_text: str\n     emoji: str\n    }\n    三个都必须是字体的路径，text为文本主体的字体路径，extra_text为备选字体的路径，emoji为emoji字体的路径，\n    \n    注意！！！\n    \n    每款emoji字体的字体大小都有固定值，如果修改了emoji字体必须同时修改emoji字体的字体大小\n    \n    """\n    result = await render.dyn_render(dynamic_formate)\n    result.show()\n    \nasyncio.run(sample1())\n\n\n\n# 如果是web返回的数据\n\nimport asyncio\nimport httpx\nfrom dynamicrender.Core import DyRender\nfrom dynamicadaptor.DynamicConversion import formate_message \n\nasync def sample2():\n    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/detail?timezone_offset=-480&id=746530608345251842"\n    headers = {\n        "Referer": "https://t.bilibili.com/746530608345251842"\n    }\n    result = httpx.get(url, headers=headers).json()\n    dynamic_formate = formate_message("web", result["data"]["item"])\n    render = DyRender()\n    result = await render.dyn_render(dynamic_formate)\n    result.show()\n\n\n# asyncio.run(sample2())\n\n```\n\n',
    'author': 'DMC',
    'author_email': 'lzxder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
