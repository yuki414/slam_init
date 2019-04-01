'''
SLAM launcherファイル
C++で書かれていることの意味わからないレベルが結構高め
ただしここがわかればmain→slamランチャという流れができて各モジュール作成に専念することが可能
'''

# In[]:
class SLAM_launcher():
    # startNはmainから与えられる
    # アンダーバーから始まる変数はprivate変数とする
    # private変数はクラス外からアクセスすることはできない，すなわちクラス内で用いる関数のみにしか利用できないと考えれば良い？
    def __init__(self, _startN, _odometryOnly):
        self.startN = _startN  # int startN: 開始スキャン番号
        self.odometryOnly = _odometryOnly  # bool odometryOnly
        # int drawSkip: 描画間隔，main関数で渡されていないが，どこからもらうのか

#   Pose2D lidarOffset # レーザスキャナとロボットの相対位置，別ファイルか？
    lidarOffset = Pose2D()
    sreader = SensorDataReader()  # ファイルからのセンサデータ読み込み
    pcmap = PointCloudMap()  # 点群地図，*pcmapはポインタ型の宣言，pyでは不要?
    sfront = SlamFrontEnd() # SLAMフロントエンド
    mdrawer = MapDrawer()  # gnuplotによる描画のクラス
    fcustom = FrameworkCustomizer()  # フレームワークの改造
# In[]:
    '''
        public:
      SlamLauncher() : startN(0), drawSkip(10), odometryOnly(false), pcmap(nullptr) {
      }
      ~SlamLauncher() {
      }
    ///////////
      void setStartN(int n) {
        startN = n;
      }
      void setOdometryOnly(bool p) {
        odometryOnly = p;
      }
    ///////////
        ここでpublicなメンバ関数の宣言
        void run();
        void showScans();
        void mapByOdometry(Scan2D *scan);
        bool setFilename(char *filename);
        void skipData(int num);
        void customizeFramework();
    };
    '''
# print('test!')
# #endif
    # 上ではprivateとpublicな変数と関数を宣言しただけであって，定義はしていない
    # C++では宣言した関数を
    # void SLAMlauncher::run()を例に(戻り型) (クラス名)::(関数名)のように定義する
    # pyでいうところの，def (関数名): か？
    # P66の34行目と同じような書き方
# In[]:
    def run(self):
        mdrawer.initGunuplot()
        mdrawer.setAspectRatio(-0.9)
        # using namespace std;     // C++標準ライブラリの名前空間を使う
        # 上でこれがつかわれてる

        # size_t cnt = 0;
        # size_tは、オブジェクトのバイト数を表現できる程度に十分に大きい符号なし整数型
        cnt = 0  # 処理の論理時刻
        if self.startN > 0:
            skipData(self.startN)

        totalTime, totalTimeDraw, totalTimeRead = 0, 0, 0  # double型
        scan = Scan2D() # scan2dはstrctなので注意
        eof = sreader.loadScan(cnt, scan)  # bool型
#         boost::timer tim; 何この書き方．．．

        while (not eof):
            if self.odometryOnly:
                if cnt == 0:
                    ipose = scan.pose
                    ipose.calRmat()
                mapByOdometry(scan)  # ポインタのやつ
            else:
                sfront.process(scan)  # SLAMによる地図構築

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
