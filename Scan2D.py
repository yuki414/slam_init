'''
Scan2Dのクラス作成
C++ではstructを別個でつくらないといけない
ここではいくつかの構造体をpythonのclassによって定義する．

たぶん大量の間違いがあるので変えていこうと思う
struct hogeはclass hogeによって代用
'''
# In[]:
class Scan2D():
    def __init__(self):
        self.sid = 0
        self.pose = Pose2D()
        # std::vector<LPoint2D> lps;
        # 標準ライブラリのvectorを用いてLPoint2D型のlpsを定義するよ
        lps = LPoint2D() # pythonでは動的配列のはずなので，これでよい？

    def setSid(self, s):
        self.sid = s

    def setPose(self, _p):
        self.pose = p
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
