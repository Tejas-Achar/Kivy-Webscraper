# ------------------------Import Libraries ---------------------------------------------
import pathlib
from bs4 import BeautifulSoup
import pandas as pd
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.uix.button import  Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import sys, subprocess
import os

#-------------------------Main Class-----------------------------------------------------
class Scrapper(App):

    def build(self):

        self.box = BoxLayout(orientation='vertical', spacing=5) #Parent Box
        self.box0 = BoxLayout(orientation='vertical', spacing=3) #Top Spacer
        self.box2 = BoxLayout(orientation='vertical' , spacing=3) #Bottom Spacer
        self.txt = TextInput(hint_text='Enter url here', size_hint=(1.0,0.1)) #Input field for url
        self.txt2 = TextInput(hint_text='enter tag here', size_hint=(1.0, 0.1)) #Input field for tag name
        self.LabelHeader = Label(text='Data Scrapper', font_size='20sp') #Heading label
        self.LabelHeader1 =Label(text='''Step 1 : Enter Url \nStep 2 : Enter the tag by which you want to scrape data \n                (Ex. a, div, p etc.)''', font_size='10sp')# Instruction Label        self.LabelHeader2 = Label(text='Data Will be displayed here !', font_size='12sp')
        self.LabelHeader2 = Label(text='Data Will be displayed here !', font_size='12sp')

        # Add labels to containers(Boxes)---------------
        self.box2.add_widget(self.LabelHeader2)
        self.box0.add_widget(self.LabelHeader)
        self.box0.add_widget(self.LabelHeader1)

        self.btn = Button(text='Clear All', on_press=self.clearText, size_hint=(1.0,0.1))#Clear all fields button
        self.btn1 = Button(text='Scrape Data',on_press=self.ScrapeData, size_hint=(1.0, 0.1))#Scrape website button

        #Add Buttons to containers(Boxes)----------------
        self.box.add_widget(self.box0)
        self.box.add_widget(self.txt)
        self.box.add_widget(self.txt2)
        self.box.add_widget(self.btn)
        self.box.add_widget(self.btn1)
        self.box.add_widget(self.box2)

        #show popup while scrapping----------------------
        self.popup = Popup(title='Test popup',
                      content=Label(text='Please Wait'),
                      size_hint=(None, None), size=(400, 400))


        return self.box
    # Method for clearing text fields--------------------
    def clearText(self, instance):

        self.txt.text = ''
        self.txt2.text = ''
    # Methods for scraping website ----------------------
    def ScrapeData(self,instance):

        url = self.txt.text # fetch url from input text field

        self.x = UrlRequest(url,on_success=self.TestMethod,on_failure=self.FailedStatus,verify=True)

        return
    # Method for displaying failed if it fails to scrape website--------------------------
    def FailedStatus(self, *args):
        self.LabelHeader.text = "URL REQUEST FAILED"

    # Main method for creating excel file using scrapped data----------------------------------------
    def TestMethod(self, *args):
        self.LabelHeader.text = "Data Scraping Started"
        self.popup.open()
        k = []
        url = self.txt.text
        tagname = self.txt2.text
        print(self.x.result)
        soupObject = BeautifulSoup(self.x.result, 'html.parser')
        # Check if tag name is anchor tag -------------------------------------
        if tagname != "a":
            y = soupObject.find_all(tagname)
            for i in y:
                # print(i.text)
                k.append(i.text)
        else:
            y = y = soupObject.find_all(tagname, href=True)
            for i in y:
                # print(i.text)
                k.append(i['href'])
        # Create data sheet with scraping results

        df = pd.DataFrame({tagname + " Tag Data for" + url: k})
        df.to_excel(tagname + ".xlsx")
        if sys.platform == "win32":
            os.startfile(tagname + ".xlsx")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, tagname + ".xlsx"])
        # self.get_Url(self.txt.text,self.txt2.text)
        self.LabelHeader2.text = "Data Saved in " + str(pathlib.Path().absolute())
        print(self.x.result)
        self.popup.dismiss()

Scrapper().run()
