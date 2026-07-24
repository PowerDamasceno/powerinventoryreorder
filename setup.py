from setuptools import setup, find_packages

setup(
    name="powerinventoryreorder",
    version="2.1.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "powerinventoryreorder": [
            "static/*.js",
        ]
    },
    entry_points={
        "inventree_plugins": [
            "PowerInventoryReorderPlugin = powerinventoryreorder.plugin:PowerInventoryReorderPlugin"
        ]
    },
)
