from setuptools import setup

setup(
    name="base_crawler",
    version="1.0",
    description="Base Crawler",
    author="Busca Juris",
    packages=["base_crawler"],
    install_requires=[
        "beautifulsoup4",
        "capmonster_python",
        "elasticsearch",
        "log4mongo",
        "pika",
        "python-dateutil",
        "pymongo",
        "pymongo",
        "Scrapy",
        "spidermon",
        "unidecode",
    ],
)
