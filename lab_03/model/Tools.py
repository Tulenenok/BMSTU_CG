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
    M_CDA = 1  # ЦДА
    M_BREZENHAM_FLOAT = 2  # Брезенхем действительные числа
    M_BREZENHAM_INT = 3  # Брезенхем целые числа
    M_BREZENHAM_ELIMINATION = 4  # Брезенхем с устранением ступенчатости
    M_VY = 5  # ВУ
    M_USUAL = 6    # С помощью граф приметивов

    METHODS = (M_CDA, M_BREZENHAM_FLOAT, M_BREZENHAM_INT, M_BREZENHAM_ELIMINATION, M_VY, M_USUAL)

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
