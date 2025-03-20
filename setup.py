from setuptools import setup, find_packages

setup(
    name='wechat-bot',
    version='0.1.0',
    description='基于 wcferry 的个人微信机器人',
    long_description='personal wechat bot build by wcferry.',
    author='wenkangqiang',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.0',
        'wcferry>=1.0.0',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'wechat-bot=bot.app:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
