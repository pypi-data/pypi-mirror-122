from setuptools import find_packages,setup
from xes import version
setup(
    name = 'myValues',
    version = version.version,
    author = 'Ruoyu Wang',
    author_email="wangruoyu666@outlook.com",
    description = '包含常用的许多值，为程序制作提供便利。',
    packages = find_packages(),
    install_requires = ["requests", "pypinyin", "pygame"],
    url = 'https://code.xueersi.com'
)