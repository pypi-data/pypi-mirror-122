import setuptools


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="bddjango",
    version="0.0.2",
    author="bode135",
    author_email='2248270222@qq.com',   # 作者邮箱
    description="常用的django开发工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bode135/bdtools',   # 主页链接
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas', ],      # 依赖模块
)
