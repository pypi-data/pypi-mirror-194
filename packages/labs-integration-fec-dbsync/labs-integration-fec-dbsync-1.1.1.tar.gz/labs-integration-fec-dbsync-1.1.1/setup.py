from setuptools import find_packages, setup

setup(
    name='labs-integration-fec-dbsync',
    version='1.1.1',
    include_package_data=True,
    install_requires=['cx_Oracle==6.3.1'],
    packages=find_packages(),
    zip_safe=False,
    author="Kuber Mehrotra",
    author_email="kuber.mehrotra@kuliza.com",
)
