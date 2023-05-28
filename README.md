# Composite Dataset Training for Improved Pose Detection in the Wild

## About
This project was implemented as a fork of the MMPose toolkit for human pose detection.
For general information on this version of MMPose and how to use it, please refer to `https://github.com/open-mmlab/mmpose/tree/0.x`

## Abstract
Human Pose Detection is a fundamental computer vision task that allows com-
puters to detect a human being in a much more sophisticated way than a simple
bounding box. The field has seen great strides in recent years with models becom-
ing increasingly sophisticated and reaching better and better scores on common
benchmarks. The underlying goal is to obtain more precise and robust detection of
in-the-wild data: Data reflecting real-world use cases which is free from potential
biases that the popular datasets may be subject to. To minimise such biases and
improve performance on in-the-wild data, we present composite dataset training:
A method to reconcile differences between datasets so that a model can be trained
on all of their data. The performance of such models is evaluated on various val-
idation sets and compared to that of models trained on individual datasets. A
comparative analysis is also conducted between models trained on a composite
dataset and models trained on individual datasets of equal size. This analysis aims
to explore the impact of dataset-external variety versus dataset-internal variety.
The results show that a model trained on a composite dataset always outper-
forms models trained on the individual parts. Furthermore, the composite-trained
models outperform models trained on individual datasets of the same size during
validation on external data, demonstrating that external variety can lead to better
generalisation than internal variety.
