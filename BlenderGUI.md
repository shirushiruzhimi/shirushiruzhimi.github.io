# Blender APIに関するメモ  
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
      ("B","displayB","descriptionB")], default="A")
   ```  
- まとめて定義する場合は、Property Groupを使う。(例は以下のコード)  
   - [公式ドキュメント](https://docs.blender.org/api/current/bpy.props.html#propertygroup-example)  
   
### 入力UIの配置  
- とりあえず作ったコードを基に説明  
[Basic_panel.py](./samples/Basic_panel.py)

```python
import bpy

# Define parameters
class PROPERTY_SETTINGS(bpy.types.PropertyGroup):
    Target1_index :   bpy.props.IntProperty()
    Target1_scale :   bpy.props.FloatProperty()
    Target1_name :    bpy.props.StringProperty()
    Target1_types :   bpy.props.EnumProperty(items=[("A","displayA","descriptionA"),
      ("B","displayB","descriptionB")], default="A")
      
# Define and draw GUI panel
class UI_PT_PANEL_TEST(bpy.types.Panel):
    # Name of panel
    bl_label = "Panel UI test"
    # The window the panel will be placed.
    bl_space_type = "VIEW_3D"
    # The region the panel will be placed.
    bl_region_type = "UI"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        my_props = bpy.data.scenes[0]

        box = layout.box()        
        row1 = box.row()         
        row1.prop(my_props.PROPERTY_SETTINGS, "Target1_index")
        row1.prop(my_props.PROPERTY_SETTINGS, "Target1_scale") 
        row2 = box.row()               
        col = row2.column()
        col.prop(my_props.PROPERTY_SETTINGS, "Target1_types")
        col.prop_search(my_props.PROPERTY_SETTINGS, "Target1_name", scene, "objects")
        if my_props.PROPERTY_SETTINGS.Target1_name != "":
            print(bpy.data.objects[my_props.PROPERTY_SETTINGS.Target1_name].type)
```

1. Propert Groupで使う変数を定義しておく。  
   - 名前に_PT_と入れるのを推奨されている。（入れないとwarningが出る）  
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
   `col.prop_search(my_props.PROPERTY_SETTINGS, "Target1_name", scene, "objects")`
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


### TIPS
- プロパティについて  
[Property Definitions](https://docs.blender.org/api/current/bpy.props.html)  
- レイアウトのメソッドについて  
[UILayout](https://docs.blender.org/api/current/bpy.types.UILayout.html)  
  - 特にpropで指定するものについて  
  [prop()](https://docs.blender.org/api/current/bpy.types.UILayout.html?highlight=icon#bpy.types.UILayout.prop)  
- Constraintsの種類やプロパティなど  
[Constraint](https://docs.blender.org/api/current/bpy.types.Constraint.html#bpy.types.Constraint)  

- ファイルの入出力  
   - `bpy_extras.io_utils.ImportHelper`や`bpy_extras.io_utils.ExportHelper`を継承したクラスを使う