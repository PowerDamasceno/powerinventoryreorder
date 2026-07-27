import csv
from io import StringIO

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import path

from plugin import InvenTreePlugin
from plugin.mixins import (
    SettingsMixin,
    UserInterfaceMixin,
    UrlsMixin,
)

from part.models import Part


class PowerInventoryReorderPlugin(
    SettingsMixin,
    UserInterfaceMixin,
    UrlsMixin,
    InvenTreePlugin
):

    NAME = "Power Inventory Reorder"
    SLUG = "powerinventoryreorder"
    TITLE = "Power Inventory Reorder"

    VERSION = "2.2.2.1"
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

    def setup_urls(self):
        return [
            path(
                "export/",
                self.export_csv,
                name="export",
            ),
            path(
                "send-test/",
                self.send_test_email,
                name="send-test",
            ),
        ]

    def send_test_email(self, request):

        try:
            recipient = self.get_setting("RECIPIENT_EMAIL")

            if not recipient:
                return HttpResponse(
                    "REPORT EMAIL ERROR: recipient email not configured",
                    status=500
                )

            reorder_list = self.build_reorder_list()

            stock_zero = len([
                item for item in reorder_list
                if item["stock"] == 0
            ])

            critical = len([
                item for item in reorder_list
                if item["missing"] >= 5
            ])

            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)

            writer.writerow([
                "N. Riga",
                "Secondo Cod. art.",
                "Descrizione",
                "Descrizione Riga 2",
                "Quantità Ordinata",
                "UM",
                "Costo Unit.",
                "Prezzo Totale",
                "Data Rich.",
                "N. disegno tecnico",
            ])

            row_number = 1

            for item in reorder_list:
                writer.writerow([
                    row_number,
                    item["ipn"],
                    "",
                    "",
                    item["qty_to_order"],
                    "",
                    "0.01",
                    "",
                    "",
                    "",
                ])

                row_number += 1

            preview_lines = []

            for item in reorder_list[:20]:
                preview_lines.append(
                    f'- {item["ipn"]} | stock {item["stock"]} | soglia {item["threshold"]} | ordinare {item["qty_to_order"]}'
                )

            if preview_lines:
                preview_text = "\n".join(preview_lines)
            else:
                preview_text = "Nessun componente da riordinare."

            message_body = (
                "Power Inventory Reorder Report\n\n"
                f"Componenti da riordinare: {len(reorder_list)}\n"
                f"Stock zero: {stock_zero}\n"
                f"Critici: {critical}\n\n"
                "Anteprima componenti:\n"
                f"{preview_text}\n\n"
                "In allegato trovi il file CSV compatibile con il gestionale.\n"
            )

            email = EmailMessage(
                subject="Power Inventory Reorder - Report",
                body=message_body,
                from_email=None,
                to=[recipient],
            )

            email.attach(
                "reorder_report.csv",
                csv_buffer.getvalue(),
                "text/csv"
            )

            email.send(fail_silently=False)

            return HttpResponse(
                f"REPORT EMAIL SENT TO {recipient} - ITEMS: {len(reorder_list)}"
            )

        except Exception as exc:
            return HttpResponse(
                f"REPORT EMAIL ERROR: {exc}",
                status=500
            )

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

    def build_reorder_list(self):

        reorder_list = []

        for part in Part.objects.all():

            if not part.IPN:
                continue

            try:
                stock = float(part.total_stock or 0)
            except Exception:
                stock = 0

            threshold = self.get_reorder_threshold(part)

            if stock < threshold:

                missing = threshold - stock

                reorder_list.append({
                    "ipn": part.IPN,
                    "name": part.name,
                    "stock": stock,
                    "threshold": threshold,
                    "missing": missing,
                    "qty_to_order": int(missing),
                })

        reorder_list.sort(
            key=lambda x: x["missing"],
            reverse=True
        )

        return reorder_list

    def export_csv(self, request):

        reorder_list = self.build_reorder_list()

        response = HttpResponse(
            content_type="text/csv"
        )

        response[
            "Content-Disposition"
        ] = 'attachment; filename="reorder_report.csv"'

        writer = csv.writer(response)

        writer.writerow([
            "N. Riga",
            "Secondo Cod. art.",
            "Descrizione",
            "Descrizione Riga 2",
            "Quantità Ordinata",
            "UM",
            "Costo Unit.",
            "Prezzo Totale",
            "Data Rich.",
            "N. disegno tecnico",
        ])

        row_number = 1

        for item in reorder_list:

            writer.writerow([
                row_number,                  # A
                item["ipn"],                 # B
                "",                          # C
                "",                          # D
                item["qty_to_order"],        # E
                "",                          # F
                "0.01",                      # G
                "",                          # H
                "",                          # I
                "",                          # J
            ])

            row_number += 1

        return response

    def get_admin_context(self):

        try:

            reorder_list = self.build_reorder_list()

            total_parts = sum(
                1 for p in Part.objects.all()
                if p.IPN
            )

            stock_zero = len([
                x for x in reorder_list
                if x["stock"] == 0
            ])

            critical = len([
                x for x in reorder_list
                if x["missing"] >= 5
            ])

            return {
                "status": "OK",
                "total_parts": total_parts,
                "reorder_parts": len(reorder_list),
                "stock_zero": stock_zero,
                "critical": critical,
                "reorder_list": reorder_list,
            }

        except Exception as exc:

            return {
                "status": f"ERROR: {exc}",
                "total_parts": 0,
                "reorder_parts": 0,
                "stock_zero": 0,
                "critical": 0,
                "reorder_list": [],
            }
