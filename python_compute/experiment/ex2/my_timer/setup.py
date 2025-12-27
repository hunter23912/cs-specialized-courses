from setuptools import setup, find_packages
'''
该文件是一个 Python 包的配置文件，用于描述包的元信息，如包名、版本号、作者、描述、依赖等。
'''
setup(
    name="timer_decorator",                # 包名
    version="0.1.0",                       # 版本号
    author="Your Name",                    # 作者名
    author_email="your.email@example.com", # 作者邮箱
    description="A Python package with a timer decorator for measuring function execution time.",
    long_description=open("README.md").read(),  # 长描述（可以从 README 文件读取）
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/timer_decorator",  # 项目主页（可选）
    packages=find_packages(),              # 自动查找包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',               # 最低 Python 版本要求
)