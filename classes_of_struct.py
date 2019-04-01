'''
Scan2Dのクラス作成
C++ではstructを別個でつくらないといけない
ここではいくつかの構造体をpythonのclassによって定義する．

'''
# In[]:
class Scan2D():
    def __init__(self):
        pose = Pose2D()
        # std::vector<LPoint2D> lps;
        # 標準ライブラリのvectorを用いてLPoint2D型のlpsを定義するよ
        lps = LPoint2D # pythonでは動的配列のはずなので，これでよい？


# In[]:
'''
ソースコード：
#ifndef SCAN2D_H_
#define SCAN2D_H_

#include <vector>
#include "MyUtil.h"
#include "LPoint2D.h"
#include "Pose2D.h"

//////////

// スキャン
struct Scan2D
{
  static double MAX_SCAN_RANGE;              // スキャン点の距離値上限[m]
  static double MIN_SCAN_RANGE;              // スキャン点の距離値下限[m]

  int sid;                                   // スキャンid
  Pose2D pose;                               // スキャン取得時のオドメトリ値
  std::vector<LPoint2D> lps;                 // スキャン点群

  Scan2D() : sid(0) {
  }

  ~Scan2D() {
  }

///////

  void setSid(int s) {
    sid = s;
  }

  void setLps (const std::vector<LPoint2D> &ps) {
    lps = ps;
  }

  void setPose(Pose2D &p) {
    pose = p;
  }

};

#endif
'''
# In[]:
'''
LPoint2Dのクラス作成

'''
class ptype(Enum):
    UNKNOWN = 0 # 点のタイプの作成
    LINE = 1 # それぞれ，未知・直線・カーブ・孤立
    CORNER = 2
    ISOLATE = 3
class LPoint2D():
    def __init__(self, sid, x, y):
        self.sid = sid
        self.x, self.y = x, y
        self.nx, self.ny = 0, 0
        self.atd = 0

    def init(self,sid,atd,type,nx,ny):
        self.sid = -1
        self.nx, self.ny = 0, 0
        self.atd = 0
        type = ptype.UNKNOWN # 列挙型のインスタンスを作成
        return self.sid, self.atd, self.type, self.nx, self.ny

    def overload1(self,): # から引数のとき
        sid, atd, type, nx, ny = init(sid,atd,type,nx,ny)
        self.x = 0
        self.y = 0
        

# In[]
'''
MyUtilのクラス作成
おそらく中身は行列計算用？
だとしたらpyではわざわざクラスを作成する必要はない．
必要になったら作成

class MyUtil
{
public:
  MyUtil(void) {
  }

  ~MyUtil(void){
  }
  メモリ初期化と開放
///////////

  static int add(int a1, int a2);
  static double add(double a1, double a2);
  static double addR(double a1, double a2);
  int型とdouble型の和の計算だろうか

  static Eigen::Matrix3d svdInverse(const Eigen::Matrix3d &A);
  static void calEigen2D( double (*mat)[2], double *vals, double *vec1, double *vec2);

};
EigenはC++の行列ライブラリ
'''
