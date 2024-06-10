import mitsuba as mi
import numpy as np
import os

mi.set_variant('llvm_ad_rgb')

def create_scene(light_position, camera_position, intrinsic, distortion, camera_name, blob_filename):
    # Calculate the field of view from the focal length, assuming the sensor is 1280 pixels wide
    sensor_width = 1280 
    fov = 2 * np.arctan(sensor_width / (2 * intrinsic[0, 0])) * 180 / np.pi  # FOV in degrees
    
    camera = mi.load_dict({
        'type': 'perspective',
        'to_world': mi.ScalarTransform4f.look_at(
            origin=mi.ScalarPoint3f(camera_position),
            target=mi.ScalarPoint3f(0, 0, 0),
            up=mi.ScalarVector3f(0, 1, 0)
        ),
        'fov_axis': 'x',
        'fov': fov,
        'sampler': {
            'type': 'independent',
            'sample_count': 64
        },
        'film': {
            'type': 'hdrfilm',
            'width': 1280,
            'height': 720,
            'rfilter': {'type': 'box'}
        }
    })

    # Light (single light)
    light = {
        'type': 'point',
        'position': mi.ScalarPoint3f(light_position),
        'intensity': {
            'type': 'spectrum',
            'value': 10000  # Increased intensity
        }
    }

    # Scene dictionary with BSDF for blob object
    scene_dict = {
        'type': 'scene',
        'integrator': {
            'type': 'path'
        },
        camera_name: camera,
        'blob': {
            'type': 'obj',
            'filename': f'blobs/obj/{blob_filename}',
            'to_world': mi.ScalarTransform4f.translate([0, 0, 0]) @ mi.ScalarTransform4f.scale([0.1, 0.1, 0.1]),  # Adjusted scaling to approximately 100 mm diameter
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': [0.5, 0.5, 0.5]  # Lightened the material
                }
            }
        },
        'light_0': light
    }

    return scene_dict

# Camera parameters from the text file
left_camera_position = [-17.5, 0, 0]
left_camera_intrinsic = np.array([
    [641.843486, 0, 638.93610662],
    [0, 643.53319355, 393.7352744],
    [0, 0, 1]
])
left_camera_distortion = np.array([
    [-0.05996174, 0.07897343, -0.00136181, 0.00177076, -0.03504367]
])

right_camera_position = [32.5, 0, 0]
right_camera_intrinsic = np.array([
    [644.32498369, 0, 654.6296148],
    [0, 645.56357309, 399.63693664],
    [0, 0, 1]
])
right_camera_distortion = np.array([
    [-0.06324747, 0.10364505, 0.00057975, 0.00352207, -0.0773982]
])

# Light positions from the text file (already in millimeters)
light_positions = np.array([
    [200, 0, 305],
    [190.211303, 61.803399, 305],
    [161.803399, 117.557050, 305],
    [117.557050, 161.803399, 305],
    [61.803399, 190.211303, 305],
    [1.22464680e-14, 200, 305],
    [-61.803399, 190.211303, 305],
    [-117.557050, 161.803399, 305],
    [-161.803399, 117.557050, 305],
    [-190.211303, 61.803399, 305],
    [-200, 2.44929360e-14, 305],
    [-190.211303, -61.803399, 305],
    [-161.803399, -117.557050, 305],
    [-117.557050, -161.803399, 305],
    [-61.803399, -190.211303, 305],
    [-3.67394040e-14, -200, 305],
    [61.803399, -190.211303, 305],
    [117.557050, -161.803399, 305],
    [161.803399, -117.557050, 305],
    [190.211303, -61.803399, 305]
])

# Blob filenames
blob_filenames = [f'blob0{i+1}.obj' for i in range(10)]

# Create directories if they do not exist
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Generate and save images
for blob_filename in blob_filenames:
    for i, light_position in enumerate(light_positions):
        # Create directories for each blob and each camera view
        left_path = f"images/{blob_filename}/left"
        right_path = f"images/{blob_filename}/right"
        create_directory(left_path)
        create_directory(right_path)

        # Left camera
        scene_dict = create_scene(light_position, left_camera_position, left_camera_intrinsic, left_camera_distortion, 'sensor_0', blob_filename)
        scene = mi.load_dict(scene_dict)
        image = mi.render(scene)
        mi.util.write_bitmap(f"{left_path}/{i+1:02d}.png", image)

        # Right camera
        scene_dict = create_scene(light_position, right_camera_position, right_camera_intrinsic, right_camera_distortion, 'sensor_1', blob_filename)
        scene = mi.load_dict(scene_dict)
        image = mi.render(scene)
        mi.util.write_bitmap(f"{right_path}/{i+1:02d}.png", image)
