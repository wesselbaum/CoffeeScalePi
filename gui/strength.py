from guizero import App, Text, Box, Picture


waterRatio = 16
lastwaterRatio = waterRatio

boldBeanImage = './bean.png'
lightBean = './bean_light.png'
strength = None
beanBox = None
beanPicture1 = None
beanPicture2 = None
beanPicture3 = None
beanPicture4 = None
beanPicture5 = None
amountText = None
strengths = []


def getStrength(app, textSize, strengthsParam):
    global strengths
    global beanPicture1
    global beanPicture2
    global beanPicture3
    global beanPicture4
    global beanPicture5
    global amountText
    global beanBox
    strength = Box(app, visible=False)
    beanBox = Box(strength, border=0, layout='grid', align='right')
    beanPicture1 = Picture(beanBox, image=boldBeanImage, grid=[0, 1])
    beanPicture2 = Picture(beanBox, image=boldBeanImage, grid=[1, 1])
    beanPicture3 = Picture(beanBox, image=boldBeanImage, grid=[2, 1])
    beanPicture4 = Picture(beanBox, image=boldBeanImage, grid=[3, 1])
    beanPicture5 = Picture(beanBox, image=lightBean, grid=[4, 1])

    text = Text(strength, size=textSize,
                text='Choose the strength by rotating\nthe knob and click to continue')
    amountText = Text(strength, size=textSize, text="")
    strengths = strengthsParam
    return strength


def adjustRatio(newValue):
    global waterRatio
    waterRatio = newValue
    processRelationship()


def processRelationship():
    global lastwaterRatio
    amountText.value = ('1/' + str(waterRatio))
    if (lastwaterRatio != waterRatio):
        lastwaterRatio = waterRatio
        if waterRatio < strengths[0]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = boldBeanImage
            beanPicture4.image = boldBeanImage
            beanPicture5.image = boldBeanImage
        if waterRatio >= strengths[0]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = boldBeanImage
            beanPicture4.image = boldBeanImage
            beanPicture5.image = lightBean
        if waterRatio >= strengths[1]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = boldBeanImage
            beanPicture4.image = lightBean
            beanPicture5.image = lightBean
        if waterRatio >= strengths[2]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = boldBeanImage
            beanPicture3.image = lightBean
            beanPicture4.image = lightBean
            beanPicture5.image = lightBean
        if waterRatio >= strengths[3]:
            beanPicture1.image = boldBeanImage
            beanPicture2.image = lightBean
            beanPicture3.image = lightBean
            beanPicture4.image = lightBean
            beanPicture5.image = lightBean
