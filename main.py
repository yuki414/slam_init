'''
main関数作成

・終了部分をsys.exit(1)に変更
・SlamLauncherのimportあたりが手付かず
'''
# In[]:
# モジュールインポート
import sys
import numpy as np
import os.path
import math # rad2deg:.degrees(), deg2rad:.radians()
from enum import Enum
import time
# クラスをもってくる
import SLAM_launcher # SLAM_launcher.pyからクラスをimport
# ここでエラーがでるが，pose2dなどを定義していないため

# In[]:
def main():
    # オプションを渡して起動したいときにもちいる
    # argcはオプションの個数(int)，argvはオプションを格納する(char)
    argv = sys.argv
    argc = len(argv)
    # 準備
    scanCheck = False  # スキャン表示か
    odometryOnly = False  # オドメトリのみによる地図構築か
    startN = 0
    # filenameはstr型
    if (argc < 2):
        print('Error: too few arguments.')
        sys.exit(1) # 実行画面にエラー1とでるはず

    # コマンド引数の処理
    idx = 1
    if (argv[1][0] == '-'):
        lim_of_argv = len(argv[1])
        for i in range(1,lim_of_argv):
            # 原本では終了条件が指定されていない，breakで抜ける
            # 無限ループは少し怖いので適当にうちきり，あとで治す
            option = argv[1][i]
            # argv[1]の最後まで行ったらbreak，けどそもそも長さがわかればいらない
            # if (option == None):
            #     break
            if (option == 's'):
                scanCheck = True
            elif (option == 'o'):
                odometryOnly = True

        if (argc == 2):
            print('Error: no file name.')
            sys.exit(1)

        idx = idx + 1
    if (argc >= idx + 1):
        filename = argv[idx]
    if (argc == idx + 2):
        startN = int(argv[idx + 1])  # str to int
    elif (argc >= idx + 2):
        print('Error: invalid arguments.')
        sys.exit(1)
    print('SlamLauncher: startN={0}, scanCheck={1}, odometryOnly={2}'.format(startN, scanCheck, odometryOnly))
    print('filename={}'.format(filename))
# In[]:
    # SLAM_launcherからSlamLauncherクラス
    sl = SlamLauncher()
    # 初期引数は自身だけであるため引数なしでおｋ

    # filenameを渡し，中でfilepathがあるか確認する
    # 存在する場合trueを返し，しない場合エラー表示とfalseを返す
    flag = sl.setFilename(filename)
    # flag=False:でファイルパスなし
    if not(flag):
        sys.exit(1)
    # 引数startNをslクラスに与えているだけ
    sl.setStartN(startN)

    # 処理本体
    if (scanCheck):
        sl.showScans()
    else:
        sl.setOdometryOnly(odometryOnly)
        # sl.customizeFramework() # まだない
        sl.run()

    return 0  # 問題なくおわったときのCの処理だけど
    # pythonでreturnいれないで処理するとnoneが帰ってきて別に何もいらないときはどうすればよいのだろう
# In[]:
if __name__ == '__main__':
    main()
