dataset_info = dict(

    dataset_name='composite',

    paper_info=dict(
        author='Leon Trochelmann',
        title='Composite Dataset Training for Improved Pose Detection in the Wild',
        container='',
        year='2023',
        homepage='',
    ),

    keypoint_info = {
        0: dict(
            name='head_top',
            id=0,
            color=[51, 153, 255],
            type='upper',
            swap=''),
        1: dict(
            name='left_eye',
            id=1,
            color=[51, 153, 255],
            type='upper',
            swap='right_eye'),
        2: dict(
            name='right_eye',
            id=2,
            color=[51, 153, 255],
            type='upper',
            swap='left_eye'),
        3: dict(
            name='left_ear',
            id=3,
            color=[51, 153, 255],
            type='upper',
            swap='right_ear'),
        4: dict(
            name='right_ear',
            id=4,
            color=[51, 153, 255],
            type='upper',
            swap='left_ear'),
        5: dict(
            name='nose',
            id=5,
            color=[51, 153, 255],
            type='upper', 
            swap=''),
        6: dict(
            name='neck', 
            id=6, 
            color=[51, 153, 255], 
            type='upper', 
            swap=''),
        7: dict(
            name='left_shoulder',
            id=7,
            color=[0, 255, 0],
            type='upper',
            swap='right_shoulder'),
        8: dict(
            name='right_shoulder',
            id=8,
            color=[255, 128, 0],
            type='upper',
            swap='left_shoulder'),
        9: dict(
            name='left_elbow',
            id=9,
            color=[0, 255, 0],
            type='upper',
            swap='right_elbow'),
        10: dict(
            name='right_elbow',
            id=10,
            color=[255, 128, 0],
            type='upper',
            swap='left_elbow'),
        11: dict(
            name='left_wrist',
            id=11,
            color=[0, 255, 0],
            type='upper',
            swap='right_wrist'),
        12: dict(
            name='right_wrist',
            id=12,
            color=[255, 128, 0],
            type='upper',
            swap='left_wrist'),
        13: dict(
            name='left_hip',
            id=13,
            color=[0, 255, 0],
            type='lower',
            swap='right_hip'),
        14: dict(
            name='right_hip',
            id=14,
            color=[255, 128, 0],
            type='lower',
            swap='left_hip'),
        15: dict(
            name='left_knee',
            id=15,
            color=[0, 255, 0],
            type='lower',
            swap='right_knee'),
        16: dict(
            name='right_knee',
            id=16,
            color=[255, 128, 0],
            type='lower',
            swap='left_knee'),
        17: dict(
            name='left_ankle',
            id=17,
            color=[0, 255, 0],
            type='lower',
            swap='right_ankle'),
        18: dict(
            name='right_ankle',
            id=18,
            color=[255, 128, 0],
            type='lower',
            swap='left_ankle')
    },

    # common links in purple, aic-only links in blue, coco-only links in red
    skeleton_info={
        0: dict(link=('right_wrist', 'right_elbow'), id=0, color=[255, 0, 255]),
        1: dict(link=('right_elbow', 'right_shoulder'), id=1, color=[255, 0, 255]),
        2: dict(link=('left_shoulder', 'left_elbow'), id=2, color=[255, 0, 255]),
        3: dict(link=('left_elbow', 'left_wrist'), id=3, color=[255, 0, 255]),
        4: dict(link=('right_ankle', 'right_knee'), id=4, color=[255, 0, 255]),
        5: dict(link=('right_knee', 'right_hip'), id=5, color=[255, 0, 255]),
        6: dict(link=('right_hip', 'left_hip'), id=6, color=[255, 0, 255]),
        7: dict(link=('left_hip', 'left_knee'), id=7, color=[255, 0, 255]),
        8: dict(link=('left_knee', 'left_ankle'), id=8, color=[255, 0, 255]),
        9: dict(link=('right_shoulder', 'right_hip'), id=9, color=[255, 0, 255]),
        10: dict(link=('left_shoulder', 'left_hip'), id=10, color=[255, 0, 255]),
        11: dict(link=('left_shoulder', 'right_shoulder'), id=11, color=[255, 0, 255]),

        12: dict(link=('right_shoulder', 'neck'), id=12, color=[0, 0, 255]),
        13: dict(link=('neck', 'left_shoulder'), id=13, color=[0, 0, 255]),
        14: dict(link=('head_top', 'neck'), id=14, color=[0, 0, 255]),

        15: dict(link=('left_eye', 'right_eye'), id=15, color=[255, 0, 0]),
        16: dict(link=('nose', 'left_eye'), id=16, color=[255, 0, 0]),
        17: dict(link=('nose', 'right_eye'), id=17, color=[255, 0, 0]),
        18: dict(link=('left_eye', 'left_ear'), id=18, color=[255, 0, 0]),
        19: dict(link=('right_eye', 'right_ear'), id=19, color=[255, 0, 0]),
        20: dict(link=('left_ear', 'left_shoulder'), id=20, color=[255, 0, 0]),
        21: dict(link=('right_ear', 'right_shoulder'), id=21, color=[255, 0, 0])
    },

    joint_weights=[1., 1., 1., 1., 1., 1., 1., 1., 1., 1.2, 1.2, 1.5, 1.5, 1., 1., 1.2, 1.2, 1.5, 1.5],

    # sigmas created by calculating from AIC and COCO sigmas
    # necessary for eval during composite training but not recommended to use for conclusions
    sigmas=[0.01291456, 0.025, 0.025, 0.035, 0.035, 0.026, 0.01236173, 0.0421436598093409, 0.04210130459424179, 
    0.036182338706306494, 0.036422573620422026, 0.030655928110977716, 0.02977796138264048, 0.06210660926448471, 
    0.06244901144807664, 0.05015083471299594, 0.05167741980833102, 0.045610413654848594, 0.043919830609138295])
