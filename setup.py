from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='yaftp-ui',
    version='0.0.1',
    description='User Interface of Yet Another File Transfer Protocol',
    long_description=readme,
    author='Weiwen Chen',
    author_email='17307110121@fudan.edu.cn',
    url='https://github.com/ofey404/yaftp-ui',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)