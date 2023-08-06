import setuptools
import os


dirname = 'bddjango'
templates_name_ls = [
    dirname + os.sep + 'templates' + os.sep + 'admin' + os.sep + 'csv_form.html',
    dirname + os.sep + 'templates' + os.sep + 'entities' + os.sep + 'mychange_list.html',
]


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name=dirname,
    version="0.0.3",
    author="bode135",
    author_email='2248270222@qq.com',   # 作者邮箱
    description="常用的django开发工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f'https://github.com/bode135/{dirname}',   # 主页链接
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas', ],      # 依赖模块
    data_files=[('', templates_name_ls)],
)
