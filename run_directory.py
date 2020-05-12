import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import math
FILE_PATH="./push1.jpg"
MODEL = "cmu"
RESIZE = '160x112'
RESIZE_OUT_RATIO = 4.0

LABLES = {
    'Nose': 0,
    'Neck': 1,
    'RShoulder': 2,
    'RElbow': 3,
    'RWrist': 4,
    'LShoulder': 5,
    'LElbow': 6,
    'LWrist': 7,
    'RHip': 8,
    'RKnee': 9,
    'RAnkle': 10,
    'LHip': 11,
    'LKnee': 12,
    'LAnkle': 13,
    'REye': 14,
    'LEye': 15,
    'REar': 16,
    'LEar': 17,
    'Background': 18,
}

RIGHT_INDX = [2,3,4,8,9,10]
LEFT_INDX = [5,6,7,11,12,13]

ANGLES = {
    'left': {
        'Shoulder,Elbow,Wrist':[5, 6, 7],
        'Hip,Shoulder,Elbow': [11,5,6],
        'Knee,Hip,Shoulder': [12,11,5],
        'Ankle,Knee,Hip':[13,12,11]
    },
    'right': {
        'Shoulder,Elbow,Wrist': [2,3,4],
        'Hip,Shoulder,Elbow': [8,2,3],
        'Knee,Hip,Shoulder': [9,8,2],
        'Ankle,Knee,Hip':[10,9,8]
    }
}
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    if ang<0:
        ang += 360
    if ang >180:
        ang = 360 - ang
    return ang 

def is_angle_in_range(angle, start, end):
    if not angle: return False
    return start <= angle <= end


def have_strait_back(Knee_Hip_Shoulder,Ankle_Knee_Hip):
    if is_angle_in_range(Knee_Hip_Shoulder, 120, 180) and is_angle_in_range(Ankle_Knee_Hip, 140, 180):
        return {"msg":"rigth position, keep going ",
            "type":"success"
        }
    elif is_angle_in_range(Knee_Hip_Shoulder, 120, 180):
        return {"msg":"Do not bend your knee and straighten it",
        "type":"error"}
    elif is_angle_in_range(Ankle_Knee_Hip, 140, 180):
        return  {"msg":"Put your torso in a single fit with your leg",
        "type":"error"}
    else:
        return  {"msg":"your position is wrong at all",
        "type":"error"}


def run(file_path):
    global RIGHT_INDX
    global LEFT_INDX
    global ANGLES
    global LABLES
    msg = {}
    image = cv2.imread(file_path)
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=RESIZE_OUT_RATIO)

    ll = {}
    for human in humans:
        for key, part in human.body_parts.items():
            ll[f'{part.part_idx}'] = {
                'indx': part.part_idx,
                'point': (part.x, part.y),
                'score': part.score
            }
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    pose = ll
    pose = { k:v for k,v in pose.items() if v['score']>=0.2 }
    right_pose = { k:v for k,v in pose.items() if v['indx'] in RIGHT_INDX }
    left_pose = {k:v for k,v in pose.items() if v['indx'] in LEFT_INDX}

    woked_pose = {'dir': 'right', 'pose': right_pose} if len(right_pose) >= len(left_pose) else {'dir': 'left', 'pose': left_pose}
    angles = {}

    for key, angle in ANGLES[woked_pose['dir']].items():
        pose = woked_pose['pose']
        
        keys = list(pose.keys())
        if not (f'{angle[0]}' in keys and f'{angle[1]}' in keys and f'{angle[2]}' in keys): continue

        angles[key] = getAngle(pose[f'{angle[0]}']['point'], pose[f'{angle[1]}']['point'], pose[f'{angle[2]}']['point'])
    keys = list(angles.keys())
    print(keys)
    if 'Knee,Hip,Shoulder' in keys and 'Ankle,Knee,Hip' in keys:
        print(angles['Knee,Hip,Shoulder'],angles['Ankle,Knee,Hip'])
        msg = have_strait_back(angles['Knee,Hip,Shoulder'],angles['Ankle,Knee,Hip'])
        msg["image"] = image
    else:
        msg = {"msg":"this image is not clear for our model \n update a good resolution jbg image from side view",
        "type":"error",
        "image":image}
    return msg
        

if __name__ == '__main__':

    w, h = model_wh('432x368')
    e = TfPoseEstimator(get_graph_path("cmu"), target_size=(w, h), trt_bool=False)
    print("______________________________________________")
    out = run(FILE_PATH)
    print(out)
    


