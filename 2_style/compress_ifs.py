def set_color(ctrlList=None, color=None):

    color_dictionary = {
                    1:4,
                    2:13,
                    3:25,
                    4:17,
                    5:17,
                    6:15,
                    7:6,
                    8:16,
                        }

    override_value = color_dictionary[color]


    for ctrlName in ctrlList:
        try:
            mc.setAttr(ctrlName + 'Shape.overrideEnabled', 1)
        except:
            pass

        try:
            mc.setAttr(ctrlName + 'Shape.overrideColor', override_value)

        except:
            pass


# EXAMPLE
# set_color(['circle','circle1'], 8)

