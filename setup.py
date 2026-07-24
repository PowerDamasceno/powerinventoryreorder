from setuptools import setup, find_packages

setup(
    name="powerinventoryreorder",
    version="1.9.1",
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
