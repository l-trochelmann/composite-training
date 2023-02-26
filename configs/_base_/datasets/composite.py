dataset_info = dict(

    dataset_name='composite',

    paper_info=dict(
        author='Leon Trochelmann',
        title='Composite Dataset Training for Improved Pose Detection in the Wild',
        container='',
        year='2023',
        homepage='',
    ),

    # legacy keypoints order:   
    # coco: [nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle]  
    # aic:  [right_shoulder, right_elbow, right_wrist, left_shoulder, left_elbow, left_wrist, right_hip, right_knee, right_ankle, left_hip, left_knee, left_ankle, head_top, neck]
    # composite keypoint order:
    # [head_top, left_eye, right_eye, left_ear, right_ear, nose, neck, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle]
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

        11: dict(link=('right_shoulder', 'neck'), id=11, color=[0, 0, 255]),
        12: dict(link=('neck', 'left_shoulder'), id=12, color=[0, 0, 255]),
        13: dict(link=('head_top', 'neck'), id=13, color=[0, 0, 255]),

        14: dict(link=('left_eye', 'right_eye'), id=14, color=[255, 0, 0]),
        15: dict(link=('nose', 'left_eye'), id=15, color=[255, 0, 0]),
        16: dict(link=('nose', 'right_eye'), id=16, color=[255, 0, 0]),
        17: dict(link=('left_eye', 'left_ear'), id=17, color=[255, 0, 0]),
        18: dict(link=('right_eye', 'right_ear'), id=18, color=[255, 0, 0]),
        19: dict(link=('left_ear', 'left_shoulder'), id=19, color=[255, 0, 0]),
        20: dict(link=('right_ear', 'right_shoulder'), id=20, color=[255, 0, 0]),
        21: dict(link=('left_shoulder', 'right_shoulder'), id=21, color=[255, 0, 0])
    },

    # for the composite joint weights, coco and aic weights did already match for the common weights, 
    #   and for non-common weights the respective original weight was used 
    joint_weights=[1., 1., 1., 1., 1., 1., 1., 1., 1., 1.2, 1.2, 1.5, 1.5, 1., 1., 1.2, 1.2, 1.5, 1.5],


    # todo: update sigmas

    # 'https://github.com/AIChallenger/AI_Challenger_2017/blob/master/'
    # 'Evaluation/keypoint_eval/keypoint_eval.py#L50'
    # delta = 2 x sigma
    sigmas=[
        0.01388152, 0.01515228, 0.01057665, 0.01417709, 0.01497891, 0.01402144,
        0.03909642, 0.03686941, 0.01981803, 0.03843971, 0.03412318, 0.02415081,
        0.01291456, 0.01236173
    ])
