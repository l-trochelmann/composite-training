"""
This script samples a mini dataset from AIC and mutates its annotations.
The original keypoint representaiton is replaced with a unified representation including all AIC and COCO keypoints. 
The resulting annotations can then be used for training together with others sharing the same representation.
It operates on one json file at a time, and thus needs to be executed separately for train and val data.
The size of the mini dataset can be set via SAMPLES_PER_DATASET.
If SAMPLES_PER_DATASET exceeds actual dataset size, sampling does not occur.
"""

import json, random

PATH_TO_AIC_ANNOTATIONS = "./data/aic/annotations/aic_train.json"
PATH_TO_COMPOSITE_OUTPUT = "./data/composite/annotations/aic_composite_train.json"
SAMPLES_PER_DATASET = 50000


# Data preparation
# Read data
print("Loading JSON data...")
with open(PATH_TO_AIC_ANNOTATIONS, "r") as aic_json:
    aic_original = json.load(aic_json)


# Sample data
aic_composite = aic_original
if len(aic_composite["annotations"]) > SAMPLES_PER_DATASET:
    print("Sampling " + str(SAMPLES_PER_DATASET) + " person annotations from AIC's total of " + str(len(aic_composite["annotations"])) + "...")
    random.seed(0)
    aic_composite["annotations"] = random.sample(aic_original["annotations"], SAMPLES_PER_DATASET)
else:
    print("Not sampling from "+ str(len(aic_composite["annotations"])) + " AIC person annotations...")


# Filter out the image details of unreferenced images
# This saves storage space but may take a few minutes
print("Filtering out unreferenced image details...")
referenced_image_ids = []
for annotation in aic_composite["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in aic_composite["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
aic_composite["images"] = referenced_images


# Overwrite categories
print("Overwriting categories...")
composite_categories = [{
    "supercategory": "person",
    "id": 1,
    "name": "person",
    "keypoints": ["head_top", "left_eye", "right_eye", "left_ear", "right_ear", "nose", "neck", 
                  "left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", 
                  "right_wrist", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", 
                  "right_ankle"],
    "skeleton":  [[12,10], [10,8], [7,9], [9,11], [18,16], [16,14], [14,13], [13,15], [15,17], [8,14], [7,13],
                 [8,6], [6,7], [0,6], [1,2], [5,1], [5,2], [1,3], [2,4], [3,7], [4,8], [7,8]]
}]
aic_composite["categories"] = composite_categories


# Change annotations to match unified representation
print("Unifying representation")
for annotation in aic_composite["annotations"]:
    old_kpts = annotation["keypoints"]
    unified_kpts = old_kpts[36:39] \
                 + [0,0,0] \
                 + [0,0,0] \
                 + [0,0,0] \
                 + [0,0,0] \
                 + [0,0,0] \
                 + old_kpts[39:42] \
                 + old_kpts[9:12] \
                 + old_kpts[0:3] \
                 + old_kpts[12:15] \
                 + old_kpts[3:6] \
                 + old_kpts[15:18] \
                 + old_kpts[6:9] \
                 + old_kpts[27:30] \
                 + old_kpts[18:21] \
                 + old_kpts[30:33] \
                 + old_kpts[21:24] \
                 + old_kpts[33:36] \
                 + old_kpts[24:27]
    annotation["keypoints"] = unified_kpts
"""
with
    [0-1-2"Right Shoulder",3-4-5"Right Elbow",6-7-8"Right Wrist",9-10-11"Left Shoulder",12-13-14"Left Elbow",15-16-17"Left Wrist",18-19-20"Right Hip",
    21-22-23"Right Knee",24-25-26"Right Ankle",27-28-29"Left Hip",30-31-32"Left Knee",33-34-35"Left Ankle",36-37-38"Head top",39-40-41"Neck"],
"""


print("Saving results to JSON...")
# Step 4: Save new mini datasets to storage
with open(PATH_TO_COMPOSITE_OUTPUT, "w") as aic_composite_json:
    json.dump(aic_composite, aic_composite_json)
