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
import pickle
kivy.require('1.8.0')

from os import listdir
from os import chdir
import subprocess
import RPi.GPIO as GPIO

import alsaaudio

alarmfile = 'alarm.mp3'
alarmvol = 22 
maxvol = 22 

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
        curday = time.localtime().tm_wday
        if self.alarmstate and curhour == self.hour and curmin == self.minute and cursec == 0 and curday < 5:
            self.playalarm()

    def updatealarm(self):
        pickle.dump( (self.alarmstate, self.hour, self.minute), 
            open( "alarm.p", "wb" ) )
        if self.alarmstate:
            self.alarm = '{0:02d}:{1:02d}'.format(self.hour,self.minute)
        else:
            self.alarm = 'Alarm Off.  Vol: {0:d}'.format(self.vol)

    def build(self):
        '''This method loads the root.kv file automatically

        :rtype: none
        '''

        Clock.schedule_interval(self.update, 1)

        chdir("/home/pi/musicbox")
        # loading the content of root.kv
        self.root = Builder.load_file('root.kv')
        self.mixer = alsaaudio.Mixer('PCM', cardindex=1)
        self.vol = int(self.mixer.getvolume()[0])

        GPIO.setmode(GPIO.BCM)
        self.mp3_files = [ f for f in listdir('.') if f[-4:] == '.mp3' ]

        if not (len(self.mp3_files) > 0):
            print "No mp3 files found!"
            quit()

        self.index = 0

        try:
            self.alarmstate, self.hour, self.minute = pickle.load( open( "alarm.p", "rb" ) )
	except:
            self.hour = 8
            self.minute = 30
            self.alarmstate = True
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
        subprocess.call(['the_matrix_scrolltext', 'GOOD', 'NIGHT'])
        subprocess.Popen(['mpg123'] + playlist)
        #popenAndCall(clearsong, ['mpg123'] + self.mp3_files)

    def playmusic(self):
        self.index += 1
        if self.index >= len(self.mp3_files):
            self.index = 0
        self.song = str(self.index) + ': ' + self.mp3_files[self.index]
        subprocess.call(['killall', 'mpg123'])
        subprocess.Popen(['the_matrix_scrolltext', 'GOOD', 'NIGHT'])
        subprocess.Popen(['mpg123', self.mp3_files[self.index]])
        #popenAndCall(clearsong, ['mpg123', self.mp3_files[self.index]])

    def playalarm(self):
        self.mixer.setvolume(alarmvol)
        subprocess.call(['killall', 'mpg123'])
        subprocess.Popen(['the_matrix_scrolltext', 'WAKE', 'UP'])
        subprocess.Popen(['mpg123'] + [alarmfile] * 5)

    def stopmusic(self):
        self.song = ''
        subprocess.call(['killall', 'mpg123'])
        subprocess.Popen(['the_matrix_scrolltext', ' '])
        print '--- Cleared all existing mp3s. ---'

    def alarmon(self):
        self.alarmstate = True
        self.updatealarm()

    def alarmoff(self):
        self.alarmstate = False
        self.updatealarm()

    def d0(self):
        return

    def d1(self):
        return

    def d2(self):
        return

    def d3(self):
        return

    def d4(self):
        return

    def d5(self):
        return

    def d6(self):
        return

    def d7(self):
        return

    def d8(self):
        return

    def d9(self):
        return

    def dce(self):
        return

    def dgo(self):
        return

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
        self.vol = self.vol + 1
        self.vol = max(self.vol, 0)
        self.vol = min(self.vol, maxvol)
        self.mixer.setvolume(self.vol)
        self.updatealarm()

    def voldown(self):
        self.vol = self.vol - 1
        self.vol = max(self.vol, 0)
        self.vol = min(self.vol, maxvol)
        self.mixer.setvolume(self.vol)
        self.updatealarm()

if __name__ == '__main__':
    '''Start the application'''

    EzsApp().run()
