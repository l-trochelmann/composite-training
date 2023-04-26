"""
This script samples a mini dataset from MPII-TRB and mutates its annotations.
The original keypoint representaiton is replaced with a unified representation including all AIC and COCO keypoints. 
The resulting annotations can then be used for training together with others sharing the same representation.
It operates on one json file at a time, and thus needs to be executed separately for train and val data.
The size of the mini dataset can be set via SAMPLES_PER_DATASET.
If SAMPLES_PER_DATASET exceeds actual dataset size, sampling does not occur.
"""

import json, random

PATH_TO_MPII_ANNOTATIONS = "./data/mpii-trb/annotations/mpii_trb_train.json"
PATH_TO_COMPOSITE_OUTPUT = "./data/composite/annotations/mpii-trb_composite_train.json"
SAMPLES_PER_DATASET = 50000


# Data preparation
# Read data
print("Loading JSON data...")
with open(PATH_TO_MPII_ANNOTATIONS, "r") as mpii_json:
    mpii_original = json.load(mpii_json)


# Sample data
mpii_composite = mpii_original
if len(mpii_composite["annotations"]) > SAMPLES_PER_DATASET:
    print("Sampling " + str(SAMPLES_PER_DATASET) + " person annotations from MPII-TRB's total of " + str(len(mpii_composite["annotations"])) + "...")
    random.seed(0)
    mpii_composite["annotations"] = random.sample(mpii_original["annotations"], SAMPLES_PER_DATASET)
else:
    print("Not sampling from "+ str(len(mpii_composite["annotations"])) + " MPII-TRB person annotations...")


# Filter out the image details of unreferenced images
# This saves storage space but may take a few minutes
print("Filtering out unreferenced image details...")
referenced_image_ids = []
for annotation in mpii_composite["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in mpii_composite["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
mpii_composite["images"] = referenced_images


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
mpii_composite["categories"] = composite_categories


# Change annotations to match unified representation
print("Unifying annotations")
for annotation in mpii_composite["annotations"]:
    old_kpts = annotation["keypoints"]
    unified_kpts = old_kpts[36:39]      \
                + [0,0,0]               \
                + [0,0,0]               \
                + [0,0,0]               \
                + [0,0,0]               \
                + [0,0,0]               \
                + old_kpts[39:42]       \
                + old_kpts[0:3]         \
                + old_kpts[3:6]         \
                + old_kpts[6:9]         \
                + old_kpts[9:12]        \
                + old_kpts[12:15]       \
                + old_kpts[15:18]       \
                + old_kpts[18:21]       \
                + old_kpts[21:24]       \
                + old_kpts[24:27]       \
                + old_kpts[27:30]       \
                + old_kpts[30:33]       \
                + old_kpts[33:36]
    annotation["keypoints"] = unified_kpts
"""
with
    [0-1-2"left_shoulder",3-4-5"right_shoulder",6-7-8"left_elbow",9-10-11"right_elbow",12-13-14"left_wrist",15-16-17"right_wrist",18-19-20"left_hip",
    21-22-23"right_hip",24-25-26"left_knee",27-28-29"right_knee",30-31-32"left_ankle",33-34-35"right_ankle",36-37-38"head",39-40-41"neck"]
"""


# Rename the "num_joints" field to "num_keypoints" and recalculate its value
for annotation in mpii_composite["annotations"]:
    annotation["num_keypoints"] = annotation["keypoints"][2::3].count(2.0)
    del annotation["num_joints"]


print("Saving results to JSON...")
# Step 4: Save new mini datasets to storage
with open(PATH_TO_COMPOSITE_OUTPUT, "w") as mpii_composite_json:
    json.dump(mpii_composite, mpii_composite_json)
