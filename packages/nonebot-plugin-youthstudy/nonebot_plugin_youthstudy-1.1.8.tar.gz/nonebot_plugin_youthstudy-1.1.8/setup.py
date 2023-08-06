# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_youthstudy', 'nonebot_plugin_youthstudy.dao']

package_data = \
{'': ['*'], 'nonebot_plugin_youthstudy': ['resource/bac/*', 'resource/font/*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'httpx>=0.23.0,<0.24.0',
 'lxml>=4.7,<5.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot-plugin-apscheduler>=0.2.0,<0.3.0',
 'nonebot2>=2.0.0b2']

setup_kwargs = {
    'name': 'nonebot-plugin-youthstudy',
    'version': '1.1.8',
    'description': '基于nonebot2的青年大学习插件',
    'long_description': '<div align="center">\n    <img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>\n    <h1>nonebot_plugin_youthstudy</h1>\n    <b>✨基于nonebot2的青年大学习插件，用于获取最新一期青年大学习答案✨</b>\n    <br/>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>\n</div>\n\n\n## 安装\n\n```bash\nnb plugin install nonebot_plugin_youthstudy\n```\n或者\n```bash\npip install nonebot_plugin_youthstudy\n```\n\n## 更新\n\n```bash\nnb plugin update nonebot_plugin_youthstudy\n```\n或者\n```bash\npip install nonebot_plugin_youthstudy -U\n```\n\n### 导入插件\n- 在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["nonebot_plugin_youthstudy"]`\n\n**注**：如果你使用`nb`安装插件，则不需要设置此项\n\n### 添加配置\n\n- 运行一遍bot，然后关闭\n\n- 在bot目录的data目录下修改`study_config.json`文件，添加如下配置：\n\n    - `"SUPER_USERS": ["超级用户qq号"]`\n\n### 正式使用\n\n| 命令                    | 举例               | 说明                                                         |\n| ----------------------- | ------------------ | ------------------------------------------------------------ |\n| 青年大学习/大学习       | 青年大学习         | 获取大学习答案                                               |\n| 开启/关闭大学习推送     | 开启大学习推送     | 在群聊中仅有超级用户能开启推送，私聊任何人都能开启推送，但需要加好友 |\n| 开启/关闭大学习全局推送 | 关闭大学习全局推送 | 关闭全局推送后，所有的群聊、私聊推送任务都会关闭，仅超级用户使用 |\n| 同意/拒绝+qq号          | 同意1234567        | 处理好友请求，仅超级用户使用                                 |\n| 同意/拒绝所有好友请求   | 拒绝所有好友请求   | 拒绝所有的好友请求，仅超级用户使用                           |\n| 大学习截图              | 大学习截图         | 获取主页截图                                                 |\n| 完成截图                | 完成截图           | 获取大学习完成截图                                           |\n| 大学习帮助              | 大学习帮助         | 获取命令列表                                                 |\n\n### TODO\n\n- [ ] 优化机器人\n\n## 更新日志\n\n### 2022/9/26\n\n- 修改异常抓取位置\n\n### 2022/9/19\n\n- 增加异常抓取\n\n### 2022/9/12\n\n- 修复获取答案失败的bug\n\n### 2022/9/8\n\n- 修复无法获取截图的bug\n\n### 2022/6/17\n\n- 修复bug，降低python版本要求为>=3.8\n\n### 2022/5/7\n\n- 代码重构\n\n### 2022/4/24\n\n- 支持对机器人发送口令开关定时推送功能\n- 支持对机器人发指令设置推送相关好友/群聊\n\n### 2022/4/18\n\n- 支持自动获取青年大学习完成截图功能。如果您所在学校会查后台观看记录，请前往相应平台观看1分钟，确保留下观看记录！\n\n### 2022/4/17\n\n- 支持通过检查更新自动提醒完成青年大学习，请参照机器人配置进行配置\n\n### 2022/3/5\n\n- 支持nonebot[v2.0.0-beta2]，请更新至最新版nonebot使用\n\n',
    'author': 'ayanamiblhx',
    'author_email': '1196818079@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ayanamiblhx/nonebot_plugin_youthstudy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
