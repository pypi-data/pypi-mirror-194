from setuptools import setup, find_packages
import io

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='momotou',
    version='1.0.1',
    packages=['momotou'],
    install_requires=['Pillow'],
    url='https://www.qsnctf.com/',
    package_data={'momotou': ['data/*']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='',
    author='Moxin',
    author_email='1044631097@qq.com',
    description='摸摸头表情包制作'
)
