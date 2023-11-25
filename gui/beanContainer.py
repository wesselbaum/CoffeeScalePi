from guizero import App, Text, Box, Picture


def getBeanContainer(app, textSize):
    beanContainerBox = Box(app, visible=False)
    text = Text(beanContainerBox, size=textSize, text='Place the bean container on scale and click\n Rotation Knob to start')
    return beanContainerBox
