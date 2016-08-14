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

alarmfile = 'alarm.mp3'
alarmvol = 90

class RootWidget(BoxLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from a kv file.
    '''

    container = ObjectProperty(None)

class EzsApp(App):
    song = Property('')
    time = Property('')
    date = Property('')
    alarm = Property('')

    '''This is the app itself'''

    def update(self, *args):
        self.time = time.strftime('%I:%M:%S')
        self.date = time.strftime('%A %B %d %Y')
        curhour = time.localtime().tm_hour
        curmin = time.localtime().tm_min
        cursec = time.localtime().tm_sec
        if curhour == self.hour and curmin == self.minute and cursec == 0:
            self.playalarm()

    def updatealarm(self):
        self.alarm = str(self.hour) + ':' + str(self.minute)

    def build(self):
        '''This method loads the root.kv file automatically

        :rtype: none
        '''

        Clock.schedule_interval(self.update, 1)

        chdir("/home/pi/musicbox")
        # loading the content of root.kv
        self.root = Builder.load_file('root.kv')
        self.mixer = alsaaudio.Mixer('PCM', cardindex=1)

        GPIO.setmode(GPIO.BCM)
        self.mp3_files = [ f for f in listdir('.') if f[-4:] == '.mp3' ]

        if not (len(self.mp3_files) > 0):
            print "No mp3 files found!"
            quit()

        self.index = 0

        self.hour = 8
        self.minute = 30
        self.updatealarm()

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

    def playalarm(self):
        self.mixer.setvolume(alarmvol)
        subprocess.call(['killall', 'mpg123'])
        subprocess.Popen(['mpg123', alarmfile])

    def stopmusic(self):
        self.song = ''
        subprocess.call(['killall', 'mpg123'])
        print '--- Cleared all existing mp3s. ---'

    def hourup(self):
        if self.hour < 24:
            self.hour += 1
        self.updatealarm()

    def minuteup(self):
        if self.minute < 59:
            self.minute += 1
        self.updatealarm()

    def hourdown(self):
        if self.hour > 0:
            self.hour -= 1
        self.updatealarm()

    def minutedown(self):
        if self.minute > 0:
            self.minute -= 1
        self.updatealarm()

    def volup(self):
        vol = self.mixer.getvolume()
        vol = int(vol[0])
        vol = vol + 1
        #vol = min(vol, 100)
        vol = min(vol, 80)
        self.mixer.setvolume(vol)

    def voldown(self):
        vol = self.mixer.getvolume()
        vol = int(vol[0])
        vol = vol - 1
        vol = max(vol, 0)
        self.mixer.setvolume(vol)

if __name__ == '__main__':
    '''Start the application'''

    EzsApp().run()
