from glob import glob
from pathlib import Path

from brainrender.scene import Scene

from injectionmapping.vis.vis_tools import load_obj_into_brainrender

##############################################################################
"""
OPTIONS ETC
"""
# directory containing the directories with the .obj files
master_directory = "/media/adam/Storage/cellfinder/analysis/inj_segment"

# If True, display region names when hovering
flag = True

# If True, display RSP as wireframe (not solid)
RSP_wireframe = True

# Transparency of the rendered region
region_alpha = 0.8

# Object shading type ("flat", "giroud" or "phong")
region_shading = "flat"

##############################################################################

# Get all .obj files
master_directory = Path(master_directory)
glob_pattern = str(master_directory / "**/*.obj")
list_obj_files = glob(glob_pattern, recursive=True)

# Create a scene
scene = Scene()

# Add RSP
scene.add_brain_regions(
    ["RSP"], use_original_color=True, wireframe=RSP_wireframe
)
if flag:
    scene.actors["regions"]["RSP"].flag("RSP")

# Add regions
for obj_file in list_obj_files:
    obj_path = Path(obj_file)
    load_obj_into_brainrender(
        scene,
        obj_file,
        alpha=region_alpha,
        shading="flat",
        flag=flag,
        name=str(Path(obj_file).stem),
    )

# Display
scene.render()
