
import bpy

# Define and draw GUI panel
class UI_PT_PANEL_TEST(bpy.types.Panel):
    # Name of panel
    bl_label = "Panel UI test"
    # The window the panel will be placed.
    bl_space_type = "VIEW_3D"
    # The region the panel will be placed.
    bl_region_type = "UI"

    def draw(self, context):
        print("HI")
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

# Define parameters
class PROPERTY_SETTINGS(bpy.types.PropertyGroup):
    Target1_index :   bpy.props.IntProperty()
    Target1_scale :   bpy.props.FloatProperty()
    Target1_name :    bpy.props.StringProperty()
    Target1_types :   bpy.props.EnumProperty(items=[("A","displayA","descriptionA"),
      ("B","displayB","descriptionB")], default="A")

UTIL_CLASSES = (
    UI_PT_PANEL_TEST,
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

