from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(name='consumer_api_telegram_bot',
    version='0.0.1',
    license='MIT License',
    author='Lucas Alves',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='lucasal072@gmail.com',
    keywords='consumer_api_lucas',
    description=u'Implementacao da api de um bot para telegram',
    packages=['consumer_api'],
    install_requires=['requests'],)