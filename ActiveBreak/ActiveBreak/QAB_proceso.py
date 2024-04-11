# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ActiveBreak
                                 A QGIS plugin
                              -------------------
        begin                : 2024-04-04
        copyright            : (C) 2024 by Aldo Sardelli
        email                : asardelli@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *  This program is covered by the terms of the GNU General Public License *
 *  <https://www.gnu.org/licenses/>.                                       *
 *                                                                         *
 ***************************************************************************/
"""
import sys
import os
from qgis.core import *
from qgis.utils import iface, reloadPlugin, plugins
from qgis.gui import QgsMessageBar, QgisInterface
from PyQt5 import QtCore, QtWidgets
from qgis.PyQt import *
from qgis.PyQt.QtCore import *
from PyQt5.QtGui import QIcon, QColor, QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import webbrowser
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import time
import winsound
import random
from datetime import date, time, datetime


# Import the code for the DockWidget
import os.path


class QAB:
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.n=0
        self.r=0
        self.start_time_m = QTime(6, 00 , 00)                     #start of the work day-morning time
        self.start_time_m2 = QTime(8, 30 , 00)                     #start of the work day-morning time
        self.end_time_m = QTime(12, 00 , 00)                     #end of the working day-morning time
        self.start_time_a = QTime(13, 00 , 00)                     #start of the work day-afternoon time
        self.start_time_a2 = QTime(14, 30 , 00)                     #start of the work day-afternoon time
        self.end_time_a = QTime(18, 00 , 00)                     #end of the working day-afternoon time
        self.start = datetime.now()
        
        
        
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_AB_path = QIcon(os.path.dirname(__file__) + "/qgis_icon_active_break.png")
        self.action = QAction(icon_AB_path,"Reset time", self.iface.mainWindow())
        self.action.triggered.connect(self.stopwatch)
        self.iface.addPluginToMenu("ActiveBreak", self.action)
        #ABOUT
        icon_AB_path = QIcon(os.path.dirname(__file__) + "/github_logo.png")
        self.actionA = QAction(icon_AB_path,"About", self.iface.mainWindow())
        self.actionA.triggered.connect(self.runABOUT)
        self.iface.addPluginToMenu("ActiveBreak", self.actionA)
        self.stopwatch()
        
        
    def stopwatch(self):
        self.cron = QTimer()
        self.cron.timeout.connect(self.cronEvent)
        self.cronreload = QTimer()
        self.cronreload.timeout.connect(self.reloadMessage)
        self.cron.start(3600000)                         #hourly
        self.cronreload.start(900000)                         #hourly
        iface.messageBar().pushMessage(f'ActiveBreak. Set time from now <b>{datetime.now().strftime("%H:%M:%S")}</b>!',Qgis.Success, duration= 5)
        
        
    def cronEvent(self):
        now = datetime.now()
        HHnow=QTime(now.time())                             #current time
        if self.start_time_m < HHnow < self.end_time_m or self.start_time_a < HHnow < self.end_time_a:
            if self.n==0:
                self.widget = iface.messageBar().createMessage("It's important to save your project, do it now! "+"\U0001f4be")
                self.button = QPushButton(self.widget)
                self.button.setText("Save "+"\U0001f4be")
                self.button.pressed.connect(self.saveProject)
                self.widget.layout().addWidget(self.button)
                if self.start_time_m < HHnow < self.start_time_m2 and self.r==1:
                    self.button2 = QPushButton(self.widget)
                    self.button2.setText("Reload plugin "+"\U000027F3")
                    self.button2.pressed.connect(self.reload)
                    self.widget.layout().addWidget(self.button2)
                else:
                    pass
                if self.start_time_a < HHnow < self.start_time_a2:
                    self.button2 = QPushButton(self.widget)
                    self.button2.setText("Reset time "+"\U0001F550")
                    self.button2.pressed.connect(self.stopwatch)
                    self.widget.layout().addWidget(self.button2)
                else:
                    pass
                iface.messageBar().pushWidget(self.widget, duration=5)
                self.n=1
            else:
                winsound.MessageBeep()
                self.widget = iface.messageBar().createMessage("Active Break", "It's time to take your active break    "+"\U0000270B")
                self.button = QPushButton(self.widget)
                self.button.setStyleSheet("background-color: #3399FF")
                self.button.setText("My message "+"\U0001F48C")
                self.button.pressed.connect(self.showMessage)
                self.widget.layout().addWidget(self.button)
                self.button1 = QPushButton(self.widget)
                self.button1.setText("Save "+"\U0001f4be")
                self.button1.pressed.connect(self.saveProject)
                self.widget.layout().addWidget(self.button1)
                if self.start_time_m < HHnow < self.start_time_m2 and self.r==1:
                    self.button2 = QPushButton(self.widget)
                    self.button2.setText("Reload plugin "+"\U000027F3")
                    self.button2.pressed.connect(self.reload)
                    self.widget.layout().addWidget(self.button2)
                else:
                    pass
                if self.start_time_a < HHnow < self.start_time_a2:
                    self.button2 = QPushButton(self.widget)
                    self.button2.setText("Reset time "+"\U0001F550")
                    self.button2.pressed.connect(self.stopwatch)
                    self.widget.layout().addWidget(self.button2)
                else:
                    pass
                iface.messageBar().pushWidget(self.widget, duration=10)
                self.n=0
        elif self.end_time_m < HHnow < self.start_time_a:
            self.widget = iface.messageBar().createMessage("It's time for your lunch. Enjoy it!"+"\U0001F60B")
            self.button = QPushButton(self.widget)
            self.button.setText("Save "+"\U0001f4be")
            self.button.pressed.connect(self.saveProject)
            self.widget.layout().addWidget(self.button)
            iface.messageBar().pushWidget(self.widget, duration=10)
            self.n=0
        else:
            self.n=0
            self.r=2
        return self.r
    
    def reloadMessage(self):
        now = datetime.now()
        HHnowr=QTime(now.time())                             #current time
        if self.start_time_m < HHnowr < self.start_time_m2:
            if self.r>1:
                self.widget = iface.messageBar().createMessage(f"The ActiveBreak plugin is active since {self.start}. It's advisable to reload ")
                self.button2 = QPushButton(self.widget)
                self.button2.setText("Reload plugin "+"\U000027F3")
                self.button2.pressed.connect(self.reload)
                self.widget.layout().addWidget(self.button2)
                iface.messageBar().pushWidget(self.widget, duration=5)
                if self.r==4:
                    self.r=1
                else:
                    self.r=self.r+1
            elif self.r==1:
                self.r=self.r+1
            else:
                pass
        elif self.start_time_m2 < HHnowr < self.end_time_a:
            self.r=0
        else:
            self.r=2
        return self.r
        
    def unload(self):
        self.cron.stop()
        #remover del pluggin menu
        self.iface.removePluginMenu("ActiveBreak", self.action)
        del self.action
        self.iface.removePluginMenu("ActiveBreak", self.actionA)
        del self.actionA
    #-------------------------------------------------------------------Previo
    def saveProject(self):
        project = QgsProject.instance()
        # Save the project to the same
        iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger() 
#        project.write()
    
    def showMessage(self):
        r=random.randint(0, 467)
        Message=self.messageEN(r)
        Messagelist=Message.split("-")
        Mes=Messagelist[0]
        try:
            Mes=Mes.replace("_","-")
        except:
            pass
        Aut=Messagelist[1]
        textm=f'<FONT SIZE=7> <i>«{Mes}»</i></font>'
        texta=f'<FONT SIZE=6> <b>- {Aut} </b></font>'
        data = QImage(os.path.dirname(__file__) + "/qgis_icon_active_break.png")
        pixmap = QPixmap(data).scaledToHeight(50, Qt.SmoothTransformation)
        msg = QMessageBox()
        msg.setWindowTitle("Random Message")
        msg.setIconPixmap(pixmap)
        msg.setText('<FONT SIZE=4><b>There is a message for you...</b></font>')
        msg.setInformativeText(textm + texta)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setText("Go for it!")
        msg.addButton("Download",QMessageBox.ActionRole)
        reply=msg.exec() 
        if reply == QMessageBox.AcceptRole:
            self.downloadMessage(r,Mes,Aut)
        else:
            pass
    
    def downloadMessage(self,r,Mes,Aut):
        #Font
        file = open(os.path.dirname(__file__) +"/fonts/KaushanScript-Regular.otf", "rb")
        KaushanScript = BytesIO(file.read())
        file.close()
        file = open(os.path.dirname(__file__) +"/fonts/AlexBrush-Regular.ttf", "rb")
        AlexBrush = BytesIO(file.read())
        file.close()
        file = open(os.path.dirname(__file__) +"/fonts/StardustAdventure.ttf", "rb")
        StardustAdventure = BytesIO(file.read())
        file.close()
        #Open image
        img = Image.open(os.path.dirname(__file__) +'/resources/activebreak_message_template1920_960.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(KaushanScript, 50)
        mb = QMessageBox()
        mb.setText('You want to personalize the message?. ')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mb.button(QMessageBox.Ok).setText("Ok")
        mb.button(QMessageBox.Cancel).setText("Cancel")
        return_value = mb.exec()
        #custom
        if return_value == QMessageBox.Ok:
            to, okPressed =QInputDialog.getText(None,"Message To","Name:",QLineEdit.Normal,"")
            to=to.title()
            text=(f'{to}, there is a message for you...')
            draw.text((100, 105), text, font=font, fill="#606060")
        elif return_value == QMessageBox.Cancel:
            draw.text((100, 105), "There is a message for you...", font=font, fill="#606060")
        #Select quote
        vme=Mes
        try:
            vm='«'+vme+'»'
        except:
            vm=vme
        nunvm=len(vm)
        va=Aut
        vm = vm. split (" ")
        n1=0
        line1=''
        line2=''
        line3=''
        line4=''
        line5=''
        line6=''
        if nunvm<101:
            typesize='A'
            for l in vm:
                n=len(l)
                n1=n1+n+1
                if n1<36:
                    line1=line1+' '+l
                if n1>35 and n1<71:
                    line2=line2+' '+l
                if n1>70 and n1<101:
                    line3=line3+' '+l
            text=line1+'\n'+line2+'\n'+line3
            fonttext = ImageFont.truetype(AlexBrush, 83)
            lines = text.splitlines()
            w=1000
            h = 250
        elif 100< nunvm < 201:
            typesize='B'
            for l in vm:
                n=len(l)
                n1=n1+n+1
                if n1<51:
                    line1=line1+' '+l
                if n1>50 and n1<101:
                    line2=line2+' '+l
                if n1>100 and n1<141:
                    line3=line3+' '+l
                if n1>140 and n1<201:
                    line4=line4+' '+l
            text=line1+'\n'+line2+'\n'+line3+'\n'+line4
            fonttext = ImageFont.truetype(AlexBrush, 83)
            lines = text.splitlines()
            w=1400
            h = 300
        elif 200< nunvm < 301:
            typesize='C'
            for l in vm:
                n=len(l)
                n1=n1+n+1
                if n1<51:
                    line1=line1+' '+l
                if n1>50 and n1<101:
                    line2=line2+' '+l
                if n1>100 and n1<151:
                    line3=line3+' '+l
                if n1>150 and n1<201:
                    line4=line4+' '+l
                if n1>200 and n1<251:
                    line5=line5+' '+l
                if n1>250:
                    line6=line6+' '+l
            text=line1+'\n'+line2+'\n'+line3+'\n'+line4+'\n'+line5+'\n'+line6
            fonttext = ImageFont.truetype(AlexBrush, 83)
            lines = text.splitlines()
            w=1600
            h = 400
        elif nunvm >300:
            typesize='D'
            for l in vm:
                n=len(l)
                n1=n1+n+1
                if n1<61:
                    line1=line1+' '+l
                if n1>60 and n1<121:
                    line2=line2+' '+l
                if n1>120 and n1<181:
                    line3=line3+' '+l
                if n1>180 and n1<241:
                    line4=line4+' '+l
                if n1>240 and n1<301:
                    line5=line5+' '+l
                if n1>300:
                    line6=line6+' '+l
            text=line1+'\n'+line2+'\n'+line3+'\n'+line4+'\n'+line5+'\n'+line6
            fonttext = ImageFont.truetype(AlexBrush, 82)
            lines = text.splitlines()
            w=1700
            h = 500
        x, y = img.size
        x /= 2
        x -= w / 2
        y /= 2
        y -= h / 2

        if nunvm<51:
            fya=(y+h)*0.08
        elif 50< nunvm < 101:
            fya=(y+h)*0.05
        elif 100< nunvm < 201:
            fya=(y+h)/28
        elif 200< nunvm < 301:
            fya=(y+h)*0.02
        else:
            fya=(y+h)*0.02
        ya =y+h+fya
        draw.multiline_text((x, y), text, font=fonttext, fill="#404040",align="center")
        if len(va)<16:
            draw.text((1200, ya+60), va, font=ImageFont.truetype(StardustAdventure, 90), fill="black")
        elif 15<len(va)<21:
            draw.text((1150, (ya+75)), va, font=ImageFont.truetype(StardustAdventure, 80), fill="black")
        elif 20<len(va)<31:
            draw.text((1150, ya), va, font=ImageFont.truetype(StardustAdventure, 80), fill="black")
        elif 30<len(va)<45:
            draw.text((1100, ya), va, font=ImageFont.truetype(StardustAdventure, 60), fill="black")
        else:
            pass
        try:
            sufijo=to.upper()
        except:
            sufijo=r
        img.save(f'msgActiveBreak{sufijo}.png')
        #confirm window
        data = QImage(os.path.dirname(__file__) + "/qgis_icon_active_break.png")
        pixmap = QPixmap(data).scaledToHeight(54, Qt.SmoothTransformation)
        msg = QMessageBox()
        msg.setWindowTitle("ACTIVE BREAK")
        msg.setIconPixmap(pixmap)
        msg.setText('The message was successfully')
        msg.setInformativeText('saved in the documents')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        
    
    def reload(self):
        reloadPlugin('ActiveBreak')
        
    def runABOUT(self):
        '''Display a help page'''
        url = 'https://github.com/asardelli/ActiveBreak.git'
        b=webbrowser.open(url, new=2)
        iface.messageBar().pushMessage('Copie '+ url + ' y pegue en su explorador si la página no abre automáticamente',Qgis.Info, duration=10)
    
    def messageEN(self,r):
        MSGlist=["A champion is afraid of losing. Everyone else is afraid of winning.-Billie Jean King",\
        "A diamond is merely a lump of coal that did well under pressure.-Unknown",\
        "A goal is a dream with a deadline.-Napoleon Hill",\
        "A negative mind will never give you a positive life.-Unknown",\
        "A reader lives a thousand lives before he dies. The man who never reads lives only one.-George R.R. Martin",\
        "A surplus of effort could overcome a deficit of confidence.-Sonia Sotomayer",\
        "A walk to a nearby park may give you more energy and inspiration in life than spending two hours in front of a screen.-Tsang Lindsay",\
        "A winner is a dreamer who never gives up.-Nelson Mandela",\
        "A year from now you will wish you had started today.-Unknown",\
        "Act as if what you do makes a difference. It does.-William James",\
        "Action is the foundational key to all success.-Pablo Picasso",\
        "After all this time_Always.-J.K. Rowling",\
        "All our dreams can come true, if we have the courage to pursue them.-Walt Disney",\
        "All we can do is the best we can do.-David Axelrod",\
        "Alone we can do so little, together we can do so much.-Helen Keller",\
        "Always be careful when you follow the masses. Sometimes the m is silent.-Unknown",\
        "Amateus sit around and wait for inspiration. The rest of us just get up and go to work.-Stephen King",\
        "And the day came when the risk to remain tight in a bud was more painful than the risk it took to blossom.-Anaïs Nin",\
        "And when you get the choice to sit it out or dance … I hope you dance.-I Hope You Dance, Lee Ann Womack",\
        "And, when you want something, all the universe conspires in helping you to achieve it.-Paulo Coelho, The Alchemist",\
        "Anything can make me stop and look and wonder, and sometimes learn.-Kurt Vonnegut",\
        "As a single footstep will not make a path on the earth, so a single thought will not make a pathway in the mind. To make a deep physical path, we walk again and again. To make a deep mental path, we must think over and over the kind of thoughts we wish to dominate our lives.-Henry David Thoreau",\
        "At any given moment you have the power to say: This is not how the story is going to end.-Unknown",\
        "At the end of the day we can endure much more than we think we can.-Frida Kahlo",\
        "Attitude is a choice. Happiness is a choice. Optimism is a choice. Kindness is a choice. Giving is a choice. Respect is a choice. Whatever choice you make makes you. Choose wisely.-Roy T. Bennett",\
        "Be a positive energy trampoline – absorb what you need and rebound more back.-Dave Carolan",\
        "Be happy with what you have while working for what you want.-Helen Keller",\
        "Be miserable. Or motivate yourself. Whatever has to be done, it's always your choice.-Wayne Dyer",\
        "Be so good they can’t ignore you.-Steve Martin",\
        "Be sure you put your feet in the right place, then stand firm.-Abraham Lincoln",\
        "Be the change that you wish to see in the world.-Mahatma Gandhi",\
        "Begin anywhere.-John Cage",\
        "Believe in yourself, take on your challenges, dig deep within yourself to conquer fears. Never let anyone bring you down. You got to keep going.-Chantal Sutherland",\
        "Better three hours too soon than a minute too late.-William Shakespeare",\
        "Change is painful, but nothing is as painful as staying stuck somewhere you don’t belong.-Mandy Hale",\
        "Change is the law of life. And those who look only to the past or present are certain to miss the future.-John F. Kennedy",\
        "Coming together is a beginning. Keeping together is progress. Working together is success.-Henry Ford",\
        "Competing at the highest level is not about winning. It’s about preparation, courage, understanding, nurturing your people, and heart. Winning is the result.-Joe Torre",\
        "Concentrate all your thoughts upon the work in hand. The sun's rays do not burn until brought to a focus.-Alexander Graham Bell",\
        "Courage is like a muscle. We strengthen it by use.-Ruth Gordo",\
        "Courage is the most important of all the virtues because without courage, you can't practice any other virtue consistently.-Maya Angelou",\
        "Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that.-Martin Luther King Jr.",\
        "Defeat is a state of mind; no one is ever defeated until defeat is accepted as a reality.-Bruce Lee",\
        "Develop success from failures. Discouragement and failure are two of the surest stepping stones to success.-Dale Carnegie",\
        "Do not stop thinking of life as an adventure. You have no security unless you can live bravely, excitingly, imaginatively; unless you can choose a challenge instead of competence.-Eleanor Roosevelt",\
        "Do not wait for the perfect time and place to enter, for you are already onstage.-Unknown",\
        "Do one thing every day that scares you.-Eleanor Roosevelt",\
        "Do something today that your future self will thank you for.-Unknown",\
        "Do the best you can. No one can do more than that.-John Wooden",\
        "Do what you can, with what you have, where you are.-Theodore Roosevelt",\
        "Do what you feel in your heart to be right_for you’ll be criticized anyway.-Eleanor Roosevelt",\
        "Don’t be afraid to give up the good to go for the great.-John D. Rockefeller",\
        "Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart.-Roy T. Bennett",\
        "Don’t be upset when people reject you. Nice things are rejected all the time by people who can’t afford them.-Unknown",\
        "Don’t compare yourself to others. Be like the sun and the moon and shine when it’s your time.-Unknown",\
        "Don’t dream about success. Get out there and work for it.-Unknown",\
        "Don’t give up, don’t take anything personally, and don’t take no for an answer.-Sophia Amoruso",\
        "Don’t let what you can’t do interfere with what you can do.-Unknown",\
        "Don’t let yesterday take up too much of today.-Will Rogers",\
        "Don’t limit your challenges. Challenge your limits.-Unknown",\
        "Don’t limit yourself. Many people limit themselves to what they think they can do. You can go as far as your mind lets you. What you believe, remember, you can achieve.-Mary Kay Ash",\
        "Don’t quit yet, the worst moments are usually followed by the most beautiful silver linings. You have to stay strong, remember to keep your head up and remain hopeful.-Unknown",\
        "Don’t say you don’t have enough time. You have exactly the same number of hours per day that were given to Helen Keller, Pasteur, Michelangelo, Mother Teresa, Leonardo da Vinci, Thomas Jefferson, and Albert Einstein.-H. Jackson Brown Jr.",\
        "Don’t stop when you are tired. Stop when you are done.-Unknown",\
        "Don’t tell everyone your plans, instead show them your results.-Unknown",\
        "Don’t tell people about your dreams. Show them your dreams.-Unknown",\
        "Don’t think or judge, just listen.-Sarah Dessen, Just Listen",\
        "Don’t watch the clock; do what it does. Keep going.-Sam Levenson",\
        "Don’t worry about failure; you only have to be right once.-Drew Houston",\
        "Don't bunt. Aim out of the ballpark. Aim for the company of immortals.-David Ogilvy",\
        "Don't let someone else's opinion of you become your reality.-Les Brown",\
        "Don't look at your feet to see if you are doing it right. Just dance.-Anne Lamott",\
        "Don't settle for average. Bring your best to the moment. Then, whether it fails or succeeds, at least you know you gave all you had.-Angela Bassett",\
        "Doubt is a killer. You just have to know who you are and what you stand for.-Jennifer Lopez",\
        "Doubt kills more dreams than failure ever will.-Suzy Kassem",\
        "Dreams are the seeds of change. Nothing ever grows without a seed, and nothing ever changes without a dream.-Debby Boone",\
        "Dreams don’t work unless you do.-John C. Maxwell",\
        "Dwell on the beauty of life. Watch the stars, and see yourself running with them.-Marcus Aurelius",\
        "Education is the most powerful weapon you can use to change the world.-Nelson Mandela",\
        "Either you run the day, or the day runs you.-Jim Rohn",\
        "Even if you’re on the right track, you’ll get run over if you just sit there.-Will Rogers",\
        "Every champion was once a contender that didn’t give up.-Gabby Douglas",\
        "Every strike brings me closer to the next home run.-Babe Ruth",\
        "Every successful person in the world is a hustler one way or another. We all hustle to get where we need to be. Only a fool would sit around and wait on another man to feed him.-K’wan",\
        "Everyone has inside them a piece of good news. The good news is you don’t know how great you can be! How much you can love! What you can accomplish! And what your potential is.-Anne Frank",\
        "Everyone thinks of changing the world, but no one thinks of changing himself.-Leo Tolstoy",\
        "Everything comes to him who hustles while he waits.-Thomas Edison",\
        "Everything is hard before it is easy.-Goethe",\
        "Everything you can imagine is real.-Pablo Picasso",\
        "Everything you've ever wanted is sitting on the other side of fear.-George Addair",\
        "Experience is a hard teacher because she gives the test first, the lesson afterwards.-Vernon Sanders Law",\
        "Failure is simply the opportunity to begin again, this time more intelligently.-Henry Ford",\
        "Failure isn’t the end of the road. It’s a big red flag saying to you ‘Wrong way. Turn around.-Oprah Winfrey",\
        "Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten.-Neil Gaiman",\
        "Falling down is how we grow. Staying down is how we die.-Brian Vaszily",\
        "Fear of what other people will think is the single most paralyzing dynamic in business and in life. The best moment of my life was the day I realized that I no longer give a damn what anybody thinks. That’s enormously liberating and freeing, and it’s the only way to live your life and do your business.-Cindy Gallop",\
        "First forget inspiration. Habit is more dependable. Habit will sustain you whether you're inspired or not. Habit will help you finish and polish your stories. Inspiration won't. Habit is persistence in practice.-Octavia Butler",\
        "Focus on being productive instead of busy.-Tim Ferriss",\
        "For the great doesn’t happen through impulse alone, and is a succession of little things that are brought together.-Vincent van Gogh",\
        "Forget your excuses. You either want it bad or don’t want it at all.-Unknown",\
        "Fortune favors the bold.-Virgil",\
        "Get a good idea and stay with it. Dog it, and work at it until it’s done right.-Walt Disney",\
        "Go the extra mile. It’s never crowded there.-Dr. Wayne D. Dyer",\
        "Goal setting is the secret to a compelling future.-Tony Robbins",\
        "Good. Better. Best. Never let it rest. ’Til your good is better and your better is best.-St. Jerome.",\
        "Great things are done by a series of small things brought together.-Vincent Van Gogh",\
        "Greatness only comes before hustle in the dictionary.-Ross Simmonds",\
        "H.O.P.E. = Hold On. Pain Ends.-Nitya Prakash",\
        "Happiness is not something ready made. It comes from your own actions.-Dalai Lama XIV",\
        "Hard work beats talent when talent doesn’t work hard.-Tim Notke",\
        "He that can have patience can have what he will.-Benjamin Franklin",\
        "Hold the vision, trust the process.-Unknown",\
        "How to stop time: kiss. How to travel in time: read. How to escape time: music. How to feel time: write. How to release time: breathe.-Matt Haig",\
        "How wonderful it is that nobody need wait a single moment before starting to improve the world.-Anne Frank",\
        "Hustle beats talent when talent doesn’t hustle.-Ross Simmonds",\
        "Hustle in silence and let your success make the noise.-Unknown",\
        "Hustlers don’t sleep, they nap.-Unknown",\
        "I always did something I was a little not ready to do. I think that’s how you grow. When there’s that moment of ‘Wow, I’m not really sure I can do this’ and you push through those moments, that’s when you have a breakthrough.-Marissa Mayer",\
        "I always wanted to be somebody, but now I realise I should have been more specific.-Lily Tomlin",\
        "I am not a product of my circumstances. I am a product of my decisions.-Stephen R. Covey",\
        "I am so clever that sometimes I don’t understand a single word of what I am saying.-Oscar Wilde",\
        "I am thankful for all of those who said no to me. It’s because of them I’m doing it myself.-Wayne W. Dyer",\
        "I attribute my success to this: I never gave or took an excuse.-Florence Nightingale",\
        "I can and I will. Watch me.-Carrie Green",\
        "I can be changed by what happens to me. But I refuse to be reduced by it.-Maya Angelou, Letter to My Daughter",\
        "I can’t tell you how many times I’ve been given a no. Only to find that a better, brighter, bigger yes was right around the corner.-Arlan Hamilton",\
        "I choose to make the rest of my life the best of my life.-Louise Hay",\
        "I could build a castle out of all the bricks they threw at me.-New Romantics, Taylor Swift",\
        "I didn’t get there by wishing for it, but by working for it.-Estée Lauder",\
        "I didn’t learn to be quiet when I had an opinion. The reason they knew who I was is because I told them.-Ursula Burns",\
        "I do not try to dance better than anyone else. I only try to dance better than myself.-Arianna Huffington",\
        "I find television very educational. Every time someone turns it on, I go in the other room and read a book.-Groucho Marx",\
        "I hated every minute of training, but I said, ‘Don’t quit. Suffer now and live the rest of your life as a champion.-Muhammad Ali",\
        "I have never let my schooling interfere with my education.-Mark Twain",\
        "I have not failed. I've just found 10,000 ways that won't work.-Thomas A. Edison",\
        "I have stood on a mountain of no’s for one yes.-Barbara Elaine Smith",\
        "I invite everyone to choose forgiveness rather than division, teamwork over personal ambition.-Jean-Francois Cope",\
        "I learned a long time ago that there is something worse than missing the goal, and that’s not pulling the trigger.-Mia Hamm",\
        "I never dreamed about success. I worked for it.-Estée Lauder",\
        "I never look back, darling. It distracts from the now.-Edna Mode",\
        "I never lose. Either I win or learn.-Nelson Mandela",\
        "I now tried a new hypothesis: It was possible that I was more in charge of my happiness than I was allowing myself to be.-Michelle Obama",\
        "I think it’s intoxicating when somebody is so unapologetically who they are.-Don Cheadle",\
        "I wake up every morning and think to myself, ‘How far can I push this company in the next 24 hours.-Leah Busque",\
        "I want to be remembered as the one who tried.-Dr. Dorothy Height",\
        "I will not erase all my hard work this week because it’s the weekend.-Unknown",\
        "I will not lose, for even in defeat, there’s a valuable lesson learned, so it evens up for me.-Jay-Z",\
        "I’d rather regret the things I’ve done than regret the things I haven’t done.-Lucille Ball",\
        "I’m a greater believer in luck, and I find the harder I work the more I have of it.-Thomas Jefferson",\
        "I’m not a product of my circumstances. I am a product of my decisions.-Stephen Covey",\
        "I’m still learning.-Michelangelo",\
        "I’ve missed more than 9,000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life, and that is why I succeed.-Michael Jordan",\
        "Ideation without execution is delusion.-Robin Sharma",\
        "If at first you don’t succeed, then skydiving isn’t for you.-Steven Wright",\
        "If everything seems to be under control, you’re not going fast enough.-Mario Andretti",\
        "If it makes you nervous, you’re doing it right.-Childish Gambino",\
        "If it’s a good idea, go ahead and do it. It’s much easier to apologize than it is to get permission.-Grace Hopper",\
        "If opportunity doesn’t knock, build a door.-Kurt Cobain",\
        "If people are doubting how far you can go, go so far that you can’t hear them anymore.-Michele Ruiz",\
        "If something is important enough, even if the odds are stacked against you, you should still do it.-Elon Musk",\
        "If the decisions you make about where you invest your blood, sweat, and tears are not consistent with the person you aspire to be, you’ll never become that person.-Clayton M. Christensen",\
        "If the highest aim of a captain were to preserve his ship, he would keep it in port forever.-Thomas Aquinas",\
        "If there is no struggle, there is no progress.-Frederick Douglass",\
        "If there is no wind, row.-Latin Proverb",\
        "If we have the attitude that it’s going to be a great day it usually is.-Catherine Pulsifier",\
        "If we take care of the moments, the years will take care of themselves.-Maria Edgeworth",\
        "If you are working on something that you really care about, you don’t have to be pushed. The vision pulls you.-Steve Jobs",\
        "If you believe it’ll work out, you’ll see opportunities. If you don’t believe it’ll work out, you’ll see obstacles.-Wayne Dyer",\
        "If you believe something needs to exist, if it's something you want to use yourself, don't let anyone ever stop you from doing it.-Tobias Lütke",\
        "If you can dream it, you can do it.-Walt Disney",\
        "If you can’t do anything about it then let it go. Don’t be a prisoner to things you can’t change.-Tony Gaskins",\
        "If you cannot do great things, do small things in a great way.-Napoleon Hill",\
        "If you can't yet do great things, do small things in a great way.-Napoleon Hill",\
        "If you change the way you look at things, the things you look at change.-Wayne Dyer",\
        "If you don’t get out of the box you’ve been raised in, you won’t understand how much bigger the world is.-Angelina Jolie",\
        "If you don’t have a competitive advantage, don’t compete.-Jack Welch",\
        "If you don’t like the road you’re walking, start paving another one.-Dolly Parton",\
        "If you don’t risk anything, you risk even more.-Erica Jong",\
        "If you fall. I’ll be there.-Floor",\
        "If you hear a voice within you say, ‘You cannot paint,’ then by all means paint, and that voice will be silenced.-Vincent Van Gogh",\
        "If you hire people just because they can do a job, they’ll work for your money. But if you hire people who believe what you believe, they’ll work for you with blood and sweat and tears.-Simon Sinek",\
        "If you judge people, you have no time to love them.-Mother Teresa",\
        "If you obey all the rules, you miss all the fun.-Katharine Hepburn",\
        "If you really want to do something, you'll find a way. If you don't, you'll find an excuse.-Jim Rohn",\
        "If you talk about it, it’s a dream. If you envision it, it’s possible. If you schedule it, it’s real.-Tony Robbins",\
        "If you think you’re too small to make a difference, try sleeping with a mosquito.-Dalai Lama",\
        "If you want to fly, give up everything that weighs you down.-Buddha",\
        "If you work on something a little bit every day, you end up with something that is massive.-Kenneth Goldsmith",\
        "If you’re not positive energy, you’re negative energy.-Mark Cuban",\
        "If you’re offered a seat on a rocket ship, don’t ask what seat! Just get on.-Sheryl Sandberg",\
        "If you’re the smartest person in the room, you’re in the wrong room.-Unknown",\
        "If you’re too comfortable, it’s time to move on. Terrified of what’s next_You’re on the right track.-Susan Fales-Hill",\
        "If you’ve never eaten while crying, you don’t know what life tastes like.-Johann Wolfgang von Goethe",\
        "Impossible is just an opinion.-Paulo Coelho",\
        "In a gentle way, you can shake the world.-Mahatma Gandhi",\
        "In order to be irreplaceable, one must always be different.-Coco Chanel",\
        "In the middle of every difficulty lies opportunity.-Albert Einstein",\
        "Individual commitment to a group effort_that is what makes a team work, a company work, a society work, a civilisation work.-Vince Lombardi",\
        "Inspiration does exist, but it must find you working.-Pablo Picasso",\
        "Invest in your dreams. Grind now. Shine later.-Unknown",\
        "It is a rough road that leads to the heights of greatness.-Lucius Annaeus Seneca",\
        "It is better to fail in originality than to succeed in imitation.-Herman Melville",\
        "It is impossible to live without failing at something, unless you live so cautiously that you might as well not have lived at all_in which case, you fail by default.-J.K. Rowling",\
        "It is never too late to be what you might have been.-George Eliot",\
        "It is only when we take chances, when our lives improve. The initial and the most difficult risk that we need to take is to become honest.-Walter Anderson",\
        "It is remarkable how much long_term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent.-Charlie Munger",\
        "It might not be easy, but it’ll be worth it.-Unknown",\
        "It takes nothing to join the crowd. It takes everything to stand alone.-Hans F. Hansen",\
        "It’s a new dawn, it’s a new day, it’s a life for me and I’m feeling good.-Feeling Good, Michael Bublé",\
        "It’s better to be absolutely ridiculous than absolutely boring.-Marilyn Monroe",\
        "It’s hard to beat a person who never gives up.-Babe Ruth",\
        "It’s my life. It’s now or never. I ain’t gonna live forever. I just want to live while I’m alive.-It’s My Life, Bon Jovi",\
        "It’s never too late for a new beginning in your life.-Joyce Meyers",\
        "It’s never too late to be what you might’ve been.-George Eliot",\
        "It’s no use going back to yesterday, because I was a different person then.-Lewis Carroll",\
        "It’s not about better time management. It’s about better life management.-Alexandra of The Productivity Zone",\
        "It’s not about having enough time, it’s about making enough time.-Rachael Bermingham",\
        "It’s not all sunshine and rainbows, but a good amount of it actually is.-Unknown",\
        "It’s not the load that breaks you down, it’s the way you carry it.-Lou Holtz",\
        "It’s not the will to win that matters_everyone has that. It’s the will to prepare to win that matters.-Paul Bryant",\
        "It’s not what you do once in a while, it's what you do day in and day out that makes the difference.-Jenny Craig",\
        "It’s not your salary that makes you rich, it’s your spending habits.-Charles A. Jaffe",\
        "It’s OK to outgrow people who don’t grow. Grow tall anyways.-Unknown",\
        "It’s the possibility of having a dream come true that makes life interesting.-Paulo Coelho, The Alchemist",\
        "It's fine to celebrate success but it is more important to heed the lessons of failure.-Bill Gates",\
        "I've searched all the parks in all the cities and found no statues of committees.-Gilbert K. Chesterton",\
        "Just because it burns doesn’t mean you’re gonna die you’ve gotta get up and try.-Try, Pink",\
        "Just one small positive thought in the morning can change your whole day.-Dalai Lama",\
        "Keep a little fire burning; however small, however hidden.-Cormac McCarthy",\
        "Keep your eyes on the stars, and your feet on the ground.-Theodore Roosevelt",\
        "Keep your face always toward the sunshine_and shadows will fall behind you.-Walt Whitman",\
        "Leaders can let you fail and yet not let you be a failure.-Stanley McChrystal",\
        "Learn as if you will live forever, live like you will die tomorrow.-Mahatma Gandhi",\
        "Learn to light a candle in the darkest moments of someone’s life. Be the light that helps others see; it is what gives life its deepest significance.-Roy T. Bennett, The Light in the Heart",\
        "Life can be much broader once you discover one simple fact: Everything around you that you call life was made up by people that were no smarter than you. And you can change it, you can influence it… Once you learn that, you'll never be the same again.-Steve Jobs",\
        "Life is 10% what happens to you and 90% how you react to it.-Charles R. Swindoll",\
        "Life is either a daring adventure or nothing at all.-Helen Keller",\
        "Life is like a sewer… what you get out of it depends on what you put into it.-Tom Lehrer",\
        "Life is like riding a bicycle. To keep your balance, you must keep moving.-Albert Einstein",\
        "Life is not what you alone make it. Life is the input of everyone who touched your life and every experience that entered it. We are all part of one another.-Yuri Kochiyama",\
        "Life’s a game made for everyone and love is the prize.-Wake Me Up, Avicii",\
        "Life’s like a movie, write your own ending. Keep believing, keep pretending.-Jim Henson",\
        "Live as if you were to die tomorrow. Learn as if you were to live forever.-Mahatma Gandhi",\
        "Live out of your imagination, not your history.-Stephen Covey",\
        "Losers quit when they fail. Winners fail until they succeed.-Robert T. Kiyosaki",\
        "Love your family, work super hard, live your passion.-Gary Vaynerchuk",\
        "Magic is believing in yourself. If you can make that happen, you can make anything happen.-Johann Wolfgang Von Goethe",\
        "Make each day your masterpiece.-John Wooden",\
        "Make sure your worst enemy doesn’t live between your own two ears.-Laird Hamilton",\
        "Make your fear of losing your greatest motivator.-Unknown",\
        "More is lost by indecision than wrong decision.-Marcus Tullius Cicero",\
        "Motivation may be what starts you off, but it’s habit that keeps you going back for more.-Miya Yamanouchi",\
        "Nature has given us all the pieces required to achieve exceptional wellness and health, but has left it to us to put these pieces together.-Diane McLaren",\
        "Never allow a person to tell you no who doesn’t have the power to say yes.-Eleanor Roosevelt",\
        "Never doubt that a small group of thoughtful, committed, citizens can change the world. Indeed, it is the only thing that ever has.-Margaret Mead",\
        "Never give up on a dream just because of the time it will take to accomplish it. The time will pass anyway.-Earl Nightingale",\
        "Never let anyone treat you like you’re regular glue. You’re glitter glue.-Unknown",\
        "Never let success get to your head and never let failure get to your heart.-Drake",\
        "Never regret a day in your life. Good days bring you happiness and bad days give you experience.-Unknown",\
        "Never regret anything that made you smile.-Mark Twain",\
        "Never stop doing your best just because someone doesn’t give you credit.-Kamari a.k.a. Lyrikal",\
        "Never stop learning because life never stops teaching.-Unknown",\
        "No matter what people tell you, words and ideas can change the world.-Robin Williams",\
        "No one changes the world who isn’t obsessed.-Billie Jean King",\
        "No one is to blame for your future situation but yourself. If you want to be successful, then become ‘Successful.-Jaymin Shah",\
        "Nothing can dim the light that shines from within.-Maya Angelou",\
        "Nothing ever goes away until it teaches us what we need to know.-Pema Chodron",\
        "Nothing in the world can take the place of Persistence. Talent will not; nothing is more common than unsuccessful men with talent. Genius will not; unrewarded genius is almost a proverb. Education will not; the world is full of educated derelicts. The slogan 'Press On' has solved and always will solve the problems of the human race.-Calvin Coolidge",\
        "Nothing will work unless you do.-Maya Angelou",\
        "Once you do know what the question actually is, you’ll know what the answer means.-Douglas Adams",\
        "One of the differences between some successful and unsuccessful people is that one group is full of doers, while the other is full of wishers.-Edmond Mbiaka",\
        "One thing’s for sure, if you don’t play, you don’t win.-Kylie Francis",\
        "Only do what your heart tells you.-Princess Diana",\
        "Only I can change my life. No one can do it for me.-Carol Burnett",\
        "Only the paranoid survive.-Andy Grove",\
        "Opportunities don't happen, you create them.-Chris Grosser",\
        "Opportunity does not knock, it presents itself when you beat down the door.-Kyle Chandler",\
        "Opportunity is missed by most people because it is dressed in overalls and looks like work.-Thomas Edison",\
        "Optimism is the faith that leads to achievement. Nothing can be done without hope and confidence.-Helen Keller",\
        "Our greatest glory is not in never falling, but in rising every time we fall.-Confucius",\
        "People often say that motivation doesn’t last. Well, neither does bathing – that’s why we recommend it daily.-Zig Ziglar",\
        "People say nothing is impossible, but I do nothing every day.-Winnie the Pooh",\
        "People who wonder if the glass is half empty or full miss the point. The glass is refillable.-Unknown",\
        "People’s passion and desire for authenticity is strong.-Constance Wu",\
        "Perfection is not attainable. But if we chase perfection we can catch excellence.-Vince Lombardi",\
        "Punctuality is not just limited to arriving at a place at the right time, it is also about taking actions at the right time.-Amit Kalantri",\
        "Quitters never win. Winners never quit!-Dr. Irene C. Kassorla",\
        "Relentlessly prune bullshit, don't wait to do things that matter, and savor the time you have. That's what you do when life is short.-Paul Graham",\
        "Remember, teamwork begins by building trust. And the only way to do that is to overcome our need for invulnerability.-Patrick Lencioni",\
        "Resilience is when you address uncertainty with flexibility.-Unknown",\
        "Revenge is a powerful motivator.-Marcus Luttrell",\
        "Rivers know this: there is no hurry. We shall get there some day.-A.A. Milne",\
        "Set your goals high, and don’t stop till you get there.-Bo Jackson",\
        "Setting goals is the first step in turning the invisible into the visible.-Tony Robbins",\
        "She remembered who she was and the game changed.-Lalah Deliah",\
        "Show up, show up, show up, and after a while the muse shows up, too.-Isabel Allende",\
        "Small is not just a stepping_stone. Small is a great destination itself.-Jason Fried",\
        "Smart people learn from everything and everyone, average people from their experiences, stupid people already have all the answers.-Socrates",\
        "Some people want it to happen, some wish it would happen, others make it happen.-Michael Jordan",\
        "Someone will declare, I am the leader! and expect everyone to get in line and follow him or her to the gates of heaven or hell. My experience is that it doesn’t happen that way. Others follow you based on the quality of your actions rather than the magnitude of your declarations.-Bill Walsh",\
        "Someone's sitting in the shade today because someone planted a tree a long time ago.-Warren Buffet",\
        "Sometimes magic is just someone spending more time on something than anyone else might reasonably expect.-Raymond Joseph Teller",\
        "Sometimes when you’re in a dark place you think you’ve been buried but you’ve actually been planted.-Christine Caine",\
        "Somewhere, something incredible is waiting to be known.-Carl Sagan",\
        "Start where you are. Use what you have. Do what you can.-Arthur Ashe",\
        "Stay away from those people who try to disparage your ambitions. Small minds will always do that, but great minds will give you a feeling that you can become great too.-Mark Twain",\
        "Stop being afraid of what could go wrong, and start being excited about what could go right.-Tony Robbins",\
        "Success is a lousy teacher. It seduces smart people into thinking they can’t lose.-Bill Gates",\
        "Success is getting what you want, happiness is wanting what you get.-W. P. Kinsella",\
        "Success is going from failure to failure without losing your enthusiasm.-Winston Churchill",\
        "Success is liking yourself, liking what you do, and liking how you do it.-Maya Angelou",\
        "Success is no accident. It is hard work, perseverance, learning, studying, sacrifice and most of all, love of what you are doing or learning to do.-Pele",\
        "Success is not final; failure is not fatal: It is the courage to continue that counts.-Winston S. Churchill",\
        "Success is peace of mind, which is a direct result of self_satisfaction in knowing you made the effort to become the best of which you are capable.-John Wooden",\
        "Success is stumbling from failure to failure with no loss of enthusiasm.-Winston Churchill",\
        "Success usually comes to those who are too busy looking for it.-Henry David Thoreau",\
        "Successful people are not gifted; they just work hard, then succeed on purpose.-G.K. Nielson",\
        "Sunshine all the time makes a desert.-Arabic proverb",\
        "Take criticism seriously, but not personally. If there is truth or merit in the criticism, try to learn from it. Otherwise, let it roll right off you.-Hillary Clinton",\
        "Take the risk or lose the chance.-Unknown",\
        "Take your victories, whatever they may be, cherish them, use them, but don’t settle for them.-Mia Hamm",\
        "Talent wins games, but teamwork and intelligence win championships.-Michael Jordan",\
        "Teamwork is the ability to work together toward a common vision. The ability to direct individual accomplishments toward organizational objectives. It is the fuel that allows common people to attain uncommon results.-Andrew Carnegie",\
        "The adventure of life is to learn. The purpose of life is to grow. The nature of life is to change. The challenge of life is to overcome. The essence of life is to care. The opportunity of life is to serve. The secret of life is to dare. The spice of life is to befriend. The beauty of life is to give.-William Arthur Ward",\
        "The battles that count aren't the ones for gold medals. The struggles within yourself_the invisible, inevitable battles inside all of us_that's where it's at.-Jesse Owens",\
        "The best revenge is massive success.-Frank Sinatra",\
        "The best time to plant a tree was 20 years ago. The second best time is now.-Chinese Proverb",\
        "The best way out is always through.-Robert Frost",\
        "The best way to appreciate your job is to imagine yourself without one.-Oscar Wilde",\
        "The best way to predict your future is to create it.-Abraham Lincoln",\
        "The big lesson in life, baby, is never be scared of anyone or anything.-Frank Sinatra",\
        "The big secret in life is that there is no secret. Whatever your goal, you can get there if you’re willing to work.-Oprah Winfrey",\
        "The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice.-Brian Herbert",\
        "The Courage doesn't always roar. Sometimes courage is a quiet voice at the end of the day saying, I will try again tomorrow.-Mary Anne Radmacher",\
        "The difference between successful people and very successful people is that very successful people say no to almost everything.-Warren Buffett",\
        "The difference between who you are and who you want to be is what you do.-Unknown",\
        "The elevator to success is out of order. You’ll have to use the stairs, one step at a time.-Joe Girard",\
        "The greater the difficulty, the more the glory in surmounting it.-Epicurus",\
        "The greatest discovery of my generation is that a human being can alter his life by altering his attitudes.-William James",\
        "The greatest gift you could give someone is your time. Because when you give your time, you are giving a portion of your life you can’t get back.-Unknown",\
        "The greatest weapon against stress is the ability to choose one thought over another.-William James",\
        "The hard days are what make you stronger.-Aly Raisman",\
        "The key to success is to start before you are ready.-Marie Forleo",\
        "The man who does not read has no advantage over the man who cannot read.-Mark Twain",\
        "The miracle is not that we do this work, but that we are happy to do it.-Mother Teresa",\
        "The only difference between ordinary and extraordinary is that little extra.-Jimmy Johnson",\
        "The only one who can tell you you can’t win is you and you don’t have to listen.-Jessica Ennis",\
        "The only thing standing in the way between you and your goal is the BS story you keep telling yourself as to why you can’t achieve it.-Jordan Belfort",\
        "The only way of discovering the limits of the possible is to venture a little way past them into the impossible.-Arthur C. Clarke",\
        "The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.-Winston Churchill",\
        "The question isn't who is going to let me; it's who is going to stop me.-Ayn Rand",\
        "The reason we struggle with insecurity is because we compare our behind the scenes with everyone else’s highlight reel.-Steve Furtick",\
        "The road to success and the road to failure are almost exactly the same.-Colin R. Davis",\
        "The same boiling water that softens the potato hardens the egg. It’s what you’re made of. Not the circumstances.-Unknown",\
        "The secret of change is to focus all your energy, not on fighting the old, but on building the new.-Socrates",\
        "The secret of getting ahead is getting started.-Mark Twain",\
        "The secret of your future is hidden in your daily routine.-Mike Murdock",\
        "The standard you walk past, is the standard you accept.-David Hurley",\
        "The trouble is, you think you have time.-Buddha",\
        "The two most important days in your life are the day you’re born and the day you find out why.-Mark Twain",\
        "The woman who follows the crowd will usually go no further than the crowd. The woman who walks alone is likely to find herself in places no one has been before.-Albert Einstein",\
        "The world is full of nice people. If you can’t find one, be one.-Nishan Panwar",\
        "There are three ways to ultimate success: The first way is to be kind. The second way is to be kind. The third way is to be kind.-Mister Rogers",\
        "There are two rules for success: Never reveal everything you know.-Roger H. Lincoln",\
        "There is a vitality, a life force, an energy, a quickening that is translated through you into action, and because there is only one of you in all time, this expression is unique. And if you block it, it will never exist through any other medium and will be lost.-Martha Graham",\
        "There is some good in this world, and it’s worth fighting for.-J.R.R. Tolkien, The Two Towers",\
        "There may be people that have more talent than you, but there’s no excuse for anyone to work harder than you.-Derek Jeter",\
        "Think like a queen. A queen is not afraid to fail. Failure is another stepping stone to greatness.-Oprah Winfrey",\
        "This is a reminder to you to create your own rule book, and live your life the way you want it.-Reese Evans",\
        "This is the mark of a really admirable man: steadfastness in the face of trouble.-Ludwig Van Beethoven",\
        "Those who cannot change their minds cannot change anything.-George Bernard Shaw",\
        "Time always exposes what you mean to someone.-Unknown",\
        "Time is money.-Benjamin Franklin",\
        "Time is what we want most and what we use worst.-William Penn",\
        "To be a champion, I think you have to see the big picture. It’s not about winning and losing; it’s about every day hard work and about thriving on a challenge. It’s about embracing the pain that you’ll experience at the end of a race and not being afraid. I think people think too hard and get afraid of a certain challenge.-Summer Sanders",\
        "To know how much there is to know is the beginning of learning to live.-Dorothy West",\
        "To learn a language is to have one more window from which to look at the world.-Chinese Proverb",\
        "Today is where your book begins, the rest is still unwritten.-Unwritten, Natasha Bedingfield",\
        "Today is your opportunity to build the tomorrow you want.-Ken Poirot",\
        "True freedom is impossible without a mind made free by discipline.-Mortimer J. Adler",\
        "True humility is not thinking less of yourself; it is thinking of yourself less.-Unknown",\
        "Trust yourself that you can do it and get it.-Baz Luhrmann",\
        "Try not to become a man of success, but rather become a man of value.-Albert Einstein",\
        "Turn your wounds into wisdom.-Oprah Winfrey",\
        "Twenty years from now you’ll be more disappointed by the things you did not do than the ones you did.-Mark Twain",\
        "Unsuccessful people make their decisions based on their current situations. Successful people make their decisions based on where they want to be.-Benjamin Hardy",\
        "Very little is needed to make a happy life; it is all within yourself, in your way of thinking.-Marcus Aurelius",\
        "Very often, a change of self is needed more than a change of scene.-A.C. Benson",\
        "We are what we repeatedly do. Excellence, then, is not an act, but a habit.-Aristotle",\
        "We can do anything we want to if we stick to it long enough.-Helen Keller",\
        "We can see through others only when we can see through ourselves.-Bruce Lee",\
        "We cannot solve problems with the kind of thinking we employed when we came up with them.-Albert Einstein",\
        "We delight in the beauty of the butterfly, but rarely admit the changes it has gone through to achieve that beauty.-Maya Angelou",\
        "We must reach out our hand in friendship and dignity both to those who would befriend us and those who would be our enemy.-Arthur Ashe",\
        "We need to accept that we won’t always make the right decisions, that we’ll screw up royally sometimes – understanding that failure is not the opposite of success, it’s part of success.-Ariana Huffington",\
        "Wealth isn’t about having a lot of money, it's about having a lot of options.-Chris Rock",\
        "What defines us is how well we rise after falling.-Lionel from the movie Maid in Manhattan",\
        "What is coming is better than what is gone.-Unknown",\
        "What is life without a little risk.-J.K. Rowling",\
        "What you do makes a difference, and you have to decide what kind of difference you want to make.-Jane Goodall",\
        "What you do speaks so loudly that I cannot hear what you say.-Ralph Waldo Emerson",\
        "What’s on the other side of fear_Nothing.-Jamie Foxx",\
        "Whatever you are, be a good one.-Abraham Lincoln",\
        "Whatever you do, never run back to what broke you.-Frank Ocean",\
        "When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.-Henry Ford",\
        "When I believe in something, I’m like a dog with a bone.-Melissa McCarthy",\
        "When I win and when I lose, I take ownership of it, because I really am in charge of what I do.-Nicki Minaj",\
        "When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us.-Helen Keller",\
        "When Plan A doesn’t work, don’t worry, you still have 25 more letters to go through.-Unknown",\
        "When someone says you can’t do it, do it twice and take pictures.-Unknown",\
        "When the pain of an obstacle is too great, challenge yourself to be stronger.-Will Rogers",\
        "When thinking about life, remember this: no amount of guilt can change the past and no amount of anxiety can change the future.-Unknown",\
        "When we strive to become better than we are, everything around us becomes better too.-Paulo Coelho",\
        "When written in Chinese, the word ‘crisis’ is composed of two characters_one represents danger and the other represents opportunity.-John F. Kennedy",\
        "When you arise in the morning think of what a privilege it is to be alive, to think, to enjoy, to love…-Marcus Aurelius",\
        "When you change your thoughts, remember to also change your world.-Norman Vincent Peale",\
        "When you feel like giving up just remember that there are a lot of people you still have to prove wrong.-Unknown",\
        "When you give joy to other people, you get more joy in return. You should give a good thought to happiness that you can give out.-Eleanor Roosevelt",\
        "When you know your worth, no one can make you feel worthless.-Unknown",\
        "When you reach the end of your rope, tie a knot and hang out.-Abraham Lincoln",\
        "Whenever you find yourself doubting how far you can go, just remember how far you have come.-Unknown",\
        "Wherever you go, go with all your heart.-Confucius",\
        "Why do we grieve failures longer than we celebrate wins.-Komal Kapoor",\
        "Winning means you’re willing to go longer, work harder, and give more than anyone else.-Vince Lombardi",\
        "Without hustle, talent will only carry you so far.-Gary Vaynerchuk",\
        "Words can inspire, thoughts can provoke, but only action truly brings you closer to your dreams.-Brad Sugars",\
        "Work hard for what you want because it won’t come to you without a fight. You have to be strong and courageous and know that you can do anything you put your mind to. If somebody puts you down or criticizes you, just keep on believing in yourself and turn it into something positive.-Leah LaBelle",\
        "Work hard in silence, let your success be the noise.-Frank Ocean",\
        "Work like there is someone working 24 hours a day to take it away from you.-Mark Cuban",\
        "Work until your bank account looks like a phone number.-Unknown",\
        "Worry is a misuse of imagination.-Unknown",\
        "Would you like me to give you a formula for success. It’s quite simple, really: Double your rate of failure. You are thinking of failure as the enemy of success. But it isn’t at all. You can be discouraged by failure or you can learn from it, so go ahead and make mistakes. Make all you can. Because remember, that’s where you will find success.-Thomas J. Watson",\
        "Write it. Shoot it. Publish it. Crochet it. Sauté it. Whatever. MAKE.-Joss Whedon",\
        "Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.-Rumi",\
        "You can be the ripest, juiciest peach in the world, and there's still going to be somebody who hates peaches.-Dita Von Teese",\
        "You can cry, scream, and bang your head in frustration but keep pushing forward. It’s worth it.-Unknown",\
        "You can do anything you set your mind to.-Benjamin Franklin",\
        "You can either experience the pain of discipline or the pain of regret. The choice is yours.-Unknown",\
        "You can get everything in life you want if you will just help enough other people get what they want.-Zig Ziglar",\
        "You can never leave footprints that last if you are always walking on tiptoe.-Leymah Gbowee",\
        "You can waste your lives drawing lines. Or you can live your life crossing them.-Shonda Rhimes",\
        "You can’t be that kid standing at the top of the waterslide, overthinking it. You have to go down the chute.-Tina Fey",\
        "You can’t go back and change the beginning, but you can start where you are and change the ending.-C.S. Lewis",\
        "You can’t let your failures define you. You have to let your failures teach you.-Barack Obama",\
        "You cannot always control what goes on outside. But you can always control what goes on inside.-Wayne Dyer",\
        "You cannot plow a field by turning it over in your mind. To begin, begin.-Gordon B. Hinckley",\
        "You carry the passport to your own happiness.-Diane von Furstenberg",\
        "You could rattle the stars,’ she whispered. ‘You could do anything, if only you dared. And deep down, you know it, too. That’s what scares you most.-Sarah J. Maas",\
        "You don’t need to see the whole staircase, just take the first step.-Martin Luther King Jr.",\
        "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. You’re on your own. And you know what you know. And YOU are the one who’ll decide where to go …-Dr. Seuss, Oh, the Places You’ll Go!",\
        "You learn more from failure than from success. Don’t let it stop you. Failure builds character.-Unknown",\
        "You must do the kind of things you think you cannot do.-Eleanor Roosevelt",\
        "You must do the thing you think you cannot do.-Eleanor Roosevelt",\
        "You never know what you can do until you try.-William Cobbett",\
        "You were born to be a player. You were meant to be here. This moment is yours.-Herb Brooks",\
        "You were born to win, but to be a winner, you must plan to win, prepare to win, and expect to win.-Zig Ziglar",\
        "You will never always be motivated, so you must learn to be disciplined.-Unknown",\
        "You’ll never get bored when you try something new. There’s really no limit to what you can do.-Dr. Seuss",\
        "You’re off to Great Places! Today is your day! Your mountain is waiting, so … get on your way!-Dr. Seuss",\
        "You’re so much stronger than your excuses.-Unknown",\
        "You’ve got to get up every morning with determination if you’re going to go to bed with satisfaction.-George Lorimer",\
        "You’ve gotta dance like there’s nobody watching, love like you’ll never be hurt, sing like there’s nobody listening, and live like it’s heaven on earth.-William W. Purkey",\
        "Your mind is powerful. When you fill it with positive thoughts your whole world will change.-Unknown",\
        "Your only limit is your mind.-Unknown",\
        "Your passion is waiting for your courage to catch up.-Isabelle Lafleche",\
        "Your playing small does not serve the world. There is nothing enlightened about shrinking so that other people won’t feel insecure around you. We are all meant to shine, as children do.-Marianne Williamson",\
        "Your positive action combined with positive thinking results in success.-Shiv Khera",\
        "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. And the only way to do great work is to love what you do. If you haven’t found it yet, keep looking. Don’t settle. As with all matters of the heart, you’ll know when you find it.-Steve Jobs"]
        phrase=MSGlist[r]
        return phrase