import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

from ttkHyperlinkLabel import HyperlinkLabel
import requests

DEFAULT_NEWS_URL = 'https://sagittarius-eye.com/'


class LinkElement(HyperlinkLabel):
    def __init__(self, parent):
        HyperlinkLabel.__init__(
            self,
            parent,
            text="Fetching News...",
            url=DEFAULT_NEWS_URL,
            wraplength=50,  # updated in __configure_event below
            anchor=tk.NW
        )
        self.resized = False
        self.bind('<Configure>', self.__configure_event)

    def __reset(self):
        self.resized = False

    def __configure_event(self, event):
        if not self.resized:
            self.resized = True
            self.configure(wraplength=event.width)
            self.after(500, self.__reset)


class RecentLinks:
    """
    Main widget class
    """

    plugin_dir = None

    def __init__(self, parent):
        self.__frame = parent
        self.__issue_widget = LinkElement(parent)
        self.__video_widget = LinkElement(parent)
        self.__audio_widget = LinkElement(parent)
        self.__bns_widget = LinkElement(parent)
        self.__news_data = []
        self.__latestIssue = None

    def update_window(self):
        self.__news_data = requests.get('https://bot.sagittarius-eye.com/api/lastBroadcast/all/').json()
        for data in self.__news_data:
            if data['source'] == "issues":
                self.__issue_widget['url'] = data['request']['magazine']['url']
                self.__issue_widget['text'] = 'Issue {} - {}'.format(data['request']['magazine']['issue']['number'],
                                                                     data['request']['magazine']['title'])
                pass
            elif data['source'] == "audio":
                self.__latestIssue = [int(s) for s in data['request']['audio']['title'].split() if s.isdigit()]
                self.__audio_widget['url'] = 'https://podcast.sagittarius-eye.com/'
                self.__audio_widget['text'] = 'Issue {}'.format(self.__latestIssue[0])
                pass
            elif data['source'] == "posts":
                self.__bns_widget['url'] = data['request']['post']['url']
                self.__bns_widget['text'] = data['request']['post']['title']
                pass
            elif data['source'] == "bulletins":
                self.__video_widget['url'] = data['request']['youtubeVideo']['url']
                self.__video_widget['text'] = data['request']['youtubeVideo']['title']
                pass
        pass

    @classmethod
    def plugin_start(cls, plugin_dir):
        cls.plugin_dir = plugin_dir

    @property
    def issue_widget(self):
        return self.__issue_widget

    @property
    def video_widget(self):
        return self.__video_widget

    @property
    def audio_widget(self):
        return self.__audio_widget

    @property
    def bns_widget(self):
        return self.__bns_widget

    @issue_widget.setter
    def issue_widget(self, e):
        self.__issue_widget = e
        pass

    @video_widget.setter
    def video_widget(self, e):
        self.__video_widget = e
        pass

    @audio_widget.setter
    def audio_widget(self, e):
        self.__audio_widget = e
        pass

    @bns_widget.setter
    def bns_widget(self, e):
        self.__bns_widget = e
        pass
