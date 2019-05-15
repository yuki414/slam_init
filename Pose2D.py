# In[]:
'''
struct Pose2Dの作成
this->tx = tx;
this->ty = ty;
this->th = th;
の部分をすべて無視して書いているためあとで訂正
'''
import numpy as np
import math # rad2deg:.degrees(), deg2rad:.radians()
class Pose2D():
    def __init__(self):
        self.tx = 0
        self.ty = 0
        self.th = 0
        self.Rmat = np.eye(2) # Rmatは2x2の単位行列

    def init_3arg(self, tx, ty, th):
        self.tx = tx
        self.ty = ty
        self.th = th
        self.calRmat(self)

    def init_4arg(self, mat, tx, ty, th):
        self.Rmat = mat # ただしmatは2x2行列
        self.tx = tx
        self.ty = ty
        self.th = th

    def reset(self):
        self.tx, self.ty, self.th = 0, 0, 0
        self.calRmat()

    def setVal(self, x, y, a):
        self.tx = x
        self.ty = y
        self.th = a
        self.calRmat()

    def calRmat(self):
        a = math.radians(self.th)
        # self.Rmat[0,0], self.Rmat[1,1] = math.cos(a), math.cos(a)
        self.Rmat = np.array([[math.cos(a), -math.sin(a)],
                              [math.sin(a), math.cos(a)]])

    def setTranslation(self, tx, ty):
        self.tx = tx
        self.ty = ty

    def setAngle(self, th):
        self.th = th

    def relativePoint(self, _p):
        # p = LPoint2D()で与えられている
        self.dx = _p.x - self.tx
        self.dy = _p.y - self.ty
        self.x = self.dx*self.Rmat[0][0] + self.dy*self.Rmat[1][0]
        self.y = self.dx*self.Rmat[1][0] + self.dy*self.Rmat[1][1]
        return LPoint2D(p.sid, x, y) # !!:return LPoint2dの意味がよくわかないため放置

    # 自分（Pose2D）の局所座標系での点pを、グローバル座標系に変換
    def globalPoint_single(self, _p):
        self.x = self.Rmat[0][0]*_p.x + self.Rmat[0][1]*_p.y + self.tx
        self.y = self.Rmat[1][0]*_p.x + self.Rmat[1][1]*_p.y + self.ty
        return LPoint2D(p.sid, x, y)

    # 自分（Pose2D）の局所座標系での点pを、グローバル座標系に変換してpoに入れる
    def globalPoint_double(self, _pi, _po):
        # pi,po両方LPoint2Dを継承
        _po.x = self.Rmat[0][0]*_pi.x + self.Rmat[0][1]*_pi.y + self.tx
        _po.y = self.Rmat[1][0]*_pi.x + self.Rmat[1][1]*_pi.y + self.ty
        # このメソッドはvoidのため返り値なし．ただしpi,poはポインタを指してるためpoは変化があるはず

    # 基準座標系bposeから見た現座標系nposeの相対位置relPoseを求める（Inverse compounding operator）
    def calRelativePose(_npose, _bpose, _relPose):
        # ここでしか使わない変数だからインスタンスに含めなくてもいいかも？
        # と思ったがそもそもR1,R2はここでも使われてないからどうしていいかわからん
        R0 = _bpose.Rmat
        R1 = _npose.Rmat
        R2 = _relPose.Rmat

        # ソースコードはこれ意味わからん
        # const double (*R0)[2] = bpose.Rmat;           // 基準座標系
        # const double (*R1)[2] = npose.Rmat;           // 現座標系
        # double (*R2)[2] = relPose.Rmat;               // 相対位置

        # 並進
        dx = _npose.tx - _bpose.tx
        dy = _npose.ty - _bpose.ty
        _relPose.tx = R0[0][0]*dx + R0[1][0]*dy
        _relPose.ty = R0[0][1]*dx + R0[1][1]*dy

        # 回転
        th = _npose.th - _bpose.th
        if (th< -180):
            th = th + 360
        elif (th >= 180):
            th = th - 360
        _relPose.th = th # !!:relはポインタが指定されてるのでこれをしても意味がないのでは
        _relPose.calRmat()

    # void Pose2D::calGlobalPose(const Pose2D &relPose, const Pose2D &bpose, Pose2D &npose)
    # このPose2Dを定義するために用いているrelPoseとかもまたPose2Dなわけだけどなんなんだろうこれは
    # 基準座標系bposeから相対位置relPoseだけ進んだ、座標系nposeを求める（Compounding operator）
    def calGlobalPose(self, _relPose, _bpose, _npose):
        self.R0 = _bpose.Rmat
        self.R1 = _relPose.Rmat
        self.R2 = _npose.Rmat

        # 並進
        self.tx = _relPose.tx
        self.ty = _relPose.ty
        _npose.tx = self.R0[0][0]*self.tx + self.R0[0][1]*self.ty + _bpose.tx
        _npose.ty = self.R0[1][0]*self.tx + self.R0[1][1]*self.ty + _bpose.ty

        # 角度
        self.th = _bpose.th + _relPose.th
        if (self.th < -180):
            self.th = self.th + 360
        elif (self.th >= 180):
            self.th = self.th - 360
        _npose.th = th # 上述同様
        _npose.calRmat()


    '''
    ワケワカランポイント
    と思ったらPose2D.cppを見てなかったためそれのせいかも
    LPoint2D relativePoint(const LPoint2D &p) const;
    LPoint2D globalPoint(const LPoint2D &p) const;
    void globalPoint(const LPoint2D &pi, LPoint2D &po) const;

    static void calRelativePose(const Pose2D &npose, const Pose2D &bpose, Pose2D &relPose);
    static void calGlobalPose(const Pose2D &relPose, const Pose2D &bpose, Pose2D &npose);
    '''
