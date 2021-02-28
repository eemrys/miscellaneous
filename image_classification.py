#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter, io
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from google.cloud import vision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


class IbmWatson:
    def __init__(self):
        self.authenticator = IAMAuthenticator('text')
        self.service = VisualRecognitionV3(version='2018-03-19',
                                           authenticator=self.authenticator)
        self.service.set_service_url('text')
        
    def classify(self, filename):
        with open(filename, 'rb') as images_file:
            classes_result = self.service.classify(images_file=images_file).get_result()
            return classes_result['images'][0]['classifiers'][0]['classes']
    
    
class GoogleCloud:
    def __init__(self):
        self.service = vision.ImageAnnotatorClient()
        
    def classify(self, filename):
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        return self.service.label_detection(image=image)
        
        
class MicrosoftAzure:
    def __init__(self):
        subscription_key = "text"
        endpoint = "text"
        self.service = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    def classify(self, filename):
        with open(filename, 'rb') as images_file:
            tags_result = self.service.tag_image_in_stream(images_file)
            return tags_result.tags

    
class ImageWindow:
    def __init__(self, master, filename):
        self.filename = filename
        self.master = master
        img = Image.open(self.filename)
        img.thumbnail((300,300))
        self.render = ImageTk.PhotoImage(img)
        self.openedWindow = Toplevel(self.master) 
        self.img = Label(self.openedWindow, image=self.render)
        self.img.image = self.render
        self.img.place(x=0, y=0)
        self.img.grid(row=0, column=0, rowspan=3, padx=1,pady=1)
        
        self.ibm_button = Button(self.openedWindow,
                                    text="IBM\nWatson",
                                    command=self._classify_ibm, width=10,
                                fg ="black", highlightbackground="white")
        self.ibm_button.grid(row=0, column=1,padx=5,pady=(5, 2), sticky='NSEW')
        self.gcl_button = Button(self.openedWindow,
                                    text="Google\nCloud",
                                    command=self._classify_gcl, width=10,
                                fg ="black", highlightbackground="white")
        self.gcl_button.grid(row=1, column=1,padx=5,pady=(3, 5), sticky='NSEW')
        self.azure_button = Button(self.openedWindow,
                                    text="Microsoft\nAzure",
                                    command=self._classify_azure, width=10,
                                fg ="black", highlightbackground="white")
        self.azure_button.grid(row=2, column=1,padx=5,pady=(3, 5), sticky='NSEW')
        
        self.scrollbar = tkinter.Scrollbar(self.openedWindow)
        self.text_box = tkinter.Text(self.openedWindow, width=45, height=0,
                                     padx=10, pady=10, borderwidth=2,
                                     relief=tkinter.GROOVE, cursor="arrow",
                                     yscrollcommand=self.scrollbar.set, wrap=tkinter.WORD,
                                    font=("Calibri", 12))
        self.scrollbar.config(command = self.text_box.yview)
        self.scrollbar.grid(row=0, column=3, rowspan=3, padx=1,pady=1, sticky='ns')
        self.text_box.insert(tkinter.INSERT, 'Нажмите на одну из кнопок слева чтобы провести анализ изображения и вывести список обнаруженных классов объектов.')
        self.text_box.config(state=tkinter.DISABLED)
        self.text_box.grid(row=0, column=2, rowspan=3, padx=1,pady=1, sticky='ns')

    
    def _classify_ibm(self):
        self.azure_button.configure(fg ="black", highlightbackground="white")
        self.gcl_button.configure(fg ="black", highlightbackground="white")
        self.ibm_button.configure(fg ="#37d3ff", highlightbackground="#37d3ff")
        ibm = IbmWatson()
        result = ibm.classify(self.filename)
        line = 'Detected classes:\n'
        for instance in result:
            line += '\nclass: ' + instance['class'].capitalize() + ' | ' + 'score: ' + str(instance['score']) + '\n'
        self._change_text(line)
    
    def _classify_gcl(self):
        self.azure_button.configure(fg ="black", highlightbackground="white")
        self.ibm_button.configure(fg ="black", highlightbackground="white")
        self.gcl_button.configure(fg ="#37d3ff", highlightbackground="#37d3ff")
        gcl = GoogleCloud()
        result = gcl.classify(self.filename)
        line = 'Detected classes:\n'
        for instance in result.label_annotations:
            line += '\nclass: ' + instance.description + ' | ' + 'score: ' + str(float("{:.3f}".format(instance.score))) + '\n'
        self._change_text(line)
        
    def _classify_azure(self):
        self.gcl_button.configure(fg ="black", highlightbackground="white")
        self.ibm_button.configure(fg ="black", highlightbackground="white")
        self.azure_button.configure(fg ="#37d3ff", highlightbackground="#37d3ff")
        azure = MicrosoftAzure()
        result = azure.classify(self.filename)
        line = 'Detected classes:\n'
        for instance in result:
            line += '\nclass: ' + instance.name.capitalize() + ' | ' + 'score: ' + str(float("{:.3f}".format(instance.confidence))) + '\n'
        self._change_text(line)
            
    def _change_text(self, text):
        self.text_box.config(state=tkinter.NORMAL)
        self.text_box.delete("1.0", tkinter.END)
        self.text_box.insert(tkinter.INSERT, text)
        self.text_box.config(state=tkinter.DISABLED)


class StartWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Visual Recognition")
        self.header = Label(self.master,
                            text="Анализ изображений\nна предмет выделения на них\nобъектов разных классов",
                            font=("Calibri", 16))
        self.header.pack(padx = 20, pady = (40, 10))
        self.upload_button = Button(self.master,
                                    text="Выберите изображения для анализа",
                                    command=self._upload_file, width=30, height=2)
        self.upload_button.pack(padx = 50, pady = (20, 50))
        
    def _upload_file(self):
        files = tkinter.filedialog.askopenfilenames(title="Выберите изображения",
                                                    filetypes=[("image", ".jpeg"),
                                                               ("image", ".png"),
                                                               ("image", ".jpg"),])
        for f in files:
            ImageWindow(self.master, f)
            

root = tkinter.Tk()
mw = StartWindow(root)
root.mainloop()