# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# BEGIN LICENSE
# This file is in the public domain
# END LICENSE

from browz.PreferencesBrowzDialog import PreferencesBrowzDialog
from browz.AboutBrowzDialog import AboutBrowzDialog
from browz_lib import Window
import logging
from gi.repository import Gtk, WebKit  # pylint: disable=E0611
import locale
locale.textdomain('browz')

logger = logging.getLogger('browz')


# See browz_lib.Window.py for more details about how this class works

class BrowzWindow(Window):
    __gtype_name__ = "BrowzWindow"

    def finish_initializing(self, builder):  # pylint: disable=E1002
        """Set up the main window"""
        super(BrowzWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutBrowzDialog
        self.PreferencesDialog = PreferencesBrowzDialog

        # Code for other initialization actions should be added here.
        self.refreshButton = self.builder.get_object("refreshbutton")
        self.urlEntry = self.builder.get_object("urlEntry")
        self.scrolledWindow = self.builder.get_object("scrolledWindow")
        self.toolbar = self.builder.get_object("toolbar")
        self.noteBook = self.builder.get_object("noteBook")
        self.newTab = self.builder.get_object("newTab")
        context = self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.webView = WebKit.WebView()
        self.scrolledWindow.add(self.webView)
        self.webView.show()

    def on_refreshButton_clicked(self, widget):
        self.webView.reload()

    def checkHTTPPrefix(self, string):
        string = list(string)
        firstFour = []
        i = 0
        for char in string:
            if i > 3:
                break
            firstFour += [char]
            i += 1
        if firstFour == ['h', 't', 't', 'p']:
            print("True")
            return True
        else:
            print(firstFour)
            print("False")
            return False

    def on_newTab_clicked(self, widget):
        self.lowLevelVBox = Gtk.ScrolledWindow()
        self.lowLevelVBox.show()
        self.noteBook.append_page(self.lowLevelVBox, Gtk.Label("New Tab"))
        self.webViewNew = WebKit.WebView()
        self.lowLevelVBox.add(self.webViewNew)
        self.webViewNew.show()
        self.page = self.noteBook.get_current_page()
        print(self.page)
        self.noteBook.set_tab_reorderable(self.lowLevelVBox, True)

    def on_urlEntry_activate(self, widget):
        url = widget.get_text()
        self.checkHTTPPrefix(url)
        # Next Step: Automatically add http to the beginning if user didn't type it in
        # Also, make the urlEntry update to links that the user pressed.
        self.webView.open(url)
