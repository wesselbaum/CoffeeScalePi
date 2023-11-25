from guizero import App, Text, Box, Picture


def getStrength(app, textSize):
    strength = Box(app, visible=False)
    text = Text(strength, size=textSize, text='Choose the strength by rotating\nthe knob and click to continue')

    boldBeanImage = './bean.png'
    lightBean = './bean_light.png'
    beanBox = Box(strength, border=0, layout='grid', align='right')
    beanPicture1 = Picture(beanBox, image=boldBeanImage, grid=[0, 1])
    beanPicture2 = Picture(beanBox, image=boldBeanImage, grid=[1, 1])
    beanPicture3 = Picture(beanBox, image=boldBeanImage, grid=[2, 1])
    beanPicture4 = Picture(beanBox, image=boldBeanImage, grid=[3, 1])
    beanPicture5 = Picture(beanBox, image=lightBean, grid=[4, 1])
    beanPicture5.bg = 'white'

    return strength
