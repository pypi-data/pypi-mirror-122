from setuptools import find_packages,setup
from xes import version
setup(
    name = 'uploadlib',
    version = version.version,
    author = 'Ruoyu Wang',
    description = '上传器库，可以上传下载文件。',
    packages = find_packages(),
    install_requires = ["xes", "pypinyin", "pygame","requests"],
    url = 'https://code.xueersi.com'
)#待上传