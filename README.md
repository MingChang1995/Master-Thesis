# Master-Thesis
The installation and use of detectron2 is identical to what is available on facebook open source. Here we are structurally redesigning the object detection model inside detectron2, mainly in the loss function section, as follows.

In detectron2/detectron2/modeling/meta_arch/retinanet.py we have added a new loss function pipeline to calculate the overlap (in the form of iou) between the bounding boxes of the model output.

In detectron2/detectron2/modeling/roi_heads/fast_rcnn.py, we have added a section for Eql v2 and changed the model structure, added a section for predicting variance to the section for predicting bounding boxes, and made changes to the loss function, this section is to add Softer-NMS.

In detectron2/detectron2/layers/nms.py we added the algorithms for Soft-NMS and Softer-NMS.

Three copy-and-paste methods are stored in Data_Aug, as described in detail in the master thesis. Split.py serves to separate the images in the training set from the .xml files that hold the annotation information.
