#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Container Example
==============

This example shows how to add a container to our screen.
A container is simply an empty place on the screen which
could be filled with any other content from a .kv file.
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import Property
from kivy.clock import Clock

import os
import kivy
import time
kivy.require('1.8.0')

from os import listdir
from os import chdir
import subprocess
import RPi.GPIO as GPIO

import alsaaudio


class RootWidget(BoxLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from a kv file.
    '''

    container = ObjectProperty(None)

class EzsApp(App):
    song = Property('')
    time = Property('')
    date = Property('')

    '''This is the app itself'''

    def update(self, *args):
        self.time = time.strftime('%I:%M:%S')
        self.date = time.strftime('%A %B %d %Y')

    def build(self):
        '''This method loads the root.kv file automatically

        :rtype: none
        '''

        Clock.schedule_interval(self.update, 1)

        chdir("/home/pi/musicbox")
        # loading the content of root.kv
        self.root = Builder.load_file('root.kv')
        self.mixer = alsaaudio.Mixer('PCM')
        GPIO.setmode(GPIO.BCM)
        self.mp3_files = [ f for f in listdir('.') if f[-4:] == '.mp3' ]

        if not (len(self.mp3_files) > 0):
            print "No mp3 files found!"
            quit()

        self.index = 0

    def clearsong():
        self.song = ''

    def popenAndCall(onExit, *popenArgs, **popenKWArgs):
            def runInThread(onExit, popenArgs, popenKWArgs):
                proc = subprocess.Popen(*popenArgs, **popenKWArgs)
                proc.wait()
                onExit()
                return
            thread = threading.Thread(target=runInThread, 
                                      args=(onExit, popenArgs, popenKWArgs))
            thread.start()
            return thread

    def playall(self):
        i = 0
        playlist = []
    
        self.index += 1
        if self.index >= len(self.mp3_files):
            self.index = 0
        startsong = self.index
        while( i < 5):
            playlist.append(self.mp3_files[self.index])
            i += 1
            self.index += 1
            if self.index >= len(self.mp3_files):
                self.index = 0
        endsong = self.index
        
        self.song = 'Play ' + str(startsong) + ' - ' + str(endsong)
        subprocess.call(['killall', 'mpg123'])
        subprocess.Popen(['mpg123'] + playlist)
        #popenAndCall(clearsong, ['mpg123'] + self.mp3_files)

    def playmusic(self):
        self.index += 1
        if self.index >= len(self.mp3_files):
            self.index = 0
        self.song = str(self.index) + ': ' + self.mp3_files[self.index]
        subprocess.call(['killall', 'mpg123'])
        subprocess.Popen(['mpg123', self.mp3_files[self.index]])
        #popenAndCall(clearsong, ['mpg123', self.mp3_files[self.index]])

    def stopmusic(self):
        self.song = ''
        subprocess.call(['killall', 'mpg123'])
        print '--- Cleared all existing mp3s. ---'

    def volup(self):
        vol = self.mixer.getvolume()
        vol = vol[0]
        vol = vol + 2
        #vol = min(vol, 100)
        vol = min(vol, 80)
        self.mixer.setvolume(vol)

    def voldown(self):
        vol = self.mixer.getvolume()
        vol = vol[0]
        vol = vol - 2
        vol = max(vol, 50)
        self.mixer.setvolume(vol)

if __name__ == '__main__':
    '''Start the application'''

    EzsApp().run()
