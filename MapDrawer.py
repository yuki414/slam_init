'''
マップ描画のところ

'''

class MapDrawer:
    def __init__(self, xmin, xmax, ymin, ymax, aspectR):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.aspectR = aspectR

    def setAspectRatio(self, a):
        self.aspectR = a
        print("set size ratio %f" % self.aspectR)

    def setRange(self, R):
        self.xmin, self.ymin = -R, -R
        self.xmax, self.ymax = R, R
        print("set xrange [%f:%f]" % (self.xmin, self.xmax))
        print("set yrange [%f:%f]" % (self.ymin, self.ymax))

    # pyではオーバーロードが不可能なので名前を変える
    def setRange_rect(self, xR, yR):
        self.xmin = -xR
        self.xmax = xR
        self.ymin = -yR
        self.ymax = yR
        print("set xrange [%f:%f]" % (self.xmin, self.xmax))
        print("set yrange [%f:%f]" % (self.ymin, self.ymax))

    def setRange_any(self, xm, xM, ym, yM):
        self.xmin = xm
        self.xmax = xM
        self.ymin = ym
        self.ymax = yM
        print("set xrange [%f:%f]" % (self.xmin, self.xmax))
        print("set yrange [%f:%f]" % (self.ymin, self.ymax))
