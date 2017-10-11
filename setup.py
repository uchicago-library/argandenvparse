from setuptools import setup, find_packages


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="argandenvparse",
    description="A patch for argparse which gives the ArgumentParser class the ability to parse environmental variables as well",
    version="0.0.1",
    long_description=readme(),
    author="Brian Balsamo",
    author_email="brian@brianbalsamo.com",
    packages=find_packages(
        exclude=[
        ]
    ),
    include_package_data=True,
    url='https://github.com/bnbalsamo/argandenvparse',
    install_requires=[
    ],
    tests_require=[
        'pytest'
    ],
    test_suite='tests'
)
