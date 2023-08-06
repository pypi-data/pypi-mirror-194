# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxxl', 'pyxxl.logger', 'pyxxl.tests', 'pyxxl.tests.api']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0', 'aiohttp>=3.8.1,<4.0.0']

extras_require = \
{'all': ['redis>=4.4.0,<5.0.0', 'python-dotenv'],
 'dotenv': ['python-dotenv'],
 'redis': ['redis>=4.4.0,<5.0.0']}

setup_kwargs = {
    'name': 'pyxxl',
    'version': '0.3.0a2',
    'description': 'A Python executor for XXL-jobs',
    'long_description': '# xxl-jobs 的python客户端实现\n\n<p align="center">\n<a href="https://pypi.org/project/pyxxl" target="_blank">\n    <img src="https://img.shields.io/pypi/v/pyxxl?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/pyxxl" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/pyxxl.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n<a href="https://pypi.org/project/pyxxl" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/fcfangcc/pyxxl?color=%2334D058" alt="Coverage">\n</a>\n</p>\n\n使用pyxxl可以方便的把Python写的方法注册到[XXL-JOB](https://github.com/xuxueli/xxl-job)中,使用XXL-JOB-ADMIN管理Python定时任务和周期任务\n\n实现原理：通过XXL-JOB提供的RESTful API接口进行对接\n\n<font color="#dd0000">注意！！！如果用同步的方法，极端情况下会卡住主线程。如果无法全异步编程的，谨慎使用本仓库。</font>\n\n## 已经支持的功能\n\n* 执行器注册到job-admin\n* task注册，类似于flask路由装饰器的用法\n* 任务的管理（支持在界面上取消，发起等操作，任务完成后会回调admin）\n* 所有阻塞策略的支持\n* 异步支持（推荐）\n* job-admin上查看日志\n\n## 适配的XXL-JOB版本\n\n* XXL-JOB:2.3.0\n\n如遇到不兼容的情况请issue告诉我XXL-JOB版本我会尽量适配\n\n## 如何使用\n\n```shell\npip install pyxxl\n# 如果日志需要写入redis\npip install pyxxl[redis]\n# 如果需要从.env加载配置\npip install pyxxl[dotenv]\n# 安装所有功能\npip install pyxxl[all]\n```\n\n```python\nimport asyncio\n\nfrom pyxxl import ExecutorConfig, PyxxlRunner\n\nconfig = ExecutorConfig(\n    xxl_admin_baseurl="http://localhost:8080/xxl-job-admin/api/",\n    executor_app_name="xxl-job-executor-sample",\n    executor_host="172.17.0.1",\n)\n\napp = PyxxlRunner(config)\n\n@app.handler.register(name="demoJobHandler")\nasync def test_task():\n    await asyncio.sleep(5)\n    return "成功..."\n\n# 如果你代码里面没有实现全异步，请使用同步函数，不然会阻塞其他任务\n@app.handler.register(name="xxxxx")\ndef test_task3():\n    return "成功3"\n\n\napp.run_executor()\n```\n\n\n更多示例和接口文档请参考 [PYXXL文档](https://fcfangcc.github.io/pyxxl/example/) ，具体代码在example文件夹下面\n\n\n## 开发人员\n下面是开发人员如何快捷的搭建开发调试环境\n\n### 启动xxl的调度中心\n\n```shell\n./init_dev_env.sh\n```\n\n\n### 启动执行器\n\n\n```shell\n# if you need. set venv in project.\n# poetry config virtualenvs.in-project true\npoetry install --all-extras\n# 修改app.py中相关的配置信息,然后启动\npoetry run python example/app.py\n```\n',
    'author': 'fcfangcc',
    'author_email': 'swjfc22@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fcfangcc/pyxxl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
