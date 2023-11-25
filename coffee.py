from RPi import GPIO
import sys
from guizero import App, Text, Box, Picture
from PIL import Image
from gui import beanContainer, strength, beanWeight, waterCan, waterWeight
from lib.hx711 import HX711
import time

# colors
color = '#262626'
bg = '#F4F4ee'
alert = '#ff7f11'
primary = '#4c956c'
secondary = '#1e91d6'
textSize = 40

# recipe
water = 300
grounds = 60.5
relationshipWater = 16
lastRelationshipWater = 1

strengths = [12, 15, 18, 21]

# weight
referenceUnit1 = -980
hx1 = HX711(26, 16)
hx1.set_reading_format("MSB", "MSB")
hx1.set_reference_unit(referenceUnit1)
hx1.reset()
hx1.tare()

#############
# GUI
#############
# boldBeanImage = './bean.png'
# lightBean = './bean_light.png'
app = App(title="Hello World", layout="auto", bg=bg, width=1024, height=600)
app.full_screen = True
currentPage = 'beanContainer'

beanContainer = beanContainer.getBeanContainer(app, textSize)
strength = strength.getStrength(app, textSize)
beanWeightBox = beanWeight.getBeanWeight(app, textSize)
waterCan = waterCan.getWaterCan(app, textSize)
waterWeight = waterWeight.getWaterWeight(app, textSize)


beanContainer.visible = True

# targetLabel = Text(app, text="target", grid=[
#    0, 0], color=color, align='left')
# amountText = Text(app, text='1/',
#   grid=[0, 1], color=color, align='left', size=30)
# beanBox = Box(app, grid=[1, 1, 2, 1], border=0, layout='grid', align='right')

# beanPicture1 = Picture(beanBox, image=boldBeanImage, grid=[0, 1])
# beanPicture2 = Picture(beanBox, image=boldBeanImage, grid=[1, 1])
# beanPicture3 = Picture(beanBox, image=boldBeanImage, grid=[2, 1])
# beanPicture4 = Picture(beanBox, image=boldBeanImage, grid=[3, 1])
# beanPicture5 = Picture(beanBox, image=lightBean, grid=[4, 1])

# currentLabel = Text(app, text='Current', grid=[0, 2], color=color, align='left')
# currentBeans = Text(app, text='', grid=[0, 3], color=color, align='left', size=30)
# currentWater = Text(app, text='',
# grid=[0, 4, 2, 1], color=color, align='left', size=30)
# warning = Text(app, text='',
#    grid=[0, 5, 2, 1], color=alert, align='left', visible=False)
# strengthLabel = Text(app, text='Rotate to change Strength', grid=[0, 6], color=color, align='left')
# resetLabel = Text(app, text='Press to tare',
#   grid=[0, 7], color=color, align='left')
# slider = Box(app, grid=[
# 2, 2, 2, 7], border=1, width=17, height=100, align='right')
# sliderContent = Box(slider, width=15, height=1,
# border=0, align='bottom')
# sliderContent.bg = secondary
# slider.set_border(1, primary)


def processRelationship():
    global lastRelationshipWater
    amountText.value = ('1/' + str(relationshipWater))
    if (lastRelationshipWater != relationshipWater):
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
    currentWater.value = str(waterDisplayValue) + \
        'ml/ ' + str(waterTarget)+'ml water'

    if waterTarget > 1250:
        warning.value = 'Warning: Too much water for the Moccamaster'
        warning.visible = True
    if grounds > 70:
        warning.value = 'Warning: Too much grounds for the Moccamaster'
        warning.visible = True
    if grounds < 71 and waterTarget < 1251:
        warning.visible = False


# processRelationship()


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


# clkLastState = GPIO.input(clk)
# dtLastState = GPIO.input(dt)
# swLastState = GPIO.input(sw)

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
    global currentPage
    if (currentPage == "beanContainer"):
        beanContainer.visible = False
        strength.visible = True
        currentPage = "strength"
    elif (currentPage == "strength"):
        strength.visible = False
        beanWeightBox.visible = True
        currentPage = "beanWeight"

    elif (currentPage == "beanWeight"):
        beanWeightBox.visible = False
        waterCan.visible = True
        currentPage = "waterCan"

    elif (currentPage == "waterCan"):
        waterCan.visible = False
        waterWeight.visible = True
        currentPage = "waterWeight"

    elif (currentPage == "waterWeight"):
        waterWeight.visible = False
        beanContainer.visible = True
        currentPage = "beanContainer"
    print(currentPage)
# warning.value = 'Tare...'
    # warning.visible = True
    # hx1.tare()
    # warning.visible = False


# GPIO.add_event_detect(clk, GPIO.FALLING, callback=clkClicked, bouncetime=100)
# GPIO.add_event_detect(dt, GPIO.FALLING, callback=dtClicked, bouncetime=100)
GPIO.add_event_detect(sw, GPIO.FALLING, callback=swClicked, bouncetime=500)

#############
# water scale
#############


def updateBeanWeight(val):
    global beanWeight

    if (val != -99999):
        oneDecimalVal = str(round(val, 1))
        if oneDecimalVal == '-0.0':
            beanWeight.updateWeight('0.0')
        else:
            beanWeight.updateWeight(oneDecimalVal)
    else:
        print('unknown bean value')
        beanWeight.updateWeight('0.0')


def updateWaterWeight(val):
    global waterWeight

    if (val != -99999):
        oneDecimalVal = str(round(val, 0))
        if oneDecimalVal == '-0.0':
            waterWeight.updateWeight('0.0')
        else:
            waterWeight.updateWeight(oneDecimalVal)
    else:
        print('unknown bean value')
        beanWeight.updateWeight('0.0')


def updateWeight(val):
    if (currentPage == "beanWeight"):
        updateBeanWeight(val)
    if (currentPage == "waterWeight"):
        updateWaterWeight(val)


def getWeight(callback):
    try:
        val = hx1.get_weight(5)
        callback(val)
        # print('hx1: ' + str(val) )
    except (KeyboardInterrupt, SystemExit):
        callback(-99999)


app.repeat(1000, getWeight, [updateWeight])

# def keyPressed(event_data):
# global currentPage;
# if(event_data.keycode == 822083616):
# if(currentPage == "beanContainer"):
#     beanContainer.visible = False
#     strength.visible = True
#     currentPage="strength"
# elif(currentPage == "strength"):
#     strength.visible = False
#     beanWeight.visible = True
#     currentPage="beanWeight"

# elif(currentPage == "beanWeight"):
#     beanWeight.visible = False
#     waterCan.visible = True
#     currentPage="waterCan"

# elif(currentPage == "waterCan"):
#     waterCan.visible = False
#     waterWeight.visible = True
#     currentPage="waterWeight"

# elif(currentPage == "waterWeight"):
#     waterWeight.visible = False
#     beanContainer.visible = True
#     currentPage="beanContainer"


# app.when_key_pressed = keyPressed

#############
# Finish
#############

app.display()

GPIO.cleanup()
