from guizero import App, Text, Box, Picture

weight = None


def getWaterWeight(app, textSize):
    global weight
    waterWeightBox = Box(app, visible=False)
    text = Text(waterWeightBox, size=textSize, text='Fill the water')
    weight = Text(waterWeightBox, size=textSize*2, text="180ml /800ml")
    next = Text(waterWeightBox, size=textSize,
                text="Click the rotation knob to finish")
    return waterWeightBox


def updateWeight(weightG):
    global weight
    if (weightG != weight.value):
        weight.value = str(weightG) + "ml  / 800ml"
        print('update weight: ' + str(weightG))
