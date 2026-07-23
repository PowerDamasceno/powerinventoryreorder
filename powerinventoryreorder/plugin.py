from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin, ScheduleMixin


class PowerInventoryReorderPlugin(
    ScheduleMixin,
    SettingsMixin,
    InvenTreePlugin
):

    NAME = "Power Inventory Reorder"
    SLUG = "powerinventoryreorder"
    TITLE = "Power Inventory Reorder"

    VERSION = "1.3.0"
    AUTHOR = "Gabriel Damasceno"
    DESCRIPTION = "Daily reorder report"

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

    SCHEDULED_TASKS = {
        "reorder_test": {
            "func": "run_test",
            "schedule": "H",
        }
    }

    def run_test(self, *args, **kwargs):

        recipient = self.get_setting("RECIPIENT_EMAIL")
        report_time = self.get_setting("REPORT_HOUR")

        print(
            f"[PowerInventoryReorder] "
            f"Recipient={recipient} "
            f"ReportTime={report_time}"
        )

        return True
