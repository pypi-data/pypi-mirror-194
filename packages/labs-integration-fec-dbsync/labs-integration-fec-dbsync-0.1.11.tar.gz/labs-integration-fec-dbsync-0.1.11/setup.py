from setuptools import find_packages, setup

setup(
    name='labs-integration-fec-dbsync',
    version='0.1.11',
    include_package_data=True,
    install_requires=['cx_Oracle==6.3.1','mysql-connector'],
    packages=find_packages(),
    zip_safe=False,
    author="Kuber Mehrotra",
    author_email="kuber.mehrotra@kuliza.com",
)
