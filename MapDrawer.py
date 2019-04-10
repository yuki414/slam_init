'''
マップ描画のところ
C++のgpみたいなのをつかわないでかけないのか？
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

    def drawMapGp(pcmap):
        lps = pcmap.globalMap()
        poses = pcmap.poses()
        drawGp(lps, poses)

    def drawScanGp(scan):
        poses = Pose2D()
        pose = Pose2D()
        poses.emplace_back(pose)
        drawGp(scan.lps, poses)

    def drawTrajectoryGp(poses):
        lps = LPoint2D()
        drawGp(lps, poses)

    def drawGp(lps, poses, flus):
        print("drawGp: lps.size={}".format(len(lps))

          # // gnuplot設定
          # fprintf(gp, "set multiplot\n");
          # //  fprintf(gp, "plot '-' w p pt 7 ps 0.1, '-' with vector\n");
          # fprintf(gp, "plot '-' w p pt 7 ps 0.1 lc rgb 0x0, '-' with vector\n");
        step1 = 1
        # 描画の書き方
        # range(start, stop, step)
        # for i in range(0, len(lps), step1):

        step2 = 10
        for i in range(0, len(lps), step2):
            cx = pose.tx
            cy = pose.ty
            cs = pose.Rmat[0][0]
            sn = pose.Rmat[1][0]

            dd = 0.4
            x1 = cs*dd
            y1 = sn*dd
            x2 = -sn*dd
            y2 = cs*dd

            print("{} {} {} {}" .format(cx, cy, x1, y1))
            print("{} {} {} {}" .format(cx, cy, x2, y2))

        # if (flush):
            #
