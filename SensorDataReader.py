"""
C++のfstreamって普通のopenで置き換えていいのか？
inFile >> hogeを理解しないと，ファイル周りがなにもできない
読み飛ばしをどうすればよいのだろうか
"""
import os.path
import math # rad2deg:.degrees(), deg2rad:.radians()
from LPoint2D import LPoint2D
from Scan2D import Scan2D
from Pose2D import Pose2D
class SensorDataReader:
    def __init__(self):
        self.angleOffset = 180
        # ここにself.inFileとしてセットしたいがファイルの与えられ方を見てからかこう

        # C++のデータファイル読み込み
        # std::ifstream inFile; // データファイル
        # inFileはファイル読み込みが便利なインスタンスになった？

    def openScanFile(self, filepath):
        if os.path.exists(filepath):
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

    def loadScan(self, cnt, _scan):
        # 外側でloadScanを使うことが多いのでlineを毎回入れるのだるそう
        self.line = self.inFile.readline() # 一度目はループ前に読み込み
        isScan = False
        self.eof = False
        # print('line=',line)
        # line = self.inFile.readline()
        # print('line2=',line)
        # while (not(self.inFile.eof()) and not(isScan):
            # isScan = loadLaserScan(cnt, scan)
        #!!:pyでのeofをつかうかline=readlineによってnoneを得るかだと思うが．．．
        # データすべての読み込みでも2400まで行かないくらい
        # while (line and not(isScan)):
        i = 0
        # これはデータの行が終わるまで読み込み続ける
        while (not self.eof) and (not isScan):
            i = i + 1
            isScan = self.loadLaserScan(cnt, _scan)
            if i%10**3==0:
                print(i)
        if (isScan):
            return False
        else:
            return True

    def loadLaserScan(self, cnt, _scan):
        # inFile >> type この意味がわからん
        # type ~ self.line
        line = self.line.split() # データをわけてリスト型にする
        if (line[0] == 'LASERSCAN'):
            _scan.setSid(cnt)
            sid, sec, nsec = line[1], line[2], line[3]
            # vector<LPoint2D> lps;
            # lps = LPoint2D()
            # lpsは普通の配列としてやってみる
            lps = []
            pnum = int(line[4]) # スキャン点数
            # スキャン点は5からスタートしてpnum個+5まで進む
            for i in range(5,2*pnum+5,2):
                # inFile >> angle >> range ここでangleが定義されてるわけで．．．
                angle = float(line[i])
                scope = float(line[i+1])
                # シフト関数の処理は避けられなさそう
                angle = angle + self.angleOffset
                # Scan2DにMIN_SCAN_RANGE()が存在しないがどういうことか
                # レンジの範囲外だったときは~
                if ((scope <= Scan2D().MIN_SCAN_RANGE) or (scope >= Scan2D().MAX_SCAN_RANGE)):
                    continue # スキップ
                lp = LPoint2D()
                lp.setSid(cnt)
                lp.calXY(scope, angle)
                lps.append(lp)
            else:
                # これで最後のiを得ることができる
                end_i = i # i:最後のangle，i+1：最後のscope

            _scan.setLps(lps)

            # スキャンに対応するオドメトリ情報
            _pose = _scan.pose # Scan2D内にpose=Pose2Dと定義されたposeが存在する
            _pose.tx = float(line[end_i+2])
            _pose.ty = float(line[end_i+3])
            th = float(line[end_i+4])
            # ined+5,iend+6の数字の羅列は何を示しているか微妙
            _pose.setAngle(math.degrees(th)) # あとでrad to deg関数つくらなきゃ
            _pose.calRmat()

            self.line = self.inFile.readline()
            if (self.line==''):
                self.eof == True # lineがこれ以上読み込めなくなったときtureを返す
            return True # isScan=Falseで最後の列までよみこんだ，この行はようがなくをかえす
            # elseを作ってわざわざ面倒なことはしない方向で行こう
        # else:
        #     # 読み飛ばしを行いたい場合どうすればよいのだろう
        #     # next(inFile)
        #     self.inFile.readline()
        #
        #     return False
