#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout



class ClockLayout(FloatLayout):

    status = StringProperty("Initializing")
    hour = StringProperty("00:00:00")


class SimpleClockApp(App):

    def on_start(self):
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        now = datetime.datetime.now()
        self.root.hour = "{hh:02d}:{mm:02d}:{ss:02d}".format(
            hh=now.hour,
            mm=now.minute,
            ss=now.second,
            )
        self.root.status = "SimpleClock"


if __name__ == "__main__":
    app = SimpleClockApp()
    app.run()


