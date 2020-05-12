import argparse
import logging
import time
import json
import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import math

from imfit import process_frame

from design import *
import globals

class poseThread(QThread):
    changePixmap = pyqtSignal(QImage)
    
    def run(self):
        CAMERA = 0
        MODEL = "cmu"
        RESIZE = "160x112"
        RESIZE_OUT_RATIO = 4.0
        w, h = model_wh(RESIZE)
        e = TfPoseEstimator(get_graph_path(MODEL), target_size=(w, h), trt_bool=False)
        cam = cv2.VideoCapture(CAMERA)
        fps_time = 0
        frame_count = 0;
        print(globals.quitcapPose)
        while True:
            ret_val, image = cam.read()

            if not ret_val:
                continue
            
            humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=RESIZE_OUT_RATIO)
            frame_count += 1
            ll = {}
            for human in humans:
                for key, part in human.body_parts.items():
                    ll[f'{part.part_idx}'] = {
                        'indx': part.part_idx,
                        'point': (part.x, part.y),
                        'score': part.score
                    }
            frame = {
                'frame': frame_count,
                'pose': ll
            }
            globals.posecounter = process_frame(frame)
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            cv2.putText(image,
                        f"FPS: {(1.0 / (time.time() - fps_time))} | counter {globals.posecounter}",
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            cv2.imshow('tf-pose-estimation result', image)
            fps_time = time.time()
            # if cv2.waitKey(1) == 27:
            #     break
        cam.release()
        #cv2.destroyAllWindows()
    
    def quit(self):
        globals.quitcapPose=True 