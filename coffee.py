from RPi import GPIO
import sys
from guizero import App, Text, Box, Picture
from PIL import Image
from lib.hx711 import HX711
import time

# colors
color = '#262626'
bg = '#F4F4ee'
alert = '#ff7f11'
primary = '#4c956c'
secondary = '#1e91d6'

# recipe
water = 300
grounds = 60.5
relationshipWater = 16
lastRelationshipWater = 1

strengths = [12, 15, 18, 21]

# weight
referenceUnit1 = -980
hx1 = HX711(25,24)
hx1.set_reading_format("MSB", "MSB")
hx1.set_reference_unit(referenceUnit1)
hx1.reset()
hx1.tare()

referenceUnit2 = -980
hx2 = HX711(26,16)
hx2.set_reading_format("MSB", "MSB")
hx2.set_reference_unit(referenceUnit1)
hx2.reset()
hx2.tare()

#############
# GUI
#############
boldBeanImage = './bean.png'
lightBean = './bean_light.png'

app = App(title="Hello World", layout="grid", bg=bg)

targetLabel = Text(app, text="target", grid=[
                   0, 0], color=color, align='left')
amountText = Text(app, text='1/',
                  grid=[0, 1], color=color, align='left', size=30)
beanBox = Box(app, grid=[1, 1, 2, 1], border=0, layout='grid', align='right')

beanPicture1 = Picture(beanBox, image=boldBeanImage, grid=[0, 1])
beanPicture2 = Picture(beanBox, image=boldBeanImage, grid=[1, 1])
beanPicture3 = Picture(beanBox, image=boldBeanImage, grid=[2, 1])
beanPicture4 = Picture(beanBox, image=boldBeanImage, grid=[3, 1])
beanPicture5 = Picture(beanBox, image=lightBean, grid=[4, 1])

currentLabel = Text(app, text='Current', grid=[0, 2], color=color, align='left')
currentBeans = Text(app, text='', grid=[0, 3], color=color, align='left', size=30)
currentWater = Text(app, text='',
                    grid=[0, 4, 2, 1], color=color, align='left', size=30)
warning = Text(app, text='',
               grid=[0, 5, 2, 1], color=alert, align='left', visible=False)
strengthLabel = Text(app, text='Rotate to change Strength', grid=[0, 6], color=color, align='left')
resetLabel = Text(app, text='Press to tare',
                  grid=[0, 7], color=color, align='left')
slider = Box(app, grid=[
    2, 2, 2, 7], border=1, width=17, height=100, align='right')
sliderContent = Box(slider, width=15, height=1,
                    border=0, align='bottom')
sliderContent.bg = secondary
slider.set_border(1, primary)

def processRelationship():
    global lastRelationshipWater
    amountText.value = ('1/' + str(relationshipWater))
    if(lastRelationshipWater != relationshipWater):
        lastRelationshipWater = relationshipWater
        if relationshipWater < strengths[0]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = boldBeanImage
            beanPicture4.image = boldBeanImage
            beanPicture5.image = boldBeanImage
        if relationshipWater >= strengths[0]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = boldBeanImage
            beanPicture4.image = boldBeanImage
            beanPicture5.image = lightBean
        if relationshipWater >= strengths[1]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = boldBeanImage
            beanPicture4.image = lightBean
            beanPicture5.image = lightBean
        if relationshipWater >= strengths[2]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = lightBean
            beanPicture4.image = lightBean
            beanPicture5.image = lightBean
        if relationshipWater >= strengths[3]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = lightBean
            beanPicture3.image = lightBean
            beanPicture4.image = lightBean
            beanPicture5.image = lightBean


def processRecipe(w):
    global water
    global waterTarget

    water = w
    waterTarget = grounds * relationshipWater
    if water < 0 and water > -0.2:
        waterDisplayValue = 0.0
    else:
        waterDisplayValue = str(round(water, 1))

    if water > 0:
        sliderContent.height = water / waterTarget * 100

    
    currentBeans.value = str(grounds) + 'g beans'
    currentWater.value = str(waterDisplayValue)+'ml/ ' + str(waterTarget)+'ml water'

    if waterTarget > 1250:
        warning.value = 'Warning: Too much water for the Moccamaster'
        warning.visible = True
    if grounds > 70:
        warning.value = 'Warning: Too much grounds for the Moccamaster'
        warning.visible = True
    if grounds < 71 and waterTarget < 1251:
        warning.visible = False


processRelationship()


#############
# rotary
#############

clk = 22
dt = 23
sw = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


clkLastState = GPIO.input(clk)
dtLastState = GPIO.input(dt)
swLastState = GPIO.input(sw)

def clkClicked(chanel):
    global relationshipWater
    global clkLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    
    if clkState == 0 and dtState == 1:
        relationshipWater += 1
        processRelationship()
    clkLastState = clkState    
        
def dtClicked(chanel):
    global relationshipWater
    global dtLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    
    if clkState == 1 and dtState == 0:
        relationshipWater -= 1
        processRelationship()
    dtLastState = dtState
    
def swClicked(chanel):
    warning.value = 'Tare...'
    warning.visible = True
    hx1.tare()
    warning.visible = False

GPIO.add_event_detect(clk, GPIO.FALLING, callback=clkClicked, bouncetime=100)
GPIO.add_event_detect(dt, GPIO.FALLING, callback=dtClicked, bouncetime=100)
GPIO.add_event_detect(sw, GPIO.FALLING, callback=swClicked, bouncetime=500)

#############
# water scale
#############

def getWeight(callback):
        try:
            
            val = hx1.get_weight(5)
            val2 = hx2.get_weight(5)
            callback('hx1: ' + str(val) + 'hx2: ' + str(val2)   )
            
        except (KeyboardInterrupt, SystemExit):
            currentWater.value = 'unknown'

currentWater.repeat(500, getWeight, [processRecipe])
    

#############
# Finish
#############

app.display()

GPIO.cleanup()
