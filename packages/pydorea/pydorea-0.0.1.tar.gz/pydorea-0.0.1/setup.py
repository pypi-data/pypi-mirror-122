from setuptools import setup, find_packages

setup(
    name='pydorea',
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests==2.26.0",
        "doson4py==0.1.1"
    ],
    url='https://dorea.mrxzx.info/',
    license='MIT',
    author='ZhuoEr Liu',
    author_email='mrxzx.info@gmail.com',
    description='DoreaDB Python Driver'
)