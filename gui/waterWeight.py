from guizero import App, Text, Box, Picture

weight = None
grounds = 0
relationshipWater = 0
sliderContent = None
overflow = None
targetWeight = 0


def getWaterWeight(app, textSize, groundsParam, waterRatio):
    global weight
    global grounds
    global relationshipWater
    global sliderContent
    global overflow
    relationshipWater = waterRatio
    grounds = groundsParam
    waterWeightBox = Box(app, visible=False)
    text = Text(waterWeightBox, size=textSize, text='Fill the water')
    weight = Text(waterWeightBox, size=textSize*2, text="180ml /800ml")
    sliderWrapper = Box(waterWeightBox,
                        width=50, border=True, height=200, align='bottom')
    sliderContent = Box(sliderWrapper, height=100,
                        width=50, border=False, align='bottom')
    overflow = Box(sliderWrapper, height=50,
                   width=50, border=False, align='top')
    target = Box(sliderWrapper, height=2, width=50, align='top')
    target.bg = 'black'
    sliderContent.bg = 'green'
    overflow.bg = '#eeeeee'
    next = Text(waterWeightBox, size=textSize,
                text="Click the rotation knob to finish")
    return waterWeightBox


def prepareState(groundsParam, waterRatio):
    global grounds
    global relationshipWater
    global targetWeight
    grounds = groundsParam
    relationshipWater = waterRatio
    targetWeight = groundsParam * waterRatio


def updateWeight(weightG):
    global weight
    if (weightG != weight.value):
        weight.value = str(weightG) + "ml  / " + \
            str(targetWeight) + "ml"
        print('update weight: ' + str(weightG))
        percentage = weightG / targetWeight * 100

        if (percentage < 100):
            sliderContent.height = percentage
        else:
            overflowPercentage = percentage - 100
            sliderContent.height = 100
            overflow.height = overflowPercentage
            overflow.align = 'bottom'


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

    # if waterTarget > 1250:
    # warning.value = 'Warning: Too much water for the Moccamaster'
    # warning.visible = True
    # if grounds > 70:
    # warning.value = 'Warning: Too much grounds for the Moccamaster'
    # warning.visible = True
    # if grounds < 71 and waterTarget < 1251:
    # warning.visible = False
