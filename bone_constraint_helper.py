import bpy

bl_info = {
    "name": "Bone Constraint Helper",
    "author": "Rapilias",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "",
    "description": "Add bone helper on pose menu.",
    "warning": "",
    "doc_url": "",
    "category": "Bone",
}

class BoneConstraintHelper(bpy.types.Operator):
    bl_idname = "object.rapilias_bone_constraint_helper"
    bl_label = "Bone Constraint Helper"

    axis: bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.context.object
        if obj and obj.type == 'ARMATURE' and obj.mode == 'POSE':
            bone = bpy.context.active_pose_bone
            if bone:
                loc_constraint = bone.constraints.new('LIMIT_LOCATION')
                loc_constraint.use_min_x = loc_constraint.use_max_x = True
                loc_constraint.use_min_y = loc_constraint.use_max_y = True
                loc_constraint.use_min_z = loc_constraint.use_max_z = True
                loc_constraint.owner_space = 'LOCAL'

                rot_constraint = bone.constraints.new('LIMIT_ROTATION')
                rot_constraint.use_limit_x = 'X' in self.axis
                rot_constraint.use_limit_y = 'Y' in self.axis
                rot_constraint.use_limit_z = 'Z' in self.axis
                rot_constraint.owner_space = 'LOCAL'

                print(f"Added constraints for axis: {self.axis}")
                bpy.ops.ed.undo_push(message="Add constraints")
        return {'FINISHED'}

class BoneConstraintPositionFreeMenu(bpy.types.Menu):
    bl_idname = "object.rapilias_bone_constraint_helper_position_free"
    bl_label = "PositionFree"

    def draw(self, context):
        layout = self.layout
        layout.operator(BoneConstraintHelper.bl_idname, text="X").axis = "X"
        layout.operator(BoneConstraintHelper.bl_idname, text="Y").axis = "Y"
        layout.operator(BoneConstraintHelper.bl_idname, text="Z").axis = "Z"
        layout.operator(BoneConstraintHelper.bl_idname, text="XY").axis = "XY"
        layout.operator(BoneConstraintHelper.bl_idname, text="XZ").axis = "XZ"
        layout.operator(BoneConstraintHelper.bl_idname, text="YZ").axis = "YZ"
        layout.operator(BoneConstraintHelper.bl_idname, text="XYZ").axis = "XYZ"

class BoneConstraintPositionFixedMenu(bpy.types.Menu):
    bl_idname = "object.rapilias_bone_constraint_helper_position_fixed"
    bl_label = "PositionFixed"

    def draw(self, context):
        layout = self.layout
        layout.operator(BoneConstraintHelper.bl_idname, text="X").axis = "X"
        layout.operator(BoneConstraintHelper.bl_idname, text="Y").axis = "Y"
        layout.operator(BoneConstraintHelper.bl_idname, text="Z").axis = "Z"
        layout.operator(BoneConstraintHelper.bl_idname, text="XY").axis = "XY"
        layout.operator(BoneConstraintHelper.bl_idname, text="XZ").axis = "XZ"
        layout.operator(BoneConstraintHelper.bl_idname, text="YZ").axis = "YZ"
        layout.operator(BoneConstraintHelper.bl_idname, text="XYZ").axis = "XYZ"

def register():
    bpy.utils.register_class(BoneConstraintHelper)
    bpy.utils.register_class(BoneConstraintPositionFreeMenu)
    bpy.utils.register_class(BoneConstraintPositionFixedMenu)
    bpy.types.VIEW3D_MT_pose_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(BoneConstraintHelper)
    bpy.utils.unregister_class(BoneConstraintPositionFreeMenu)
    bpy.utils.unregister_class(BoneConstraintPositionFixedMenu)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(menu_func)

def menu_func(self, context):
    self.layout.menu(BoneConstraintPositionFreeMenu.bl_idname)
    self.layout.menu(BoneConstraintPositionFixedMenu.bl_idname)

if __name__ == "__main__":
    register()