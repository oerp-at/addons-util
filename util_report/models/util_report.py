# -*- coding: utf-8 -*--
# © 2017 Funkring.net (Martin Reisenhofer <martin.reisenhofer@funkring.net>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import models, fields, api, _


class UtilReport(models.AbstractModel):
    _name = "util.report"
    _inherit = "util.file"

    def _getReportAttachment(self, report_name, obj=None):
        if not obj:
            obj = self

        report_obj = self.env["ir.actions.report.xml"]
        report = report_obj.search([("report_name", "=", report_name)], limit=1)
        if report:
            attachment_id = report_obj._get_attachment_id(report, obj)
            if attachment_id:
                return self.env["ir.attachment"].browse(attachment_id)
        return None

    def _renderReport(self, report_name, objects=None, encode=False, add_pdf_attachments=False, report_title=None):

        if not objects:
            objects = self

        cr = objects._cr
        uid = objects._uid

        report_context = dict(self._context)
        if add_pdf_attachments:
            report_context["add_pdf_attachments"] = add_pdf_attachments
        if report_title:
            report_context["report_title"] = report_title

        report_obj = self.env.registry["ir.actions.report.xml"]
        report = report_obj._lookup_report(cr, report_name)
        if report:
            values = {}
            (report_data, report_ext) = report.create(cr, uid, objects.ids, values, context=report_context)
            if len(objects.ids) > 1:
                name_first = objects[0].name_get()[0][1]
                name_last = objects[-1].name_get()[0][1]
                name = "%s-%s" % (name_first, name_last)
            else:
                name = objects.name_get()[0][1]

            name = "%s.%s" % (self._cleanFileName(name), report_ext)
            if encode:
                report_data = report_data and base64.encodestring(report_data) or None
            return (report_data, report_ext, name)
        return (None, None, None)
