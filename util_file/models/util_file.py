# -*- coding: utf-8 -*--
# © 2017 Funkring.net (Martin Reisenhofer <martin.reisenhofer@funkring.net>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
import os
import sys
import base64

from odoo import models
from odoo import tools


class UtilFile(models.AbstractModel):
    _name = "util.file"
    _repl_name = (
        ("Ö", "Oe"),
        ("Ü", "Ue"),
        ("Ä", "Ae"),
        ("ö", "oe"),
        ("ü", "ue"),
        ("ä", "ae"),
        (", ", "_"),
        (" ", "_"),
        ("_-_", "-"),
        ("_-", "-"),
        ("-_", "-"),
    )
    _re_name = re.compile("([^a-zA-Z0-9\-_ ,])|(_+$)")

    def _clean_file_name(self, name):
        name = name.strip()

        for key, value in self._repl_name:
            name = name.replace(key, value)

        name = self._re_name.sub("", name)
        # name = re.sub("[^a-zA-Z0-9\-_ ,]","",name)
        return name

    def _get_resource(self, path):
        ad = os.path.abspath(os.path.join(tools.ustr(tools.config["root_path"]), u"addons"))
        mod_path_list = map(lambda m: os.path.abspath(tools.ustr(m.strip())), tools.config["addons_path"].split(","),)
        mod_path_list.append(ad)
        for mod_path in mod_path_list:
            module_path = mod_path + os.path.sep + path.split(os.path.sep)[0]

            if os.path.lexists(module_path):
                filepath = mod_path + os.path.sep + path
                filepath = os.path.normpath(filepath)

                python_path = os.path.dirname(filepath)
                if not python_path in sys.path:
                    sys.path.append(python_path)

                return {"module": module_path, "path": filepath, "zip": False}

            else:
                zip_path = module_path + ".zip"
                if os.path.lexists(zip_path):
                    return {
                        "module": path.split(os.path.sep)[0],
                        "path": zip_path,
                        "zip": True,
                    }
