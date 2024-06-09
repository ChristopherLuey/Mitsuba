import mitsuba as mi
from scene import *

# MacOS
mi.set_variant('llvm_ad_rgb') # CPU vectorized using llvm

scene_dict = create_scene()

# 1: Load the scene
scene = mi.load_dict(scene_dict)

# 2: Render the scene
image = mi.render(scene, spp=256)

# 3: Save the image
mi.util.write_bitmap("my_first_render.png", image)

