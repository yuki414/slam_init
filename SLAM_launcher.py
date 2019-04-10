'''
SLAMランチャー起動部分
ファイル開いたり，処理をどこでするかなどの振り分けを行ってる
各クラスファイルが何を実装してたかの対応が面倒
各引数をinit部分で与えるか，メソッドのところで与えるのか
initのところで与えられた場合，あるメソッドが他のメソッドに影響があるわけでその意図を求めてないくない？
と思ったがself.hogeを定義して，他のメソッドでも使えるようにすると良さそう
ただメイン関数とかランチャーの処理のメソッドのときに与えたりするので初期値はいらないかな
'''
# In[]:
class SlamLauncher():
    # startNはmainから与えられる
    # アンダーバーから始まる変数はprivate変数とする
    # private変数はクラス外からアクセスすることはできない，すなわちクラス内で用いる関数のみにしか利用できないと考えれば良い？
    def __init__(self):
        # selfインスタンスをインスタンスとしていいのかわからん
        # 適当なテストファイル作ってうまく行ったっぽいのでおｋ
        self.lidarOffset = Pose2D()
        self.sreader = SensorDataReader()  # ファイルからのセンサデータ読み込み
        self.pcmap = PointCloudMap()  # 点群地図，*pcmapはポインタ型の宣言，pyでは不要?
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
            skipData(self.startN)
            # C++では同じクラス内であればメソッドがどこにあるか明示しなくてもいいらしい
            # !!:pythonでもできるか確認

        totalTime, totalTimeDraw, totalTimeRead = 0, 0, 0  # double型
        scan = Scan2D() # scan2dはstrctなので注意
        eof = self.sreader.loadScan(cnt, scan)  # bool型
#         boost::timer tim; 何この書き方．．．

        while not(eof):
            if self.odometryOnly:
                if cnt == 0:
                    self.ipose = scan.pose() # iposeを入れたけど，ここでscan.poseを代入しちゃう？
                    self.ipose.calRmat()
                mapByOdometry(scan)  # これもランチャー内のメソッド
            else:
                self.sfront.process(scan)  # SLAMによる地図構築

            if (cnt & drawSkip == 0):
                # *pcmapなので本来ポインタ型の宣言，内部でそれ用に対応する必要がある
                mdrawer.drawMapGp(pcmap)

            cnt = cnt + 1  # ++cnt:wihle文中では前置と後置のインクリメント差は特にない
            eof = sreader.loadScan(cnt, scan)  # 次のスキャンを読み込む

        sreader.closeScanFile()
        # 終了時刻あとのテク，今は意味がわかっていないため放置
        # while(true):
        # sleep(1000)

        '''
        gitに上がっているものと教科書が違うため，違う部分をここに記載
        おそらくプログラムの進捗具合によって変化

        t1 = 100*tim.elapsed()

        if (cnt%drawSkip == 0):
            mdrawer.drawMapGp(pcmap)

        t2 = 1000*tim.elapsed()

        cnt = cnt + 1
        eof = sreader.loadScan(cnt, scan)

        t3 = 1000*tim.elapsed()
        totalTime = t3
        totalTimeDraw = totalTimeDraw + (t2 - t1)
        totalTimeRead = totalTimeRead + (t3 - t2)
ね
        print('---- SLAMlauncher: cnt = %f ends ----', cnt) # 原本では %1u
        '''

        sreader.closeScanFile()

        print("Elapsed time: mapping=%g, drawing=%g, reading=%g",
              (totalTime - totalTimeDraw - totalTimeRead), totalTimeDraw, totalTimeRead)
        print("SlamLauncher finished.")

    # 開始からnum個のスキャンまで読み飛ばす
    def skipData(self, num):
        scan = Scan2D() # この書き方だとクラスのような書き方がベストか？
        eof = sreader.loadScan(0, scan)
#         for (int i=0; !eof && i<num; i++) という文だが，pythonではbreakで抜けなければならない

        while (not eof and i < num):
            eof = sreader.loadScan(0, scan)

    # ここまでがSLAMluncherのメイン部分
    # ここからランチャーでつかったstructや関数の定義
    def mapByOdometry(self, scan):
        pose = Pose2D
        Pose2D.calRelativePose(scan.pose()) # スキャン取得時のオドメトリ位置
        lps = scan.lps()
        for j in range(lps.size()):
            lp = lps[j]
            pose.globalPoint(lp, glp)
            glps,emplace_back(glp)

        # // 点群地図pcmapにデータを格納
        # pcmap->addPose(pose);
        # pcmap->addPoints(glps);
        # pcmap->makeGlobalMap();

    def globalPoint(pi, po):
        po.x = Rmat[0][0]*pi.x + Rmat[0][1]*pi.y + tx
        po.y = Rmat[1][0]*pi.x + Rmat[1][1]*pi.y + ty


    def showsScans(self):
        mdrawer.initGnuplot()
        mdrawer.setRange(6)
        mdrawer.setAspectRatio(-0.9)

        cnt = 0
        if (startN > 0):
            skipData(startN)

        scan = Scan2D()
        eof = srader.loadScan(cnt, scan)
        while(not(eof)):
            # Sleep(100)

        mdrawer.drawScanGp(scan)

        eof = sreader.loadScan(cnt, scan)
        cnt = cnt + 1

    sreader.closeScanFile()
