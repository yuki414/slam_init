"""
もとのC+の例外処理の仕方がわからん

"""

class SensorDataReader:
    def __init__(self, angleOffset):
        self.angleOffset = angleOffset
        # C++のデータファイル読み込み
        # std::ifstream inFile; // データファイル
    """
    このあたりに例外処理
    """

    def setAngleOffset(o):
        self.angleOffset = o

    def loadScan(self, cnt, scan):
        isScan = False
        while (!inFile.eof() and !isScan):
            isScan = loadLaserScan(cnt, scan)

        # isscanに対応して返り値true or false
        if (isScan):
            return False
        else:
            return True

    def loadLaserScan(self, cnt, Scan2D, scan):
