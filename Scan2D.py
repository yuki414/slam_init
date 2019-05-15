'''
struct Scan2D
Scan2Dのクラス作成
C++ではstructを別個でつくらないといけない
ここではいくつかの構造体をpythonのclassによって定義する．

たぶん大量の間違いがあるので変えていこうと思う
struct hogeはclass hogeによって代用
'''
# In[]:
from Pose2D import Pose2D
from LPoint2D import LPoint2D
class Scan2D():
    def __init__(self):
        self.sid = 0
        self.pose = Pose2D()
        # std::vector<LPoint2D> lps;
        # 標準ライブラリのvectorを用いてLPoint2D型のlpsを定義するよ
        self.lps = LPoint2D() # pythonでは動的配列のはずなので，これでよい？
        self.MAX_SCAN_RANGE = 6
        self.MIN_SCAN_RANGE = 0.1

    def setSid(self, s):
        self.sid = s

    def setLps(self, _ps):
        self.lps = _ps

    def setPose(self, _p):
        self.pose = p
# In[]:
