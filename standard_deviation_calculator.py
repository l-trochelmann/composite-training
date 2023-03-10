import json, math

PATH_TO_COCO_ANNOTATIONS = "./data/coco/annotations/person_keypoints_train2017.json"
PATH_TO_AIC_ANNOTATIONS = "./data/aic/annotations/aic_train.json"

with open(PATH_TO_COCO_ANNOTATIONS, "r") as coco_json:
    coco= json.load(coco_json)
with open(PATH_TO_AIC_ANNOTATIONS, "r") as aic_json:
    aic = json.load(aic_json)

aic_kpt_counts = [0] * 14
coco_kpt_counts = [0] * 17

for annotation in aic["annotations"]:
    visibilities = annotation["keypoints"][2::3]
    for i in range(len(visibilities)):
        if visibilities[i] != 0:  # MIGHT DIFFER if flag 1 annotations are ignored
            aic_kpt_counts[i] += 1

for annotation in coco["annotations"]:
    visibilities = annotation["keypoints"][2::3]
    for i in range(len(visibilities)):
        if visibilities[i] != 0:  # MIGHT DIFFER if flag 1 annotations are ignored
            coco_kpt_counts[i] += 1

aic_sigmas=[
        0.01388152, 0.01515228, 0.01057665, 0.01417709, 0.01497891, 0.01402144,
        0.03909642, 0.03686941, 0.01981803, 0.03843971, 0.03412318, 0.02415081,
        0.01291456, 0.01236173
]

coco_sigmas=[
        0.026, 0.025, 0.025, 0.035, 0.035, 0.079, 0.079, 0.072, 0.072, 0.062,
        0.062, 0.107, 0.107, 0.087, 0.087, 0.089, 0.089
]

composite_sigmas = [0]*19

def calc_sigma(aic_kpt_idx, coco_kpt_idx):
    N_aic  = aic_kpt_counts[aic_kpt_idx]
    N_coco = coco_kpt_counts[coco_kpt_idx]
    SIGMA_aic = aic_sigmas[aic_kpt_idx]
    SIGMA_coco = coco_sigmas[coco_kpt_idx]

    return math.sqrt(((N_aic/(N_aic+N_coco))*(SIGMA_aic**2)) + ((N_coco/(N_coco+N_aic))*(SIGMA_coco**2)))


# legacy keypoints order:   
# aic:  [right_shoulder, right_elbow, right_wrist, left_shoulder, left_elbow, left_wrist, right_hip, right_knee, right_ankle, left_hip, left_knee, left_ankle, head_top, neck]
# coco: [nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle]  
# composite keypoint order:
# [head_top, left_eye, right_eye, left_ear, right_ear, nose, neck, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle]

composite_sigmas[0] = aic_sigmas[12]
composite_sigmas[1] = coco_sigmas[1]
composite_sigmas[2] = coco_sigmas[2]
composite_sigmas[3] = coco_sigmas[3]
composite_sigmas[4] = coco_sigmas[4]
composite_sigmas[5] = coco_sigmas[0]
composite_sigmas[6] = aic_sigmas[13]
composite_sigmas[7] = calc_sigma( 3 , 5)
composite_sigmas[8] = calc_sigma( 0 , 6)
composite_sigmas[9] = calc_sigma( 4 , 7)
composite_sigmas[10] = calc_sigma(1 , 8)
composite_sigmas[11] = calc_sigma(5 , 9)
composite_sigmas[12] = calc_sigma(2 , 10)
composite_sigmas[13] = calc_sigma(9 , 11)
composite_sigmas[14] = calc_sigma(6 , 12)
composite_sigmas[15] = calc_sigma(10, 13)
composite_sigmas[16] = calc_sigma(7 , 14)
composite_sigmas[17] = calc_sigma(11, 15)
composite_sigmas[18] = calc_sigma(8 , 16)

print("Composite sigma values: ", composite_sigmas)
