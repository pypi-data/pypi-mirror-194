# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
# This file is in the public domain
# END LICENSE

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.browz.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from browz_lib.PreferencesDialog import PreferencesDialog
import logging
from gi.repository import Gio  # pylint: disable=E0611

import gettext
gettext.textdomain('browz')

logger = logging.getLogger('browz')


class PreferencesBrowzDialog(PreferencesDialog):
    __gtype_name__ = "PreferencesBrowzDialog"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the preferences dialog"""
        super(PreferencesBrowzDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        settings = Gio.Settings("net.launchpad.browz")
        widget = self.builder.get_object('example_entry')
        settings.bind("example", widget, "text", Gio.SettingsBindFlags.DEFAULT)

        # Code for other initialization actions should be added here.
