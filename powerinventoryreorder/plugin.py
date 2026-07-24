from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin, UserInterfaceMixin

from part.models import Part


class PowerInventoryReorderPlugin(
    SettingsMixin,
    UserInterfaceMixin,
    InvenTreePlugin
):

    NAME = "Power Inventory Reorder"
    SLUG = "powerinventoryreorder"
    TITLE = "Power Inventory Reorder"

    VERSION = "1.8.0"
    AUTHOR = "Gabriel Damasceno"
    DESCRIPTION = "Daily reorder report"

    ADMIN_SOURCE = "ui_settings.js"

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

        try:
            if part.minimum_stock and float(part.minimum_stock) > 0:
                return float(part.minimum_stock)
        except Exception:
            pass

        ipn = (part.IPN or "").upper()

        if ipn.startswith("IC"):
            return 5

        if ipn.startswith(("DIS", "TRS", "CON", "MOS")):
            return 10

        return 10

    def get_admin_context(self):

        total_parts = 0
        reorder_parts = 0

        reorder_list = []

        try:

            for part in Part.objects.all():

                if not part.IPN:
                    continue

                total_parts += 1

                try:
                    stock = float(part.total_stock or 0)
                except Exception:
                    stock = 0

                threshold = self.get_reorder_threshold(part)

                if stock <= threshold:

                    reorder_parts += 1

                    reorder_list.append({
                        "ipn": part.IPN,
                        "name": part.name,
                        "stock": stock,
                        "threshold": threshold,
                    })

            reorder_list = sorted(
                reorder_list,
                key=lambda x: x["stock"]
            )

            return {
                "status": "OK",
                "total_parts": total_parts,
                "reorder_parts": reorder_parts,
                "reorder_list": reorder_list[:50],
            }

        except Exception as exc:

            return {
                "status": f"ERROR: {exc}",
                "total_parts": 0,
                "reorder_parts": 0,
                "reorder_list": [],
            }
