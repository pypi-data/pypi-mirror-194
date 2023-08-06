# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['photfdtd']

package_data = \
{'': ['*']}

install_requires = \
['fdtd', 'matplotlib', 'numpy']

setup_kwargs = {
    'name': 'photfdtd',
    'version': '0.0.5',
    'description': 'PyPhot FDTD package',
    'long_description': '# PhotFDTD\n\nPhot FDTD 目前包含了基础器件和光器件的实现和测试用例，使用了fdtd库已经实现了的 Finite-difference time-domain method （时域有限差分）算法。\n\n## 基础器件\n\n1. waveguide - 直波导\n2. arc - 圆弧\n3. sbend - s波导\n4. ysplitter - y分支\n\n## 光器件\n\n光器件由基础器件组成，光器件与光器件之间也可以连接。\n\n1. directional coupler - 方向耦合器\n2. mmi - 多模耦合干涉仪\n3. ring - 微环\n\n## 安装\n\n在命令行界面输入以下命令即可\n\n```shell\npip install photfdtd\n```\n\n## Demo\n\n```python\nfrom photfdtd import Sbend\n\n\nif __name__ == "__main__":\n\n    # 设置器件参数\n    sbend = Sbend(\n        xlength=40, ylength=60, zlength=1, x=10, y=10, z=1, direction=-1, width=10, refractive_index=1.7, name="sbend"\n    )\n\n    # 设置 grid 参数\n    sbend.set_grid(grid_xlength=80, grid_ylength=80, grid_zlength=1, grid_spacing=155e-9, total_time=200, pml_width=10)\n\n    # 设置光源\n    sbend.set_source()\n\n    # 保存画好的图，设置保存位置，以及从哪一个轴俯视画图\n    sbend.savefig(filepath="SbendZ.png", axis="z")\n```\n\n### 运行结果\n\n![SbendZ](./docs/figures/SbendZ.png)\n\n## 各种光器件使用示例\n\n在 `tests` 目录下，可以看到各种光器件的使用示例，例如 `waveguide_test.py` 代表着波导的使用示例。\n\n## 开发者文档\n\n[开发者文档](docs/developer-guide.md) 提供了对于开发者的指导。',
    'author': 'Chunyu Li',
    'author_email': 'cyli0212@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/photfdtd/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
