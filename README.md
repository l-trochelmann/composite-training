# Composite Dataset Training for Improved Pose Detection in the Wild

## About
This is the complementary Git Repository for the bachelor thesis Composite Dataset Training for Improved Pose Detection in the Wild by Leon Trochelmann.
The project was implemented as a fork of the MMPose toolkit for human pose detection.

For general information on this version of MMPose, please refer to: https://github.com/open-mmlab/mmpose/tree/0.x

To download the full evaluation results, please refer to: https://drive.google.com/drive/folders/1P4PMb_HLkrSuiyxAozG_RIbaw9L6bM0z

## Installation
To execute composite dataset training locally, please install MMPose: https://github.com/open-mmlab/mmpose/blob/0.x/docs/en/install.md, but clone this repository rather than the original.

## Training
This project presents a method to create composite datasets by defining a unified representation. This is implemented through a change to the annotations and the MMPose dataset configurations. This repository includes the tools needed to create a composite dataset from AIC, COCO and Crowdpose data. It also includes the required configs.
To train a model on such a composite dataset, execute two steps:
1. Convert your AIC, COCO and/or Crowdpose annotations to the composite style using the scripts in `composite_tools/`.
2. Train with one of the configs in `configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/composite` as you would any other MMPose config.
This will yield a model trained on the given composite dataset.

## Evaluation
To evaluate the composite-trained model, repeat the same steps as during training, but converting the validation annotations and evaluating with the same config.

If you wish to evaluate on specific keypoints and sigmas, you need to manipulate one of the dependencies:

In `(path-to-your-python)/python3.8/site-packages/xtcocotools/cocoeval.py`, in `computeOks`:
1. Manually supply sigmas for the desired keypoints, i.e. replace `sigmas = self.sigmas` with `np.asarray(sigmas = [0.026, 0.025, 0.025, 0.035, 0.035])`
2. Slice the ground truth and detected keypoints accordingly, i.e. replace `g = np.array(gt['keypoints'])` with `g = np.array(gt['keypoints'][3:18])` and do the same for the detections.

The given example evaluates COCO-style head keypoints with COCO head sigmas.

Please note that it is highly recommended to always work on the same unified representation, even if working with comparison models that don't predict certain keypoints. This allows the skipping of additional remapping steps.

## Defining Your Own
Please read and understand the following basic MMPose tutorials before creating new composites: https://github.com/open-mmlab/mmpose/blob/0.x/docs/en/tutorials/0_config.md, https://github.com/open-mmlab/mmpose/blob/0.x/docs/en/tutorials/2_new_dataset.md.

In order to define a new unified representation for new composite datasets, follow these steps:
1. Convert your annotations to your new representation, and to the general COCO dataset format.
2. Define a new `composite.py` file in `configs/_base_/` matching your representation.
3. Create a new config in `configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/composite` or alter an existing one.
4. In `_base_`: use `composite.py`
5. In `channel_cfg`: match the number of channels to your representation
6. In `data_cfg`: Set `use_gt_bbox=True`
7. In `data`: Set the used dicts to match your new composite. Each dict represent one dataset. When the `train` field receives a list of dicts, it then concatenates them to a composite dataset.

## Acknowledgement
This project may have not been possible without the efforts of the MMPose ccontributors.
The author extends his gratitude.

## License

This project is released under the [Apache 2.0 license](LICENSE).
