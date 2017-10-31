import kivy

from kivy.app import App
from kivy.base import runTouchApp
from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition

from kivy.uix.progressbar import ProgressBar

import time
import random
import os
from os import listdir
from os.path import isfile, join

from src.sqlite.query_db import generate_output


inputimage = None


def ocr(filename):
	print "-------------------------------------------------------------------------"
	print "\t\t\tRUNNNING OCR"
	print "-------------------------------------------------------------------------"
	os.system('python src/extract_text.py {} data/output/pre_output.jpg'.format(inputimage))
	txtfile = 'data/text/{}.txt'.format(inputimage.split('/')[-1].split('.')[0])
	database=	"src/sqlite/projectdb.sqlite"
	outputImage = 'data/output/output.jpg'
	hindiTextImage = 'data/output/textoutput.jpg'
	generate_output(txtfile,database,outputImage,hindiTextImage)
	

class MyWidget(Widget):
	progress_bar = ObjectProperty()	
	def __init__(self, **kwa):
		super(MyWidget, self).__init__(**kwa)
		self.progress_bar = ProgressBar()
		self.popup = Popup(
			title='Translating',
			content=self.progress_bar,
			title_size='30sp'
		)
		self.popup.bind(on_open=self.puopen)
	def pop(self):
		self.progress_bar.value = 1
		self.popup.open()
	def next(self, dt):
		if self.progress_bar.value>=100:
			self.popup.dismiss()
			return False
		self.progress_bar.value += 1
	def puopen(self,instance):
		Clock.schedule_interval(self.next, 1/5)


class RootCamWidget(Screen):
	def capture(self):
		image = self.manager.get_screen('first').ids.cam
		inputfile = "data/input/input.jpg"
		image.export_to_png(inputfile)
		print("Captured")
		ocr(inputfile)
		time.sleep(1)
		self.manager.current = 'third'

class Loading(Screen):
	pass

class HindiTransWidget(Screen):
	def update_img(self, sec):
		try:
			self.ids.image.source = 'data/output/output.jpg'
			self.Image.reload()
		except:
			pass
	def on_start(self):
		event1 = Clock.create_trigger(self.update_img)
		Clock.schedule_interval(self.update_img, 2) # 2 sec
		event1()

class MyScreenManager(ScreenManager):
	pass


root_widget = Builder.load_string('''
#:import Factory kivy.factory.Factory
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
MyScreenManager:
	transition: FadeTransition()
	RootCamWidget:
	Loading:
	HindiTransWidget:
<RootCamWidget>:
	name: 'first'
	BoxLayout:
		orientation: 'vertical'
		padding:10
		spacing:10
		Label:
			font_size: '30sp'
			text: 'TranslateMenu'
			size_hint_y: None
		Camera:
			id: cam
			resolution: (480,640)
			play: False
		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			Button:
				font_size: '20sp'
				text: 'Play'
				on_press: cam.play = not cam.play
				height: '50dp'
			Button:
				font_size: '20sp'
				text: 'Capture'
				height: '50dp'
				on_release: cam.play = False
				on_release: root.capture()
			Button:
				font_size: '20sp'
				text: 'Exit'
				height: '50dp'
				on_release: app.stop()
<Loading>:
	name: 'second'
	BoxLayout:
		orientation: 'vertical'
		padding:10
		spacing:10
		Label:
			font_size: '30sp'
			text: 'Translating...'
			size_hint_y: None		
		MyWidget:
			id: progbar
		Button:
			font_size: '30sp'
			text: ''
			height: '80dp'
<HindiTransWidget>:
	on_pre_enter: root.manager.get_screen('second').ids.progbar.pop()
	on_enter: self.on_start()
	id: htw
	name: 'third'
	BoxLayout:
		orientation: 'vertical'
		padding:10
		spacing:10
		Label:
			font_size: '30sp'
			text: 'Menu Details'
			size_hint_y: None		
		Image:
			id: image
			keep_ratio: True
			allow_stretch: True
		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			Button:
				font_size: '20sp'
				text: 'Back'
				on_release: app.root.current = 'first'
				height: '50dp'
			Button:
				font_size: '20sp'
				text: 'Exit'
				height: '50dp'
				on_release: app.stop()
''')


class TranslateMenu(App):
	def build(self):
		return root_widget

if __name__ == "__main__":
	print "-------------------------------------------------------------------------"
	print "\t\t\tMENU TRANSLATION PROJECT Version 0.1.2"
	print "-------------------------------------------------------------------------\n\n"
	print "-------------------------------------------------------------------------"
	print "NOTE: \n1. While taking the picture make sure the dish to be queried is at the top in the image! \n2. If working on Desktop, save the clicked picture in the data directory and set the corresponding flag and inputfile name\n3. Happy Feasting!"
	print "-------------------------------------------------------------------------\n\n"
	print "-------------------------------------------------------------------------"
	print "1. Running on android device \t\t 2. Running on Desktop\n"
	while(1):
		choice = raw_input("Enter input:\t")
		if(choice == str(1)):
			print "This version doesn't provide android support. Stay tuned for the later releases!\n"
		else:
			input_data_dir = 'data/input'
			print "\n\nFiles available:"
			files = [f for f in listdir(input_data_dir) if isfile(join(input_data_dir,f)) and (f.endswith(".jpg") or f.endswith(".png"))]
			print files
			inputimage = join(input_data_dir,raw_input("Enter input image filename:\t"))
			break
	print "-------------------------------------------------------------------------\n\n"
	print "-------------------------------------------------------------------------"
	print "\t\t\tPress Capture Button"
	print "-------------------------------------------------------------------------\n\n"
	TranslateMenu().run()
