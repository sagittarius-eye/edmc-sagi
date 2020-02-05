"""
The Sagittarius Eye EDMC plugin
:author: CMDR 147loch
:date: 05.02.2020
:version: 1.0.3
"""

import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

from sagi import links, release
import myNotebook as nb
from config import config

this = sys.modules[__name__]

this.plugin = "edmc-sagi"
this.version = "1.0.3"
this.client_version = "{}.{}".format(this.plugin, this.version)


def plugin_start(plugin_directory):
    """
    Plugin start hook
    :param plugin_directory: The directory (used by automated updates)
    :return: Plugin name
    """
    this.plugin_dir = plugin_directory
    links.RecentLinks.plugin_start(plugin_directory)
    release.Release.plugin_start(plugin_directory)
    return 'SAGi'


def plugin_end():
    # Plugin end hook
    pass


def plugin_prefs(parent, cmdr, is_beta):
    """
    Return a TK Frame for adding to the EDMC settings dialog.
    """
    this.disable_auto_update = tk.IntVar(value=config.getint("disable_auto_update"))
    frame = nb.Frame(parent)
    nb.Checkbutton(frame, text="Disable Auto Updates", variable=this.disable_auto_update).grid(padx=10, pady=10)
    nb.Label(frame, text='Loaded Version %s' % this.version).grid(padx=10, pady=10, sticky=tk.W)

    this.Release.plugin_prefs(frame)

    return frame


def prefs_changed(cmdr, is_beta):
    """
    Save settings.
    """
    config.set('disable_auto_update', this.disable_auto_update.get())


def plugin_app(parent):
    """
    Hook widgets with links to our latest media in the 4 different categories
    :param parent: tkinter frame parent
    :return: The frame
    """
    this.parent = parent
    this.frame = tk.Frame(parent)

    this.RecentLinks = links.RecentLinks(this.frame)
    this.Release = release.Release(this.version)

    rl = this.RecentLinks

    tk.Label(this.frame, text="Sagittarius Eye", justify=tk.LEFT).grid(row=0, columnspan=2, sticky="NSEW")

    tk.Label(this.frame, text="Issue:", justify=tk.LEFT).grid(row=1, column=0, sticky=tk.W)
    tk.Label(this.frame, text="Audio:", justify=tk.LEFT).grid(row=2, column=0, sticky=tk.W)
    tk.Label(this.frame, text="News:", justify=tk.LEFT).grid(row=3, column=0, sticky=tk.W)
    tk.Label(this.frame, text="Video:", justify=tk.LEFT).grid(row=4, column=0, sticky=tk.W)

    rl.issue_widget.grid(row=1, column=1, sticky="NSEW")
    rl.audio_widget.grid(row=2, column=1, sticky="NSEW")
    rl.bns_widget.grid(row=3, column=1, sticky="NSEW")
    rl.video_widget.grid(row=4, column=1, sticky="NSEW")

    this.frame.columnconfigure(1, weight=1)

    this.spacer = tk.Frame(this.frame)
    rl.update_window()

    return this.frame
