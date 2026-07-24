from setuptools import setup, find_packages

setup(
    name="powerinventoryreorder",
    versionackage_data={
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
