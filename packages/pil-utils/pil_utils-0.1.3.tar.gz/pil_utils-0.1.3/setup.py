# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pil_utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'bbcode>=1.1.0,<2.0.0',
 'fonttools>=4.0.0,<5.0.0',
 'matplotlib>=3.0.0,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'opencv-python-headless>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'pil-utils',
    'version': '0.1.3',
    'description': 'A simple PIL wrapper and text-to-image tool',
    'long_description': '## pil-utils\n\n\n### 功能\n\n- 提供 `BuildImage` 类，方便图片尺寸修改、添加文字等操作\n- 提供 `Text2Image` 类，方便实现文字转图，支持少量 `BBCode` 标签\n- 文字支持多种字体切换，能够支持 `emoji`\n- 添加文字自动调节字体大小\n\n\n### 配置字体\n\n字体文件需要安装到系统目录下\n\n默认从以下备选字体列表中查找能够显示的字体\n\n```\n"Arial", "Tahoma", "Helvetica Neue", "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Source Han Sans SC", "Noto Sans SC", "Noto Sans CJK JP", "WenQuanYi Micro Hei", "Apple Color Emoji", "Noto Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"\n```\n\n\n> 对于 `Ubuntu` 系统，建议安装 `fonts-noto` 软件包 以支持中文字体和 emoji\n>\n> 并将简体中文设置为默认语言：（否则会有部分中文显示为异体（日文）字形，详见 [ArchWiki](https://wiki.archlinux.org/title/Localization_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)/Simplified_Chinese_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E4%BF%AE%E6%AD%A3%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87%E6%98%BE%E7%A4%BA%E4%B8%BA%E5%BC%82%E4%BD%93%EF%BC%88%E6%97%A5%E6%96%87%EF%BC%89%E5%AD%97%E5%BD%A2)）\n> ```bash\n> sudo apt install fonts-noto\n> sudo locale-gen zh_CN zh_CN.UTF-8\n> sudo update-locale LC_ALL=zh_CN.UTF-8 LANG=zh_CN.UTF-8\n> fc-cache -fv\n> ```\n\n\n### 使用示例\n\n\n- `BuildImage`\n\n```python\nfrom pil_utils import BuildImage\n\n# output: BytesIO\noutput = BuildImage.new("RGBA", (200, 200), "grey").circle().draw_text((0, 0, 200, 200), "测试test😂").save_png()\n```\n\n![](https://s2.loli.net/2023/02/17/oOjw9sSbfDAJvYr.png)\n\n\n- `Text2Image`\n\n```python\nfrom pil_utils import Text2Image\n\n# img: PIL.Image.Image\nimg = Text2Image.from_text("@mnixry 🤗", 50).to_image(bg_color="white")\n```\n\n![](https://s2.loli.net/2023/02/06/aJTqGwzvsVBSO8H.png)\n\n\n- 使用 `BBCode`\n\n```python\nfrom pil_utils import text2image\n\n# img: PIL.Image.Image\nimg = text2image("N[size=40][color=red]O[/color][/size]neBo[size=40][color=blue]T[/color][/size]\\n[align=center]太强啦[/align]")\n```\n\n![](https://s2.loli.net/2023/02/06/Hfwj67QoVAatexN.png)\n\n\n目前支持的 `BBCode` 标签：\n- `[align=left|right|center][/align]`: 文字对齐方式\n- `[color=#66CCFF|red|black][/color]`: 字体颜色\n- `[stroke=#66CCFF|red|black][/stroke]`: 描边颜色\n- `[font=msyh.ttc][/font]`: 文字字体\n- `[size=30][/size]`: 文字大小\n- `[b][/b]`: 文字加粗\n\n\n### 特别感谢\n\n- [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) 基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库，非常可爱的绪山真寻bot\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MeetWq/pil-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
