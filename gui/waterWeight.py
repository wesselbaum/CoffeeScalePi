from guizero import App, Text, Box, Picture


def getWaterWeight(app, textSize):
    waterWeightBox = Box(app, visible=False)
    text = Text(waterWeightBox, size=textSize, text='Fill the water')
    weight = Text(waterWeightBox, size=textSize*2, text="180ml /800ml")
    next = Text(waterWeightBox, size=textSize, text="Click the rotation knob to finish")
    return waterWeightBox
