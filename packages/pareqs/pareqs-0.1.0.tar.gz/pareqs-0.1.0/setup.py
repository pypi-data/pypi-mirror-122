from io import open
from os import environ

from setuptools import setup


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


def requirements():
    with open('requirements.txt', 'r') as req:
        return [r for r in req.read().split("\n") if r]


setup(
    name='pareqs',
    version=environ.get("CI_COMMIT_TAG", '0.0.1a66').replace('v', ''),
    packages=['pareqs', 'pareqs.models'],
    url='https://gitlab.com/whiteapfel/pareqs',
    license='Mozilla Public License 2.0',
    author='WhiteApfel',
    author_email='white@pfel.ru',
    description='Tool to decode PaReq and PaRes into handy Python objects',
    install_requires=requirements(),
    project_urls={
        "Donate": "https://pfel.cc/donate",
        "Source": "https://github.com/WhiteApfel/pyQiwiP2P",
        "Telegram": "https://t.me/apfel"
    },
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    keywords='payments 3ds threedsecure pareq pares'
)
