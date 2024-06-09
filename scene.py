import mitsuba as mi
import numpy as np

mi.set_variant('llvm_ad_rgb')

def create_scene():
    # Function to create the camera
    def create_camera(name, position, intrinsic, distortion):
        camera = mi.load_dict({
            'type': 'perspective',
            'to_world': mi.ScalarTransform4f.look_at(
                origin=mi.ScalarPoint3f(position),
                target=mi.ScalarPoint3f(0, 0, 0),
                up=mi.ScalarVector3f(0, 1, 0)
            ),
            'fov_axis': 'x',
            'fov': 45,
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
        return camera

    # Left camera parameters
    left_camera_position = [-17.5, 0, 0]
    left_camera_intrinsic = np.array([
        [641.843486, 0, 638.93610662],
        [0, 643.53319355, 393.7352744],
        [0, 0, 1]
    ])
    left_camera_distortion = np.array([
        [-0.05996174, 0.07897343, -0.00136181, 0.00177076, -0.03504367]
    ])

    # Right camera parameters
    right_camera_position = [32.5, 0, 0]
    right_camera_intrinsic = np.array([
        [644.32498369, 0, 654.6296148],
        [0, 645.56357309, 399.63693664],
        [0, 0, 1]
    ])
    right_camera_distortion = np.array([
        [-0.06324747, 0.10364505, 0.00057975, 0.00352207, -0.0773982]
    ])

    # Create cameras
    left_camera = create_camera('left_camera', left_camera_position, left_camera_intrinsic, left_camera_distortion)
    right_camera = create_camera('right_camera', right_camera_position, right_camera_intrinsic, right_camera_distortion)

    # Light positions
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

    # Create lights
    lights = {}
    for i, pos in enumerate(light_positions):
        lights[f'light_{i}'] = {
            'type': 'point',
            'position': mi.ScalarPoint3f(pos),
            'intensity': {
                'type': 'spectrum',
                'value': 300
            }
        }

    # Scene dictionary with BSDF for blob object
    scene_dict = {
        'type': 'scene',
        'integrator': {
            'type': 'path'
        },
        'left_camera': left_camera,
        'right_camera': right_camera,
        'blob': {
            'type': 'obj',
            'filename': 'blobs/obj/blob01.obj',
            'to_world': mi.ScalarTransform4f.translate([7.5, 0, 0]),
            'bsdf': {
                'type': 'diffuse',
                'reflectance': {
                    'type': 'rgb',
                    'value': [0.1, 0.1, 0.1]
                }
            }
        }
    }

    # Add lights to the scene dictionary
    scene_dict.update(lights)
    return scene_dict

