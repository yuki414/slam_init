'''
SLAMランチャー起動部分
ファイル開いたり，処理をどこでするかなどの振り分けを行ってる
各クラスファイルが何を実装してたかの対応が面倒
各引数をinit部分で与えるか，メソッドのところで与えるのか
initのところで与えられた場合，あるメソッドが他のメソッドに影響があるわけでその意図を求めてないくない？
と思ったがself.hogeを定義して，他のメソッドでも使えるようにすると良さそう
ただメイン関数とかランチャーの処理のメソッドのときに与えたりするので初期値はいらないかな
ポインタの扱いの話題は避けられなさそう
ひとまずポインタに該当する箇所はアンダーバーを入れて対応
参考書の進捗ページでは処理時間のコードが内があってもなくてもどっちでもいいと思うのでつけておく
'''
# In[]:
# クラスimport
import SensorDataReader
import Pose2D
import Scan2D
import MapDrawer
# In[]:
class SlamLauncher():
    # アンダーバーから始まる変数はprivate変数とする
    # pythonにおけるprivate変数の扱いが少し特殊かもペンディング
    # private変数はクラス外からアクセスすることはできない，すなわちクラス内で用いる関数のみにしか利用できないと考えれば良い？
    def __init__(self):
        self.startN = 0
        self.drawSkip = 10
        self.odometryOnly = False
        self.pcmap = None
        # selfインスタンスをインスタンスとして定義していいのかわからん
        # 適当なテストファイル作ってうまく行ったっぽいのでおｋ
        self.ipose = Pose2D()
        self.lidarOffset = Pose2D()
        self.sreader = SensorDataReader()  # ファイルからのセンサデータ読み込み
        self._pcmap = PointCloudMap()  # 点群地図，*pcmapはポインタ型の宣言，pyでは不要?
        self.sfront = SlamFrontEnd() # SLAMフロントエンド
        self.mdrawer = MapDrawer()  # gnuplotによる描画のクラス
        self.fcustom = FrameworkCustomizer()  # フレームワークの改造

        '''
        こいつらをインスタンスとして扱えばいいのかどうか・・・
        Pose2D ipose;                    // オドメトリ地図構築の補助データ。初期位置の角度を0にする
        Pose2D lidarOffset;              // レーザスキャナとロボットの相対位置

        SensorDataReader sreader;        // ファイルからのセンサデータ読み込み
        PointCloudMap *pcmap;            // 点群地図
        SlamFrontEnd sfront;             // SLAMフロントエンド
        MapDrawer mdrawer;               // gnuplotによる描画
        FrameworkCustomizer fcustom;     // フレームワークの改造
        '''
# In[]:
    def setStartN(self, n):
        self.startN = n
        # startNはprivate変数でクラス内で使いたいのでself.startNとした

    def setOdometryOnly(self, p):
        self.odometryOnly = p # bool

    # 上ではprivateとpublicな変数と関数を宣言しただけであって，定義はしていない
    # C++では宣言した関数を
    # void SLAMlauncher::run()を例に(戻り型) (クラス名)::(関数名)のように定義する
    # pyでいうところの，def (関数名): か？
    # P66の34行目と同じような書き方
