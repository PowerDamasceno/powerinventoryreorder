from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin

from part.models import Part


class PowerInventoryReorderPlugin(
    SettingsMixin,
    InvenTreePlugin
):

    NAME = "Power Inventory Reorder"
    SLUG = "powerinventoryreorder"
    TITLE = "Power Inventory Reorder"

    VERSION = "1.6.0"
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

    def get_reorder_threshold(self, part):

        if part.minimum_stock and float(part.minimum_stock) > 0:
            return float(part.minimum_stock)

        ipn = (part.IPN or "").upper()

        if ipn.startswith("IC"):
            return 5

        if ipn.startswith("DIS"):
            return 10

        if ipn.startswith("TRS"):
            return 10

        if ipn.startswith("CON"):
            return 10

        if ipn.startswith("MOS"):
            return 10

        return 10

    def generate_report(self):

        total_parts = 0
        reorder_parts = 0

        for part in Part.objects.all():

            if not part.IPN:
                continue

            total_parts += 1

   
