'''
main関数作成

・終了部分をsys.exit(1)に変更
・SlamLauncherのimportあたりが手付かず
'''
# In[]:
import sys
import os.path
from enum import Enum
from SLAM_launcher import SLAM_launcher
# ここでエラーがでるが，pose2dなどを定義していないため

# In[]:
# あとで入力引数として書き換えた
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
    print('hello')
    if (argc < 2):
        print('Error: too few arguments.')
        sys.exit(1)

    # コマンド引数の処理??
    idx = 1
    if (argv[1][0] == '-'):
        for i in range(30):
            # 原本では終了条件が指定されていない，breakで抜ける
            # 無限ループは少し怖いので適当にうちきり，あとで治す
            option = argv[1][i]
            # 存在しない要素を参照しようとするとエラーがでるのでは？
            if (option == None):
                break
            elif (option == 's'):
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
    print('SlamLauncher: startN=%d, scanCheck=%d, odometryOnly=%d' % (startN, scanCheck, odometryOnly))
    print('filename={}'.format(filename))
# In[]:
    sl = SlamLauncher()
    # sl = SLAMLauncher(_startN, _odometryOnly) # __init__のための引数を入れる場合こっち

    # filenameを渡し，中でfilepathがあるか確認する
    # 存在する場合trueを返し，しない場合エラー表示とfalseを返す
    flag = sl.setFilename(filename)
    if not(flag):
        sys.exit()

    sl.setStartN(startN)

    # 処理本体
    if (scanCheck):
        sl.showScans()
    else:
        sl.setOdometryOnly(odometryOnly)
        sl.customizeFramework()
        sl.run()

    return 0  # 問題なくおわったときのCの処理だけど
    # pythonでreturnいれないで処理するとnoneが帰ってきて別に何もいらないときはどうすればよいのだろう
# In[]:
if __name__ == '__main__':
    main()
