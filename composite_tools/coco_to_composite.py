"""
This script samples a mini dataset from COCO and mutates its annotations.
The original keypoint representaiton is replaced with a unified representation including all AIC and COCO keypoints. 
The resulting annotations can then be used for training together with others sharing the same representation.
It operates on one json file at a time, and thus needs to be executed separately for train and val data.
The size of the mini dataset can be set via SAMPLES_PER_DATASET.
If SAMPLES_PER_DATASET exceeds actual dataset size, sampling does not occur.
"""

import json, random

PATH_TO_COCO_ANNOTATIONS = "./data/coco/annotations/person_keypoints_val2017.json"
PATH_TO_COMPOSITE_OUTPUT = "./data/composite/annotations/coco_composite_val.json"
SAMPLES_PER_DATASET = 50000


# Data preparation
# Read data
print("Loading JSON data...")
with open(PATH_TO_COCO_ANNOTATIONS, "r") as coco_json:
    coco_original = json.load(coco_json)


# Filter out useless zero-keypoint annotations
print ("Removing zero-keypoint annotations from COCO...")
zeroes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
coco_original["annotations"] = [annotation for annotation in coco_original["annotations"] if annotation["keypoints"] != zeroes]


# Delete unused segmentation info
print("Deleting unused segmentation info from COCO annotations...")
for annotation in coco_original["annotations"]:
    del annotation["segmentation"]


# Sample data
coco_composite = coco_original
if len(coco_composite["annotations"]) > SAMPLES_PER_DATASET:
    print("Sampling " + str(SAMPLES_PER_DATASET) + " person annotations from COCO's total of " + str(len(coco_composite["annotations"])) + "...")
    random.seed(0)
    coco_composite["annotations"] = random.sample(coco_original["annotations"], SAMPLES_PER_DATASET)
else:
    print("Not sampling from "+ str(len(coco_composite["annotations"])) + " COCO person annotations...")


# Filter out the image details of unreferenced images
# This saves storage space but may take a few minutes
print("Filtering out unreferenced image details...")
referenced_image_ids = []
for annotation in coco_composite["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in coco_composite["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
coco_composite["images"] = referenced_images


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
coco_composite["categories"] = composite_categories


# Change annotations to match unified representation
print("Unifying annotations")
for annotation in coco_composite["annotations"]:
    old_kpts = annotation["keypoints"]
    unified_kpts = [0,0,0] \
                 + old_kpts[3:6] \
                 + old_kpts[6:9] \
                 + old_kpts[9:12] \
                 + old_kpts[12:15] \
                 + old_kpts[0:3] \
                 + [0,0,0] \
                 + old_kpts[15:18] \
                 + old_kpts[18:21] \
                 + old_kpts[21:24] \
                 + old_kpts[24:27] \
                 + old_kpts[27:30] \
                 + old_kpts[30:33] \
                 + old_kpts[33:36] \
                 + old_kpts[36:39] \
                 + old_kpts[39:42] \
                 + old_kpts[42:45] \
                 + old_kpts[45:48] \
                 + old_kpts[48:51]
    annotation["keypoints"] = unified_kpts
"""
with
    [0-1-2"nose",3-4-5"left_eye",6-7-8"right_eye",9-10-11"left_ear",12-13-14"right_ear",15-16-17"left_shoulder",18-19-20"right_shoulder",
    21-22-23"left_elbow",24-25-26"right_elbow",27-28-29"left_wrist",30-31-32"right_wrist",33-34-35"left_hip",36-37-38"right_hip",39-40-41"left_knee",
    42-43-44"right_knee",45-46-47"left_ankle",48-49-50"right_ankle"]
"""


print("Saving results to JSON...")
# Step 4: Save new mini datasets to storage
with open(PATH_TO_COMPOSITE_OUTPUT, "w") as coco_composite_json:
    json.dump(coco_composite, coco_composite_json)
