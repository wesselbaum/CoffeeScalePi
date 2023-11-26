from RPi import GPIO
import sys
from guizero import App, Text, Box, Picture
from PIL import Image
from gui import beanContainer, strength, beanWeight, waterCan, waterWeight
from lib.hx711 import HX711
import time
import asyncio

# colors
color = '#262626'
bg = '#F4F4ee'
alert = '#ff7f11'
primary = '#4c956c'
secondary = '#1e91d6'
textSize = 40

# recipe
water = 300
grounds = 20
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
app = App(title="Coffee Scale Pi", layout="auto",
          bg=bg, width=1024, height=600)
app.full_screen = True
currentPage = 'beanContainer'

beanContainerBox = beanContainer.getBeanContainer(app, textSize)
strengthBox = strength.getStrength(app, textSize, strengths)
beanWeightBox = beanWeight.getBeanWeight(app, textSize)
waterCanBox = waterCan.getWaterCan(app, textSize)
waterWeightBox = waterWeight.getWaterWeight(
    app, textSize, grounds, relationshipWater)


beanContainerBox.visible = True


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


def clkClicked(chanel):
    global relationshipWater
    global clkLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)

    if clkState == 0 and dtState == 1:
        relationshipWater += 1
        print(relationshipWater)
        strength.adjustRatio(relationshipWater)
    clkLastState = clkState


def dtClicked(chanel):
    global relationshipWater
    global dtLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)

    if clkState == 1 and dtState == 0:
        relationshipWater -= 1
        print(relationshipWater)
        strength.adjustRatio(relationshipWater)
    dtLastState = dtState


tareTime = time.time()


def tare():
    global tareTime
    hx1.tare()
    tareTime = time.time()


def swClicked(chanel):
    clickedTime = time.time()

    if (clickedTime - tareTime < 1):
        print('skip')
        return

    global currentPage
    if (currentPage == "beanContainer"):
        beanContainerBox.visible = False
        strengthBox.visible = True
        currentPage = "strength"
    elif (currentPage == "strength"):
        tare()
        strengthBox.visible = False
        beanWeightBox.visible = True
        currentPage = "beanWeight"
    elif (currentPage == "beanWeight"):
        beanWeightBox.visible = False
        waterCanBox.visible = True
        currentPage = "waterCan"

    elif (currentPage == "waterCan"):
        tare()
        waterWeight.prepareState(grounds, relationshipWater)
        waterCanBox.visible = False
        waterWeightBox.visible = True
        currentPage = "waterWeight"
    elif (currentPage == "waterWeight"):
        waterWeightBox.visible = False
        beanContainerBox.visible = True
        currentPage = "beanContainer"
    print(currentPage)


GPIO.add_event_detect(clk, GPIO.FALLING, callback=clkClicked, bouncetime=100)
GPIO.add_event_detect(dt, GPIO.FALLING, callback=dtClicked, bouncetime=100)
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
    global waterWeightBox

    if (val != -99999):
        oneDecimalVal = str(int(val))
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
        val = hx1.get_weight(3)
        callback(val)
        # print('hx1: ' + str(val) )
    except (KeyboardInterrupt, SystemExit):
        callback(-99999)


app.repeat(400, getWeight, [updateWeight])

#############
# Finish
#############

app.display()

GPIO.cleanup()
