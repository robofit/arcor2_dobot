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
    author_email='imaterna@fit.vutbr.cz',
    description='',
    setup_requires=['bad-setuptools-git-version'],
    install_requires=[
        'arcor2==0.8.0b1.*',
        'pydobot'
    ],
    zip_safe=False
)
