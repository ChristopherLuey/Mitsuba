import mitsuba as mi
from scene import *

# MacOS
mi.set_variant('llvm_ad_rgb') # CPU vectorized using llvm

# Create the scene
scene_dict = create_scene()

# Load the scene
scene = mi.load_dict(scene_dict)

# Render the scene
image = mi.render(scene)

# Save the rendered image
mi.util.write_bitmap("output.png", image)


