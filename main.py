'''
main関数作成
C++のコードをpythonに落とし込んでいく
SLAM入門を参考

疑問：
・int mainをクラスにしてよかったのか
・return 1 の終わり方をexit()にした
・classで書いてしまったため，処理の大部分をメソッドで書いてしまった

'''
# In[]:
from enum import Enum
from SLAM_launcher import SLAM_launcher
# ここでエラーがでるが，pose2dなどを定義していないため
# In[]:
class main():
    def __init__(self, argc, argv):
        # オプションを渡して起動したいときにもちいる
        # argcはオプションの個数(int)，argvはオプションを格納する(char)
        self.argc = argc
        self.argv = argv

    # 準備
    scanCheck = False  # スキャン表示か
    odometryOnly = False  # オドメトリのみによる地図構築か
    startN = 0
    print('hello')
# In[]:
    # main関数のメインの部分
    def excute(self):
        if self.argc < 2:
            print('Error: too few arguments.')
            exit()  # !!注意: return 1に変わる関数がわからない

        # コマンド引数の処理??
        idx = 1
        if (self.argv[1, 0] == '-'):
            for i in range(30):
                # 原本では終了条件が指定されていない，breakで抜ける
                # 無限ループは少し怖いので適当にうちきり，あとで治す
                option = argv[1, i]
                if (option == None):
                    break
                elif (option == 's'):
                    scanCheck = True
                elif (option == 'o'):
                    odometryOnly = True
            if (argc == 2):
                print('Error: no file name.')
                exit()  # !!注意

            idx = idx + 1
        if (argc >= idx + 1):
            filename = argv[idx]
        if (argc == idx + 2):
            startN = atoi(argv[idx + 1])  # !!注意: atoi，急に出てきた
        elif (argc >= idx + 2):
            print('Error: invalid arguments.')
            exit()
# In[]:
    # ファイルを開く
    def open_file(self):
        # slamランチャーの起動，現時点では存在しないためコメントアウト
        # SLAM_launcher sl
        sl = SLAM_launcher(_startN, _odometryOnly) # __init__のための引数をいれろ
        flag = sl.setFilename(filename)  # 原本では bool flagなので，True or False
        if flag != True:  # !flag = not false = true で実行
            exit()

        sl.setStartN(startN)

        # 処理本体
        if scanCheck == True:
            sl.showScans()
        else:
            sl.setOdometryOnly(odometryOnly)
            sl.customizeFramework()
            sl.run()

        return 0  # 問題なくおわったときのCの処理だけど
        # pythonでreturnいれないで処理するとnoneが帰ってきて別に何もいらないときはどうすればよいのだろう
# In[]:
5+2
print('Test!')
