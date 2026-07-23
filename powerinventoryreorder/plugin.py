from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin, ActionMixin


class PowerInventoryReorderPlugin(
    ActionMixin,
    SettingsMixin,
    InvenTreePlugin
):

    NAME = "Power Inventory Reorder"
    SLUG = "powerinventoryreorder"
    TITLE = "Power Inventory Reorder"

    VERSION = "1.4.0"
    AUTHOR = "Gabriel Damasceno"
    DESCRIPTION = "Daily reorder report"

    ACTION_NAME = "generate_report"

    SETTINGS = {

        "RECIPIENT_EMAIL": {
            "name": "Recipient Email",
            "description": "Email recipient for reorder reports",
            "default": "gabriel.damasceno@powersoft.com",
        },

        "REPORT_HOUR": {
            "name": "Report Time",
            "description": "Daily report time (HH:MM)",
            "default": "16:30",
        },

    }

    def perform_action(self, user=None, data=None):
        print("Power Inventory Reorder plugin action executed")

    def get_result(self, user=None, data=None):
        return {
            "success": True,
            "message": "Power Inventory Reorder plugin is working"
        }
