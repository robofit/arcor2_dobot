from setuptools import setup, find_packages  # type: ignore

setup(
    name='arcor2_fit_demo',
    version_config={
            "template": "{tag}.dev{cc}",
            "starting_version": "0.1.0"
    },
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={"arcor2_fit_demo": ["py.typed"]},
    url='https://github.com/robofit/arcor2_fit_demo',
    license='LGPL',
    author='Robo@FIT',
    author_email='imaterna@fit.vut.cz',
    description='',
    setup_requires=['another-setuptools-git-version'],
    install_requires=[
        'arcor2>=0.8.0b6.dev*',
        'pydobot'
    ],
    zip_safe=False
)
