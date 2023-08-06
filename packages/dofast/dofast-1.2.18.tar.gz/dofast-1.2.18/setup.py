import codefast as cf
import setuptools

setuptools.setup(
    name="dofast",
    version="1.2.18",  # Latest version .
    author="GaoangLiu",
    author_email="byteleap@gmail.com",
    description="A package for dirty faster Python programming.",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/slipper",
    packages=setuptools.find_packages(),
    package_data={
        setuptools.find_packages()[0]: [
            "dofast.json.zip", 'data/vps_init.sh', 'data/*.txt', 'data/*.conf',
            'pyavatar/templates/*.svg', 'pyavatar/templates/**/*.svg',
            'pyavatar/templates/**/**/*.svg'
        ]
    },
    install_requires=[
        'codefast>=0.6.4', 'fire', 'simauth', 'hashids', 'colorlog>=4.6.1', 'tqdm', 'joblib', 'PyGithub',
        'oss2', 'lxml', 'cos-python-sdk-v5', 'smart-open', 'pillow', 'bs4',
        'arrow', 'redis', 'termcolor', 'python-twitter', 'python-telegram-bot',
        'deprecation', 'faker', 'flask', 'pymysql',
        "cairosvg >= 2.3.0", 'jinja2 >= 2.9.3', 'waitress', 'celery',
        'youtube-dl', 'telegraph'
    ],
    entry_points={
        'console_scripts': [
            'sli=dofast.apps.sli:main',
            'hint=dofast.sli_entry:_hint_wubi',
            'websurf=dofast.nsq.websurf:run',
            'weather=dofast.weather:entry',
            'jsy=dofast.sli_entry:jsonify',
            'qflask=dofast.qflask:run',
            'hostoss=dofast.apps.hostoss:upload_to_oss',
            'ydd=dofast.toolkits.youdao_dict:run',
            'pcloud_upload=dofast.web.pcloud:pcloud_upload_entry',
            'setupfish=dofast.setups.fish:setup_fish',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
