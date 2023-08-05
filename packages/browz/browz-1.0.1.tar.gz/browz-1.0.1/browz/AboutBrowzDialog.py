# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
# This file is in the public domain
# END LICENSE

from browz_lib.AboutDialog import AboutDialog
import logging
import gettext
gettext.textdomain('browz')

logger = logging.getLogger('browz')


# See browz_lib.AboutDialog.py for more details about how this class works.

class AboutBrowzDialog(AboutDialog):
    __gtype_name__ = "AboutBrowzDialog"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutBrowzDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.
