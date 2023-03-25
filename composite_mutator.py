"""
The task of this script is to sample mini datasets from the coco and aic datasets and mutate the representation of their 
annotations to a unified representation, so that they can be used for composite dataset training.
"""

import json, random

PATH_TO_COCO_ANNOTATIONS = "./data/coco/annotations/person_keypoints_val2017.json"
PATH_TO_AIC_ANNOTATIONS = "./data/aic/annotations/aic_val.json"
PATH_TO_COCO_OUT_ANNOTATIONS = "./data/composite/annotations/coco_composite_val.json"
PATH_TO_AIC_OUT_ANNOTATIONS = "./data/composite/annotations/aic_composite_val.json"
SAMPLES_PER_DATASET = 50000

print("Mutator script started")


# Step 1: Data preparation
# Step 1.1: Read data
with open(PATH_TO_COCO_ANNOTATIONS, "r") as coco_json:
    coco_original = json.load(coco_json)
with open(PATH_TO_AIC_ANNOTATIONS, "r") as aic_json:
    aic_original = json.load(aic_json)

print("Json data loaded")


# Step 1.2: Filter out useless coco annotations
coco_zeroes = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
coco_original["annotations"] = [annotation for annotation in coco_original["annotations"] if annotation["keypoints"] != coco_zeroes]

print ("Coco's zero keypoint labels removed")


# Step 1.3: Sample data
coco_composite = coco_original
if len(coco_composite["annotations"]) > SAMPLES_PER_DATASET:
    random.seed(0)  # ensure the same annotations are sampled for comparison datasets
    coco_composite["annotations"] = random.sample(coco_composite["annotations"], SAMPLES_PER_DATASET)
aic_composite = aic_original
if len(aic_composite["annotations"]) > SAMPLES_PER_DATASET:
    random.seed(0)
    aic_composite["annotations"] = random.sample(aic_original["annotations"], SAMPLES_PER_DATASET)

print("Original data sampled")


# Step 1.4: Filter out image details of unreferenced images
referenced_image_ids = []
for annotation in coco_composite["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in coco_composite["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
coco_composite["images"] = referenced_images

referenced_image_ids = []
for annotation in aic_composite["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in aic_composite["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
aic_composite["images"] = referenced_images

print("Image details filtered")


# Bonus step: Delete unused segmentation info
for annotation in coco_composite["annotations"]:
    del annotation["segmentation"]

# Step 2: Overwrite categories with unified representation
# todo if necessary: adjust info, licenses
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
aic_composite["categories"] = composite_categories

print("Categories overwritten")


# Step 3: Rearrange and expand annotations to match unified representation
for annotation in coco_composite["annotations"]:
    annotation["keypoints"] = [0,0,0] + annotation["keypoints"][3:15] + annotation["keypoints"][0:3] \
                              + [0,0,0] + annotation["keypoints"][15:51]
"""
Long notation:
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
with                 
    [0-1-2"nose",3-4-5"left_eye",6-7-8"right_eye",9-10-11"left_ear",12-13-14"right_ear",15-16-17"left_shoulder",18-19-20"right_shoulder",
    21-22-23"left_elbow",24-25-26"right_elbow",27-28-29"left_wrist",30-31-32"right_wrist",33-34-35"left_hip",36-37-38"right_hip",39-40-41"left_knee",
    42-43-44"right_knee",45-46-47"left_ankle",48-49-50"right_ankle"]
"""

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

print("Annotations unified")


# Step 4: Save new mini datasets to storage
with open(PATH_TO_COCO_OUT_ANNOTATIONS, "w") as coco_composite_json:
    json.dump(coco_composite, coco_composite_json)
with open(PATH_TO_AIC_OUT_ANNOTATIONS, "w") as aic_composite_json:
    json.dump(aic_composite, aic_composite_json)

print("Results saved to JSON data")
