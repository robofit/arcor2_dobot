from setuptools import setup, find_packages  # type: ignore
import arcor2_dobot

setup(
    name='arcor2_dobot',
    version=arcor2_dobot.version(),
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={"arcor2": ["py.typed"]},
    url='https://github.com/robofit/arcor2_dobot',
    download_url=f'https://github.com/robofit/arcor2_dobot/archive/{arcor2_dobot.version()}.tar.gz',
    license='LGPL',
    author='Robo@FIT',
    author_email='imaterna@fit.vutbr.cz',
    description='',
    install_requires=[
        'arcor2==0.6.*',
        'pydobot'
    ],
    zip_safe=False
)
