from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin


class PowerInventoryReorderPlugin(SettingsMixin, InvenTreePlugin):

    NAME = "Power Inventory Reorder"
    SLUG = "powerinventoryreorder"
    TITLE = "Power Inventory Reorder"

    VERSION = "1.1.0"
    AUTHOR = "Gabriel Damasceno"
    DESCRIPTION = "Daily reorder report"

    SETTINGS = {
        "RECIPIENT_EMAIL": {
            "name": "Recipient Email",
            "description": "Email recipient for reorder reports",
            "default": "gabriel.damasceno@powersoft.com",
        }
    }
