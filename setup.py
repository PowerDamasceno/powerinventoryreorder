from setuptools import setup, find_packages

setup(
    name="powerinventoryreorder",
    version="1.2.0",
    packages=find_packages(),
    entry_points={
        "inventree_plugins": [
            "PowerInventoryReorderPlugin = powerinventoryreorder.plugin:PowerInventoryReorderPlugin"
        ]
    },
)
