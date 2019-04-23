# In[]:
'''
struct Pose2Dの作成
this->tx = tx;
this->ty = ty;
this->th = th;
の部分をすべて無視して書いているためあとで訂正
'''
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

    '''
    ワケワカランポイント
    LPoint2D relativePoint(const LPoint2D &p) const;
    LPoint2D globalPoint(const LPoint2D &p) const;
    void globalPoint(const LPoint2D &pi, LPoint2D &po) const;

    static void calRelativePose(const Pose2D &npose, const Pose2D &bpose, Pose2D &relPose);
    static void calGlobalPose(const Pose2D &relPose, const Pose2D &bpose, Pose2D &npose);
    '''
