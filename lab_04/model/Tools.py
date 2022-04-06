import colorsys


class Tools:
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1
    SEPARATOR_COORDS = ' ; '
    SEPARATOR_POL = '---'
    INVALID_FILENAME = -1
    INVALID_LISTNAME = -2
    INVALID_HEAD = -3
    INVALID_DATA = -4
    INVALID_FORMAT_DATA = -5
    OBSCURE_ERROR = -6

    """ Методы отрисовки отрезка """
    M_CANONICAL = 0
    M_PARAMETRIC = 1
    M_BREZENHAM = 2
    M_MIDDLE_POINT = 3
    M_USUAL = 4

    METHODS = (M_CANONICAL, M_PARAMETRIC, M_BREZENHAM, M_MIDDLE_POINT, M_USUAL)

    EPS = 0.1

    @staticmethod
    def isInt(x):
        try:
            x = int(x)
            return True
        except:
            return False

    @staticmethod
    def isFloat(x):
        try:
            x = float(x)
            return True
        except:
            return False

    @staticmethod
    def isRightFilename(filename):
        try:
            f = open(filename, 'r')
            f.close()
            return True
        except:
            return False

    @staticmethod
    def changeIntens(color_rgb, i):
        if len(color_rgb) != 3:
            r, g, b = int(color_rgb[1:3], 16), int(color_rgb[3:5], 16), int(color_rgb[5:7], 16)
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        else:
            h, s, v = colorsys.rgb_to_hsv(color_rgb[0] / 255, color_rgb[1] / 255, color_rgb[2] / 255)
        s *= i
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        rh = '0' + str(hex(int(r * 255))[2:].upper())
        gh = '0' + str(hex(int(g * 255))[2:].upper())
        bh = '0' + str(hex(int(b * 255))[2:].upper())
        return f'#{rh[-2:]}{gh[-2:]}{bh[-2:]}'
