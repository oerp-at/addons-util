# -*- coding: utf-8 -*--
# © 2017 Funkring.net (Martin Reisenhofer <martin.reisenhofer@funkring.net>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import base64
import logging

from odoo import models
from odoo import tools

_logger = logging.getLogger(__name__)


class UtilTest(models.AbstractModel):
    _name = "util.test"

    def _testDownloadAttachments(self, obj=None, prefix=None):
        if not obj:
            obj = self

        test_download = tools.config.get("test_download")
        res = []
        if test_download:
            att_obj = obj.env["ir.attachment"]
            for att in att_obj.search([("res_model", "=", obj._model._name), ("res_id", "=", obj.id)]):
                file_name = att.datas_fname
                if prefix:
                    file_name = "%s%s" % (prefix, file_name)

                download_path = os.path.join(test_download, att.datas_fname)
                with open(download_path, "wb") as f:
                    if att.datas:
                        f.write(base64.decodestring(att.datas))

                res.append(download_path)
                _logger.info("Download %s" % download_path)

        return res
