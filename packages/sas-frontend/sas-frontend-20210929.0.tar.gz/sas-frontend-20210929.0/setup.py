from setuptools import setup, find_packages

setup(
    name="sas-frontend",
    version="20210929.0",
    description="SmartAutomatic Server frontend",
    license="Apache-2.0",
    packages=find_packages(include=["sas_frontend", "sas_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
