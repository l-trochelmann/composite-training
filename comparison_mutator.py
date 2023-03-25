"""
The task of this script is to sample mini datasets from the coco and aic datasets.
"""

import json, random

PATH_TO_COCO_ANNOTATIONS = "./data/coco/annotations/person_keypoints_val2017.json"
PATH_TO_AIC_ANNOTATIONS = "./data/aic/annotations/aic_val.json"
PATH_TO_COCO_OUT_ANNOTATIONS = "./data/composite/annotations/coco_comparison_val.json"
PATH_TO_AIC_OUT_ANNOTATIONS = "./data/composite/annotations/aic_comparison_val.json"
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
coco_comparison = coco_original
if len(coco_comparison["annotations"]) > SAMPLES_PER_DATASET:
    random.seed(0)  # ensure the same annotations are sampled for comparison datasets
    coco_comparison["annotations"] = random.sample(coco_comparison["annotations"], SAMPLES_PER_DATASET)
aic_comparison = aic_original
if len(aic_comparison["annotations"]) > SAMPLES_PER_DATASET:
    random.seed(0)
    aic_comparison["annotations"] = random.sample(aic_original["annotations"], SAMPLES_PER_DATASET)

print("Original data sampled")


# Step 1.4: Filter out image details of unreferenced images
referenced_image_ids = []
for annotation in coco_comparison["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in coco_comparison["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
coco_comparison["images"] = referenced_images

referenced_image_ids = []
for annotation in aic_comparison["annotations"]:
    if annotation["image_id"] not in referenced_image_ids:
        referenced_image_ids.append(annotation["image_id"])
referenced_images = []
for image_detail in aic_comparison["images"]:
    if image_detail["id"] in referenced_image_ids:
        referenced_images.append(image_detail)
aic_comparison["images"] = referenced_images

print("Image details filtered")


# Bonus step: Delete unused segmentation info
for annotation in coco_comparison["annotations"]:
    del annotation["segmentation"]


# Step 2: Save new mini datasets to storage
with open(PATH_TO_COCO_OUT_ANNOTATIONS, "w") as coco_comparison_json:
    json.dump(coco_comparison, coco_comparison_json)
with open(PATH_TO_AIC_OUT_ANNOTATIONS, "w") as aic_comparison_json:
    json.dump(aic_comparison, aic_comparison_json)

print("Results saved to JSON data")
