from guizero import App, Text, Box, Picture


beanWeightBox = None
text = None
weight = None
next = None
weightGValue = ''


def updateLabel():
    weight.value = (weightGValue)
    weight.after(50, updateLabel)


def getBeanWeight(app, textSize):
    global beanWeightBox
    global text
    global weight
    global next
    beanWeightBox = Box(app, visible=False)
    text = Text(beanWeightBox, size=textSize,
                text='Grind the beans and place them with\nthe container on the scale')
    weight = Text(beanWeightBox, size=textSize*2, text="40g")
    updateLabel()
    next = Text(beanWeightBox, size=textSize,
                text="Click the rotation knob to continue")
    return beanWeightBox


def updateWeight(weightG):
    global weightGValue
    weightGValue = str(weightG)
    # global weight
    # if (weightG != weight.value):
    # print('update weight: ' + str(weightG))
    # weight.value = str(weightG)
