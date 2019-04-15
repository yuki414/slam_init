# In[]:
'''
struct LPoint2D
LPoint2Dのクラス作成
'''
# !!:クラスにするか関数にするか
def ptype(Enum):
    UNKNOWN = 0 # 点のタイプの作成
    LINE = 1 # それぞれ，未知・直線・カーブ・孤立
    CORNER = 2
    ISOLATE = 3

# struct LPoint2D
class LPoint2D():
    def __init__(self):
        LPoint2D.init(self) # どこのメソッドか明示すればおｋ，インスタンス自身が引数である必要がある
        # self.sid = -1
        # self.x, self.y = 0, 0
        # self.atd = 0
        # self.type = 'UNKNOWN'
        # self.nx, self.ny = 0, 0
    # オーバーロードできないので別の初期化メソッドを用意する
    def init_3arg(self, id, _x, _y):
        LPoint2D.init(self) # init関数のあとでidなどを代入するのでsidは変わる
        self.sid = id
        self.x = _x
        self.y = _y

    def init(self):
        self.sid = -1
        self.atd = 0
        self.type = 'UNKNOWN'
        self.nx = 0
        self.ny = 0

    # コードてきには3argの初期化メソッドとかわらない．．．
    def setData(self, id, _x, _y):
        LPoint2D.init(self)
        self.sid = id
        self.x = _x
        self.y = _y

    def setXY(self, _x, _y):
        self.x = _x
        self.y = _y

    # angeとangleからxyを求める(右手系)
    def calXY(self, range, angle):
        a = math.radians(angle)
        self.x = range*math.cos(a)
        self.y = range*math.sin(a)

    # rangeとangleからxyを求める(左手系）
    def calXYi(self, range, angle):
        a = math.radians(a)
        self.x = range*math.cos(a)
        self.y = -range*math.sin(a)

    def setSid(self, i):
        self.sid = i

    def setAtd(self, t):
        self.atd = t

    def setType(self, t):
        self.type = t

    def setNormal(self, x, y):
        self.nx = x
        self.ny = y
