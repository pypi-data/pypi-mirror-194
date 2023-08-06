# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d_project']

package_data = \
{'': ['*']}

install_requires = \
['confection>=0.0.4,<0.0.5',
 'rich>=13.3.1,<14.0.0',
 'srsly>=2.4.5,<3.0.0',
 'typer>=0.7.0,<0.8.0',
 'wasabi>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['project = d_project.app:app']}

setup_kwargs = {
    'name': 'd-project',
    'version': '0.1.1',
    'description': '项目流程管理命令行工具',
    'long_description': '## 项目: d-project\n\n### 描述\n项目命令管理工具\n\n### 安装\n```\npip install d-project\n```\n### 使用\n\n首先初始化project.yml文件\n\n```\n# 默认生成当前目录\nproject init\n# 若要修改目录\nproject init ./configs/project.yml\n```\n\n运行自定义的命令或者流程\n```\nproject run some_command\n\nproject run some_workflow\n```\n\n生成READMD.md文件\n\n```\nproject document --output ./READMD.md\n```\n',
    'author': 'wangmengdi',
    'author_email': 'wangmengdi@smart-insight.com.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
