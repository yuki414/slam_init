'''
マップ描画のところ
C++のgpみたいなのをつかわないでかけないのか？
'''
# まだ変えてない
# このままだと初期値に大量の引数を入れることになるので変更
class MapDrawer:
    def __init__(self):
        self.gp = None # nullptr
        self.xmin = -10
        self.xmax = 10
        self.ymin = -10
        self.ymax = 10
        self.aspectR = -1.0

    # def initGunuplot():
        # gp = popen("gnuplot", "w");
        # 別画面で開くとかなんとか，C特有か？

    def setAspectRatio(self, a):
        self.aspectR = a
        print('set size ratio {}'.format(self.aspectR))

    def setRange(self, R):
        self.xmin, self.ymin = -R, -R
        self.xmax, self.ymax = R, R
        self.prin()

    # pyではオーバーロードが不可能なので名前を変える
    def setRange_double(self, xR, yR):
        self.xmin = -xR
        self.xmax = xR
        self.ymin = -yR
        self.ymax = yR
        self.prin()

    def setRange_quad(self, xm, xM, ym, yM):
        self.xmin = xm
        self.xmax = xM
        self.ymin = ym
        self.ymax = yM
        self.prin()

    def prin(self):
        print('set xrange [{}:{}]'.format(self.xmin, self.xmax))
        print('set yrange [{}:{}]'.format(self.ymin, self.ymax))

    # pcmap = PointCloudMap()
    def drawMapGp(self, _pcmap):
        self._lps = _pcmap.globalMap()
        self._poses = _pcmap.poses()
        self.drawGp(self._lps, self._poses)

    def drawScanGp(self, _scan):
        poses = Pose2D()
        pose = Pose2D()
        poses.emplace_back(pose)
        self.drawGp(scan.lps(), poses)

    def drawTrajectoryGp(_poses):
        lps = LPoint2D()
        drawGp(lps, _poses)

    def drawGp(self, _lps, _poses, flush):
        print('drawGp: size of lps = {}'.format(len(_lps)))
          # // gnuplot設定
          # fprintf(gp, "set multiplot\n");
          # //  fprintf(gp, "plot '-' w p pt 7 ps 0.1, '-' with vector\n");
          # fprintf(gp, "plot '-' w p pt 7 ps 0.1 lc rgb 0x0, '-' with vector\n");
        step1 = 1
        # 描画の書き方
        # range(start, stop, step)
        for i in range(0, len(_lps), step1):
            self._lp = _lps[i]
            print('{} {}'.format(lp.x, lp.y))

        step2 = 10
        for i in range(0, len(_poses), step2):
            cx = _pose.tx
            cy = _pose.ty
            cs = _pose.Rmat[0][0]
            sn = _pose.Rmat[1][0]

            dd = 0.4
            x1 = cs*dd
            y1 = sn*dd
            x2 = -sn*dd
            y2 = cs*dd

            print('{} {} {} {}'.format(cx, cy, x1, y1))
            print('{} {} {} {}'.format(cx, cy, x2, y2))

        # if (flush):
            #
