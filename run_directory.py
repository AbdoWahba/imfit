import argparse
import time
import glob
import ast
import os
import dill

import common
import cv2
import numpy as np
from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh

from lifting.prob_model import Prob3dPose
from lifting.draw import plot_pose

FILE_PATH=""


if __name__ == '__main__':
    scales = ast.literal_eval(None)

    w, h = model_wh('432x368')
    e = TfPoseEstimator(get_graph_path("cmu"), target_size=(w, h))

        image = imread(FILE_PATH)

        humans = e.inference(image, scales=scales)


        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv2.imshow('tf-pose-estimation result', image)
        cv2.waitKey(5)

