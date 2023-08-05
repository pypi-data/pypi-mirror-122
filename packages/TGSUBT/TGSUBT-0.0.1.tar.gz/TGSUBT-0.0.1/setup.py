from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TGSUBT',
    version='0.0.1',
    description='A basic package to calculate the sum of two numbers',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Taiwo Gabriel',
    license='MIT',
    author_email='omomuletaiwo@gmail.com',
    url='https://github.com/Taiwo2020/TGSUM2021',
    classifiers=classifiers,
    keyword='Mathematics',
    install_requires=['numpy','pandas'],
    packages=find_packages()

)