# In[]:
    def run(self):
        self.mdrawer.initGunuplot()
        self.mdrawer.setAspectRatio(-0.9)

        cnt = 0  # 処理の論理時刻
        # startNはmainにてsetStartN(n)として与えられる
        if self.startN > 0:
            self.skipData(self.startN)
            # C++では同じクラス内であればメソッドがどこにあるか明示しなくてもいいらしい
            # 確認：self.hogemehodとすればいいらしい

        totalTime, totalTimeDraw, totalTimeRead = 0, 0, 0  # 処理時間みるため，初期化
        scan = Scan2D() # !!:scan2dはstrctなので注意
        eof = self.sreader.loadScan(cnt, scan)  # bool型
        # 処理時間の計測
        time_origin = time.time() # 開始処理時刻(年月日~という感じで得る)
        while not(eof):
            if (self.odometryOnly):
                # オドメトリによる地図構築
                if (cnt == 0):
                    self.ipose = scan.pose() # iposeを入れたけど，ここでscan.poseを代入しちゃう？
                    self.ipose.calRmat()
                mapByOdometry(scan)  # これもランチャー内のメソッド
            else:
                # SLAMによる地図構築
                self.sfront.process(scan)

            t1 = time.time() - time_origin

            if (cnt % drawSkip == 0):
                # *pcmapなので本来ポインタ型の宣言，内部でそれ用に対応する必要がある
                self.mdrawer.drawMapGp(self._pcmap)
                t2 = time.time() - time_origin

            cnt = cnt + 1  # ++cnt:wihle文中では前置と後置のインクリメント差は特にない
            eof = sef.sreader.loadScan(cnt, scan)  # 次のスキャンを読み込む

            t3 = time.time() - time_origin
            totalTime = t3 # 全体の処理時間 これだと毎回t3消えない？
            totalTimeDraw = totalTimeDraw + (t2 - t1) # 描画時間の合計
            totalTimeRead = totalTimeRead + (t3 - t2) # ロード時間の合計

            print('---- SlamLauncher: cnt={} ends'.format(cnt))
        self.sreader.closeScanFile()

        print('Elapsed time: mapping={0}, drawing={1}, reading={2}'.format(\
        (totalTime-totalTimeDraw-totalTimeRead), totalTimeDraw, totalTimeRead))
        print('SlamLauncher finished.')

        '''
        描画画面を残しておくための処理
        C++特有のものじゃない？とりあえずいらない        '''

        '''

        while(true) {
        #ifdef _WIN32
            Sleep(1000);                            // WindowsではSleep
        #elif __linux__
            usleep(1000000);                        // Linuxではusleep
        #endif
          }
        '''

        sreader.closeScanFile()

        print("Elapsed time: mapping=%g, drawing=%g, reading=%g",
              (totalTime - totalTimeDraw - totalTimeRead), totalTimeDraw, totalTimeRead)
        print("SlamLauncher finished.")

    # 開始からnum個のスキャンまで読み飛ばす
    def skipData(self, num):
        scan = Scan2D()
        eof = self.sreader.loadScan(0, scan)
#         for (int i=0; !eof && i<num; i++) という文だが，pythonではbreakで抜けなければならない
        for i in range(num):
            if not(eof):
                break
            eof = self.sreader.loadScan(0, scan)
        # こっちのほうがスマート
        # while (not(eof) and (i < num)):
        #     eof = sreader.loadScan(0, scan)

    '''
    # 進捗的にはここがまだない
    def mapByOdometry(self, _scan):
        pose = Pose2D()
        # Pose2D::calRelativePose(scan->pose, ipose, pose);
        # C++では->（アロー演算子）によってポインタ変数のメンバ関数が呼び出される
        Pose2D.calRelativePose(scan.pose, self.ipose, pose) #!!:ここかなり怪しい
        &lps = scan.lps()
        for j in range(len(lps)):
            # LPoint2D &lp = lps[j];
            # LPoint2D glp;
            &lp = lps[j]
            glp = LPoint2D()
            pose.globalPoint(lp, glp)
            glps.emplace_back(glp)

        # // 点群地図pcmapにデータを格納
        # pcmap->addPose(pose);
        # pcmap->addPoints(glps);
        # pcmap->makeGlobalMap();
        pcmap.addPose(pose)
        pcmap.addPoints(glps)
        pcmap.makeGlobalMap()

        print('Odom pose: tx={0}, ty={1}, th={2}'.format(pose.tx, pose.ty, pose.th))
    '''
    def globalPoint(pi, po):
        po.x = Rmat[0][0]*pi.x + Rmat[0][1]*pi.y + tx
        po.y = Rmat[1][0]*pi.x + Rmat[1][1]*pi.y + ty


    def showsScans(self):
        mdrawer.initGnuplot()
        mdrawer.setRange(6)
        mdrawer.setAspectRatio(-0.9)

        cnt = 0
        if (self.startN > 0):
            self.skipData(self.startN)

        scan = Scan2D()
        eof = self.srader.loadScan(cnt, scan)
        # while(not(eof)):
            # Sleep(100)

        self.mdrawer.drawScanGp(scan)

        print('---- scan num={} ----'.format(cnt))
        eof = sreader.loadScan(cnt, scan)
        cnt = cnt + 1

    sreader.closeScanFile()
    print('SlamLauncher finished.')

    def setFilename(self, _filename):
        flag = self.sreader.openScanFile(filename)

        return flag
