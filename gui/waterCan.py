from guizero import App, Text, Box, Picture


def getWaterCan(app, textSize):
    waterCanBox = Box(app, visible=False)
    text = Text(waterCanBox, size=textSize, text='Place the water can on scale and click\n Rotation Knob to continue')
    return waterCanBox
