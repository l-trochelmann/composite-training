"""
This script samples a mini dataset from Crowdpose and mutates its annotations.
The original keypoint representaiton is replaced with a unified representation including all AIC and COCO keypoints. 
The resulting annotations can then be used for training together with others sharing the same representation.
It operates on one json file at a time, and thus needs to be executed separately for train and val data.
The size of the mini dataset can be set via SAMPLES_PER_DATASET.
If SAMPLES_PER_DATASET exceeds actual dataset size, sampling does not occur.
"""

import json, random

PATH_TO_CROWDPOSE_ANNOTATIONS = "./data/crowdpose/annotations/mmpose_crowdpose_test.json"
PATH_TO_COMPOSITE_OUTPUT = "./data/composite/annotations/crowdpose_composite_val.json"
SAMPLES_PER_DATASET = 50000


# Data preparation
# Read data
print("Loading JSON data...")
with open(PATH_TO_CROWDPOSE_ANNOTATIONS, "r") as crowdpose_json:
    crowdpose_original = json.load(crowdpose_json)


# Filter out useless zero-keypoint annotations
print ("Removing zero-keypoint annotations from COCO...")
zeroes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
crowdpose_original["annotations"] = [annotation for annotation in crowdpose_original["annotations"] if annotation["keypoints"] != zeroes]


# Sample data
crowdpose_composite = crowdpose_original
if len(crowdpose_composite["annotations"]) > SAMPLES_PER_DATASET:
    print("Sampling " + str(SAMPLES_PER_DATASET) + " person annotations from Crowdpose's total of " + str(len(crowdpose_composite["annotations"])) + "...")
    random.seed(0)
    crowdpose_composite["annotations"] = random.sample(crowdpose_original["annotations"], SAMPLES_PER_DATASET)
else:
    print("Not sampling from "+ str(len(crowdpose_composite["annotations"])) + " Crowdpose person annotations...")


# Filter out the image details of unreferenced images
# This saves storage space but may take a few minutes
print("Filtering out unreferenced image details...")
referenced_image_ids = []
for annotation in crowdpose_composite["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in crowdpose_composite["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
crowdpose_composite["images"] = referenced_images


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
crowdpose_composite["categories"] = composite_categories


# Change annotations to match unified representation
print("Unifying representation")
for annotation in crowdpose_composite["annotations"]:
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


print("Saving results to JSON...")
# Step 4: Save new mini datasets to storage
with open(PATH_TO_COMPOSITE_OUTPUT, "w") as crowdpose_composite_json:
    json.dump(crowdpose_composite, crowdpose_composite_json)
