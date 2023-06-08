bl_info = {
    "name": "未保存图片插件 unsaved image plugin",
    "author": "iskanime",
    "version": (0, 1),
    "blender": (3, 4, 1),
    "location": "无面板",
    "description": "如果有未保存的图片，会弹出窗口显示图片名称，可以复制名称后在图像编辑器中搜索图片",
    "category": "Object"
}

import bpy
from bpy.app.handlers import save_post
from bpy.app import driver_namespace

# 弹出窗口显示未保存的图片名称
class UnsaveImageMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_unsaved_image"
    bl_label = "未保存的图片"

    def draw(self, context):
        layout = self.layout
        for image in bpy.data.images:
            if image.is_dirty:
                # 在窗口中显示图片名称
                layout.prop(image, "name", text="")

# 保存图片处理器函数
def unsave_image_handler(dummy):
    for image in bpy.data.images:
            if image.is_dirty:
                bpy.ops.wm.call_menu(name="OBJECT_MT_unsaved_image")
                break

classes = [UnsaveImageMenu] 

# 保存图片处理器函数值在driver_namespace中存储的键值
handler_key = "UNSAVE_IMAGE_01"

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # 注册处理器函数
    if handler_key in driver_namespace:
        if driver_namespace[handler_key] in save_post:
            save_post.remove(driver_namespace[handler_key])

        del driver_namespace[handler_key]

    save_post.append(unsave_image_handler)
    driver_namespace[handler_key] = unsave_image_handler


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    save_post.remove(driver_namespace[handler_key])
    
if __name__ == "__main__":
    register()