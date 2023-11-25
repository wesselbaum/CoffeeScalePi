from guizero import App, Text, Box, Picture


def getBeanWeight(app, textSize):
    beanWeightBox = Box(app, visible=False)
    text = Text(beanWeightBox, size=textSize, text='Grind the beans and place them with\nthe container on the scale')
    weight = Text(beanWeightBox, size=textSize*2, text="40g")
    next = Text(beanWeightBox, size=textSize, text="Click the rotation knob to continue")
    return beanWeightBox
