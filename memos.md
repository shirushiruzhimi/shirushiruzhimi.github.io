---
layout: default
title: メモページ
---

# 量が溜まってきたら整理すること　＞　未来の自分

# Python関係の忘備録
## 環境系
### Python
#### Pythonが動かない(MicrosoftStoreが開く)
- Windowsアップデートでパスの優先度が取られてしまっているので、『環境変数の編集』→『ユーザー環境変数』→『Path』を編集し、『...WindowsApp』を一番下に移動する。
### OpenCVが動かない
#### cv2.cv2 not found
- opencv-python をインストールする。`pip install opencv-python`
 - 既にインストールされている場合は、一度`pip uninstall opencv-python`してからもう一度実行する。
### TensorFlowが動かない
#### Session()がない
- TF2.0からはSessionが無くなったらしい。バージョンを1.xに落とせば動く。
### Anaconda
#### envが切り替えられない
- powershellを使っているとダメらしい。エラーすら出ないので気づき難いのが憎らしい。
- command promptあたりでやればよい。
 - 実際にやって出来た。
### JSON
#### 文字列を辞書にパースしたい
- json.load()
### OpenCV
#### cap.set()が効かない
- カメラidが合っているか確認する。(0だと思っていたら仮想デバイスに押されて1になってることがある）
### Blender
#### socketでプロセス間通信をしようとすると止まる。
- スクリプト実行するまでblenderはほかの動作を止める。
- したがって別のスレッドを立てて実行する必要がある。

#### 毎回忘れるクロスシムの手順
1. 布を用意する。<br>
 a. 厚みのないメッシュ、Subdivision Surfaceで頂点を増やしておく。<br>
 b. `Physics`→`Cloth`をクリックしてクロスシムを有効化。<br>
2. 布と相互作用するオブジェクトを用意する。<br>
 a. `Physics`→`Collision`をクリックして衝突判定を有効化する。<br>
 
#### 毎回忘れるオブジェクト毎のレンダリングと合成
- Compositingのレンダーレイヤーはビュー単位でインプットを取り扱う
- ビューは右上から選択する。デフォルトでView Layer
1. View Layerを複製する。
   - 分けたい数だけ複製する。
   - 現在の状態から分けたいなら、Copy Settingを選択すると表示するレイヤーの状態がコピーされて楽。
2. 編集したいView Layerを選択した状態で、Outliner(オブジェクトの一覧)から表示したいオブジェクトだけにチェックを入れる。
   - 可視状態はView Layerごとに管理している。
3. レンダリング後、Compositing画面で、Render Layerノードを複製し、下部のView Layerを所望のレイヤーに変更する。
4. `Color`→`Z combine`ノードを追加し、分離したViewのImageとZ値を繋ぐと合成してくれる。
- 背景を削除する際、`Film`->`Transparent`で消すと全部のViewから消えて不便。個別に設定できない。
   - 一度背景ありでレンダリングしてしまってから、Z値でしきい値を取って削除する。
   - 特に何も考えなくても、`Z combine`に入れる時に最も優先度が低くなる(Z->\inf)ので勝手に消えてくれる。
   
#### 影だけレンダリングしたい場合の設定
##### Eeveeの場合
- マテリアルで設定する。Alpha設定を影に反映されないようにし、Alpha=0とすればよい。
1. `Material` -> `Settings` -> `Blend Mode`を`Alpha Clip`
2. `Material` -> `Settings` -> `Shadow Mode`を`Opaque`
3. `Material` -> `Surface` -> `Alpha`を`0`にする
##### Cyclesの場合
- オブジェクトの設定でレイトレ時に無視するようにする。
1. `Object Properties` -> `Visibility` -> `Ray Visibility` -> `Camera`のチェックを外す

#### BVHについて
##### 概要
- モーキャプのアニメーションとArmatureのセット

##### 使い方
- File -> Import -> .bvh　だけでOK
- ImportされたArmatureにアニメーションがついてるので、今持ってるモデルにそのまま使える訳じゃない。
##### トレースする場合に逆回転する
- オイラー角じゃなくてクォータニオンを使う
[参考 dskjal様](https://dskjal.com/blender/eular-vs-quaternion-on-blender.html)

## Blender APIのGUI周りについて
### 変数の宣言
- [公式ドキュメント](https://docs.blender.org/api/current/bpy.props.html)
- 下記のようにSceneのメンバ変数を外から定義する。  
`bpy.types.Scene.test_variable= bpy.props.StringProperty(default = "skelton")`  
`bpy.types.Scene.test_variable= bpy.props.IntProperty(default = 1919)`  
`bpy.types.Scene.test_variable= bpy.props.FloatProperty(default = 191.9)`  
`bpy.types.Scene.test_variable= bpy.props.BoolProperty(default = True)`  
- プルダウンにしたい場合はEnumPropertyを定義する。左から順に(識別子, UI表示文, オンカーソル時の説明文)のセットをリストにしてitemsに設定。
   ```python
   bpy.types.Scene.test_variable= bpy.props.EnumProperty(items=[("A","displayA","descriptionA"),
      ("B","displayB","descriptionB")], default="A")`
   ```  
- まとめて定義する場合は、Property Groupを使う。(例は以下のコード)  
   - (公式ドキュメント)[https://docs.blender.org/api/current/bpy.props.html#propertygroup-example]  
### 入力UIの配置
```python
# Define parameters
class PROPERTY_SETTINGS(bpy.types.PropertyGroup):
    Target1_index :   bpy.props.IntProperty()
    Target1_scale :   bpy.props.FloatProperty()
    Target1_name :    bpy.props.StringProperty()
    Target1_types :   bpy.props.EnumProperty(items=[("A","displayA","descriptionA"),
      ("B","displayB","descriptionB")], default="A")
      
# Define and draw GUI panel
class UI_PANEL_TEST(bpy.types.Panel):
    # Name of panel
    bl_label = "Panel UI test"
    # The window the panel will be placed.
    bl_space_type = "VIEW_3D"
    # The region the panel will be placed.
    bl_region_type = "UI"

    def update_tree(self, context):
        self.do_update = True  

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        my_props = bpy.data.scenes[0]

        box = layout.box()        
        row = box.row()              
        row.prop(my_props.PROPERTY_SETTINGS, "Target1_index")
        row.prop(my_props.PROPERTY_SETTINGS, "Target1_scale") 
        row = box.row()               
        col = row.column()
        col.prop(my_props.PROPERTY_SETTINGS, "Target1_types")
        col.prop_search(my_props.PROPERTY_SETTINGS, "Target1_name", scene, "objects")
```
1. Propert Groupで使う変数を定義しておく。
2. `bpy.types.Panel`を継承したクラスを作る。
3. 名前と配置情報を`bl_***`に代入する。
4. `context`を引数に持つdrawメソッドを定義(オーバーライド?)する。
   - `context`にBlenderのcontextが入れられるので、`context.scene`などでsceneの情報を取得できる
5. `self.layout`の各種メソッドを呼ぶとUIが追記されていく。
   - 描画領域中に行を追加（改行）したい場合  
      `row = self.layout.row()`
   - 描画領域中に列を追加（改行）したい場合  
      `row = self.layout.column()`      
   - 描画領域のセットを追加したい場合  
      `box = self.layout.box()`
   - 上記領域の中に入れ子にして領域を定義することで柔軟にレイアウトできる。  
      ```python
      box = self.layout.box()
      row = box.row()
      col = row.column()
      ```
   - 戻り値(ポインタ)を捨てちゃうと後で追加できないので、複雑な場合は変数を分けておくといいかも。  
      ```python
      box1 = self.layout.box()   
      box2 = self.layout.box()   
      ```
6. 入力UIを設置する。
   - 以下のように、上記レイアウトからクラスとそのメンバ（String)を引数とした`prop()`を呼び出すと配置される。
   `col.prop(my_props.PROPERTY_SETTINGS, "Target1_types")`
   - シーン中に存在するオブジェクトから選択させたい場合、`prop_search()`を呼び出す。第3, 4引数は検索条件。
   `col.prop_search(my_props.PROPERTY_SETTINGS, "Target1_name", scene, "objects")
7. クラスを登録する。
```python
UTIL_CLASSES = (
    UI_PANEL_TEST,
)
def register():
    from bpy.utils import register_class
    for cls_v in UTIL_CLASSES:
        register_class(cls_v)
    register_class(PROPERTY_SETTINGS)
    bpy.types.Scene.PROPERTY_SETTINGS = bpy.props.PointerProperty(type=PROPERTY_SETTINGS)

def unregister():
    from bpy.utils import unregister_class
    for cls_v in UTIL_CLASSES:
        unregister_class(cls_v)
    del bpy.types.Scene.PROPERTY_SETTINGS
    unregister_class(PROPERTY_SETTINGS)             
if __name__ == "__main__":
    register()
```
- 別にクラスを定義する際は、そのクラスもregister_class()しなければいけないのでUTIL_CLASSESにまとめている
- Property Groupも登録しないと使えないので注意。

### VScode
#### 実行時にfailed to launch (exit code: 1)となる
- 既にほかの用途でVScodeを使っている場合、WSLで実行していないか確認する。
- ローカルにインストールしているならsettings.jsonのshellは`"C:/WINDOWS/System32/wsl.exe"`ではなく`"C:/WINDOWS/System32/cmd.exe"`にする。
- 切り替え面倒だな...
