import urllib.request
from moviepy.editor import *
import requests
from PIL import Image
import json
import os

class Download:

    def __init__(self , url , quality = 720 , output = "downloaded"):
        self.output = output
        qualityTypes = [360,720,1080]
        if quality not in qualityTypes:
            print("Error: Unkown Quality Type" + f" {quality} choose either 360 , 720 , 1080")
        else:
            self.postLink = requests.get("https://jackhammer.pythonanywhere.com/reddit/media/downloader" , params={'url':url}).text
            if 'v.redd.it' in self.postLink:
                print("Detected Post Type: Video")
                self.InitiateVideo(quality , self.postLink)
            elif 'i.redd.it' in self.postLink:
                print("Detected Post Type: Image")
                imageData = requests.get(self.postLink).content
                file = open(f'{self.output}'+'.jpeg' , 'wb')
                file.write(imageData)
                print("Sucessfully Downloaded Image " + f"{self.output}")
            else:
                print("Error: Could Not Recoganize Post Type")

    def InitiateVideo(self , quality , url):
        try:
            print('Fetching Video...')
            self.fetchVideo(quality , url)
            print('Fetching Audio...')
            self.fetchAudio(url)
            self.MergeVideo()
        except:
            print("Sorry there was an error while fetching video/audio files")

    def fetchVideo(self , quality , url):
        urllib.request.urlretrieve(url+f'/DASH_{quality}.mp4',"Video.mp4")

    def fetchAudio(self , url):
        doc = requests.get(url+'/DASH_audio.mp4')
        with open('Audio.mp3', 'wb') as f:
            f.write(doc.content)

    def MergeVideo(self):
        try:
            print("Merging Files")
            clip = VideoFileClip("Video.mp4")
            try:
                audioclip = AudioFileClip("Audio.mp3")
                videoclip = clip.set_audio(audioclip)
                videoclip.ipython_display()
                self.CleanUp()
                print(self.output + " Successfully Downloaded!")
            except:
                del clip.reader
                del clip
                print('Video has no sound')
                self.CleanUp(True)
                print(self.output + " Successfully Downloaded!")
        except Exception as e:
            print("Merge Failed!")
            print(e)

    def CleanUp(self , videoOnly = False):
        os.remove("Audio.mp3") 
        if videoOnly:
            os.rename('Video.mp4',self.output+'.mp4')
        else: 
            os.rename('__temp__.mp4',self.output+'.mp4')
            os.remove("Video.mp4")