"""
C++のfstreamって普通のopenで置き換えていいのか？
"""

class SensorDataReader:
    def __init__(self, angleOffset):
        self.angleOffset = angleOffset
        # ここにself.inFileとしてセットしたいがファイルの与えられ方を見てからかこう

        # C++のデータファイル読み込み
        # std::ifstream inFile; // データファイル
        # inFileはファイル読み込みが便利なインスタンスになった？

    def openScanFile(filepath):
        if os.path.exsit(filepath):
            # fileが存在する場合
            inFile = open(filepath)
            return True
        else:
            print("Error: cannot open file")
            return False

    # この辺はメソッドではなく関数として扱う感じか？
    # そもそもselfを用いるかどうかがメソッドとの違いな気がするが
    def closeScanFile():
        inFile.close()

    def setAngleOffset(self, o):
        self.angleOffset = o

    def loadScan(self, cnt, scan):
        isScan = False
        while (not(inFile.eof()) and not(isScan):
            isScan = loadLaserScan(cnt, scan)

        # isscanに対応して返り値true or false
        if (isScan):
            return False
        else:
            return True

    def loadLaserScan(self, cnt, Scan2D, scan):
        # inFile >> type この意味がわからん
        if (type == "LASERSCAN"):
            scan.setSid(cnt)
            lps = LPoint2D()
            # inFile >> pnum
            lps.reserve(pnum)
            for i in range(pnum):
                # inFile >> angle >> range
                angle = angle + self.angleOffset
                if (range <= Scan2D.MIN_SCAN_RANGE()) or (range >= Scan2D.MAX_SCAN_RANGE()):
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
            pose.setAngle(rad2deg(th)) # あとでrad to deg関数つくらなきゃ
            pose.calRmat()

            return True
            
        else:
            getline(inFile, line)
            return False
