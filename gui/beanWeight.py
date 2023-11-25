from guizero import App, Text, Box, Picture


weight = None
lastWeight = "0"


def getBeanWeight(app, textSize):

    global weight
    beanWeightBox = Box(app, visible=False)
    text = Text(beanWeightBox, size=textSize,
                text='Grind the beans and place them with\nthe container on the scale')
    weight = Text(beanWeightBox, size=textSize*2, text="40g")
    next = Text(beanWeightBox, size=textSize,
                text="Click the rotation knob to continue")
    return beanWeightBox


def updateWeight(weightG):
    global weight
    global lastWeight
    if (weightG != lastWeight):
        lastWeight = weightG
        weight.value = str(weightG)
        print('update weight: ' + str(weightG))
