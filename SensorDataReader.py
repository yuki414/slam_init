"""
C++のfstreamって普通のopenで置き換えていいのか？
inFile >> hogeを理解しないと，ファイル周りがなにもできない
読み飛ばしをどうすればよいのだろうか
"""

class SensorDataReader:
    def __init__(self):
        self.angleOffset = 180
        # ここにself.inFileとしてセットしたいがファイルの与えられ方を見てからかこう

        # C++のデータファイル読み込み
        # std::ifstream inFile; // データファイル
        # inFileはファイル読み込みが便利なインスタンスになった？

    def openScanFile(self, filepath):
        if os.path.exsit(filepath):
            # fileが存在する場合
            self.inFile = open(filepath)
            return True
        else:
            print("Error: cannot open file")
            return False

    # この辺はメソッドではなく関数として扱う感じか？
    # そもそもselfを用いるかどうかがメソッドとの違いな気がするが
    def closeScanFile(self):
        self.inFile.close()

    def setAngleOffset(self, o):
        self.angleOffset = o

    def loadScan(self, cnt, &scan,line):
        isScan = False
        # while (not(self.inFile.eof()) and not(isScan):
            # isScan = loadLaserScan(cnt, scan)
        #!!:pyでのeofをつかうかline=readlineによってnoneを得るかだと思うが．．．
        while (line and not(isScan)):
            isScan = SensorDataReader.loadLaserScan(cnt, scan)

        if (isScan):
            return False
        else:
            return True

    def loadLaserScan(self, cnt, Scan2D, scan):
        # inFile >> type この意味がわからん
        if (type == 'LASERSCAN'):
            scan.setSid(cnt)
            lps = LPoint2D()
            # inFile >> pnum
            lps.reserve(pnum)
            for i in range(pnum):
                # inFile >> angle >> range ここでangleが定義されてるわけで．．．
                # シフト関数の処理は避けられなさそう
                angle = angle + self.angleOffset
                # Scan2DにMIN_SCAN_RANGE()が存在しないがどういうことか
                if ((range <= Scan2D.MIN_SCAN_RANGE()) or (range >= Scan2D.MAX_SCAN_RANGE())):
                    continue # スキップ
                lp = LPoint2D
                lp.setSid(cnt)
                lp.calXY(range, angle)
                lps.emplace_back(lp)

            scan.setLpst(lps)

            # スキャンに対応するオドメトリ情報
            # Pose2D &pose = scan.pose; ???
            # inFile >> pose.tx >> pose.ty
            # inFile >> th
            pose.setAngle(degrees(th)) # あとでrad to deg関数つくらなきゃ
            pose.calRmat()

            return True

        else:
            # 読み飛ばしを行いたい場合どうすればよいのだろう
            # next(inFile)
            self.inFile.readline()

            return False
