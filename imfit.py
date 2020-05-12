import math
import json 
import globals



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


data = []

CURRENT_STATE = None
LAST_STATE = None

STATES = {
    "UP": 'UP',
    "DOWN": 'DOWN'
}

COUNTER = 0

def have_strait_back(angles):
    Knee_Hip_Shoulder = None
    Ankle_Knee_Hip  = None
    
    keys = list(angles.keys())

    if 'Knee,Hip,Shoulder' in keys: 
        Knee_Hip_Shoulder = angles['Knee,Hip,Shoulder']
    else: Knee_Hip_Shoulder = None
    if 'Ankle,Knee,Hip' in keys: 
        Ankle_Knee_Hip = angles['Ankle,Knee,Hip']
    else: Ankle_Knee_Hip = None

    if (Knee_Hip_Shoulder and Ankle_Knee_Hip):
        return is_angle_in_range(Knee_Hip_Shoulder, 120, 180) and is_angle_in_range(Ankle_Knee_Hip, 140, 180)
    elif (Knee_Hip_Shoulder ):
        return is_angle_in_range(Knee_Hip_Shoulder, 120, 180)
    elif (Ankle_Knee_Hip ):
        return is_angle_in_range(Ankle_Knee_Hip, 140, 180)
    else: 
        return True



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


def starting_pose_correct(angles):
    Shoulder_Elbow_Wrist = None 
    Hip_Shoulder_Elbow = None
    Knee_Hip_Shoulder = None
    Ankle_Knee_Hip  = None
    
    keys = list(angles.keys())

    if 'Shoulder,Elbow,Wrist' in keys: 
        Shoulder_Elbow_Wrist = angles['Shoulder,Elbow,Wrist']
    if 'Hip,Shoulder,Elbow' in keys: 
        Hip_Shoulder_Elbow = angles['Hip,Shoulder,Elbow']
    if 'Knee,Hip,Shoulder' in keys: 
        Knee_Hip_Shoulder = angles['Knee,Hip,Shoulder']
    if 'Ankle,Knee,Hip' in keys: 
        Ankle_Knee_Hip = angles['Ankle,Knee,Hip']
    
    if not Shoulder_Elbow_Wrist and Hip_Shoulder_Elbow and Knee_Hip_Shoulder and Ankle_Knee_Hip:
        return False

    return (is_angle_in_range(Shoulder_Elbow_Wrist, 140, 180) and is_angle_in_range(Hip_Shoulder_Elbow, 45, 90) and is_angle_in_range(Knee_Hip_Shoulder, 140, 180) and is_angle_in_range(Ankle_Knee_Hip, 140, 180))


def check_angles(angles):
    Shoulder_Elbow_Wrist = None 
    Hip_Shoulder_Elbow = None
    Knee_Hip_Shoulder = None
    Ankle_Knee_Hip  = None
    
    keys = list(angles.keys())

    if 'Shoulder,Elbow,Wrist' in keys: 
        Shoulder_Elbow_Wrist = angles['Shoulder,Elbow,Wrist']
    if 'Hip,Shoulder,Elbow' in keys: 
        Hip_Shoulder_Elbow = angles['Hip,Shoulder,Elbow']
    if 'Knee,Hip,Shoulder' in keys: 
        Knee_Hip_Shoulder = angles['Knee,Hip,Shoulder']
    if 'Ankle,Knee,Hip' in keys: 
        Ankle_Knee_Hip = angles['Ankle,Knee,Hip']

    if not (Shoulder_Elbow_Wrist or Hip_Shoulder_Elbow): return False

    return True

def is_up(Shoulder_Elbow_Wrist, Hip_Shoulder_Elbow):

    if (Shoulder_Elbow_Wrist and Hip_Shoulder_Elbow):
        return is_angle_in_range(Shoulder_Elbow_Wrist, 140, 180) and is_angle_in_range(Hip_Shoulder_Elbow, 45, 90)

    if Shoulder_Elbow_Wrist:
        return is_angle_in_range(Shoulder_Elbow_Wrist, 140, 180)

    if Hip_Shoulder_Elbow:
        return is_angle_in_range(Hip_Shoulder_Elbow, 45, 90)
    
    return False



def is_down(Shoulder_Elbow_Wrist, Hip_Shoulder_Elbow):
    if (Shoulder_Elbow_Wrist and Hip_Shoulder_Elbow):
        return is_angle_in_range(Shoulder_Elbow_Wrist, 0, 140) and is_angle_in_range(Hip_Shoulder_Elbow, 0, 45)

    if Shoulder_Elbow_Wrist:
        return is_angle_in_range(Shoulder_Elbow_Wrist, 0, 140)

    if Hip_Shoulder_Elbow:
        return is_angle_in_range(Hip_Shoulder_Elbow, 0, 45)
    
    return False


def get_current_state(angles, current_state, last_state):
    Shoulder_Elbow_Wrist = None
    Hip_Shoulder_Elbow = None

    keys = list(angles.keys())
    if 'Shoulder,Elbow,Wrist' in keys: 
        Shoulder_Elbow_Wrist = angles['Shoulder,Elbow,Wrist']
    if 'Hip,Shoulder,Elbow' in keys: 
        Hip_Shoulder_Elbow = angles['Hip,Shoulder,Elbow']

    if is_up(Shoulder_Elbow_Wrist, Hip_Shoulder_Elbow):
        globals.show_msg['type'] = "success"
        globals.show_msg['content'] = "keep going, Everything is okay"
        return STATES['UP']
    elif is_down(Shoulder_Elbow_Wrist, Hip_Shoulder_Elbow):
        globals.show_msg['type'] = "success"
        globals.show_msg['content'] = "keep going, Everything is okay"
        return STATES['DOWN']
    globals.show_msg['type'] = "error"
    globals.show_msg['content'] = "Something is went wrong, Make sure your webcam cover your whole body"
    return last_state

def process_frame(frame):

    global CURRENT_STATE
    global LABLES
    global RIGHT_INDX
    global LEFT_INDX
    global ANGLES
    global LAST_STATE
    global STATES
    global COUNTER

    pose = frame['pose']
    pose = { k:v for k,v in pose.items() if v['score']>=0.3 }
    right_pose = { k:v for k,v in pose.items() if v['indx'] in RIGHT_INDX }
    left_pose = {k:v for k,v in pose.items() if v['indx'] in LEFT_INDX}

    woked_pose = {'dir': 'right', 'pose': right_pose} if len(right_pose) >= len(left_pose) else {'dir': 'left', 'pose': left_pose}
    angles = {}

    for key, angle in ANGLES[woked_pose['dir']].items():
        pose = woked_pose['pose']
        
        keys = list(pose.keys())
        if not (f'{angle[0]}' in keys and f'{angle[1]}' in keys and f'{angle[2]}' in keys): continue

        angles[key] = getAngle(pose[f'{angle[0]}']['point'], pose[f'{angle[1]}']['point'], pose[f'{angle[2]}']['point'])

    print(angles)
    print(globals.show_msg)

    if not check_angles(angles):
        print('Not Angles')
        globals.show_msg["type"] = "error"
        globals.show_msg['content'] = "SET your webcam correctly, many points are not detected"
        return COUNTER
    else:
        globals.show_msg['type'] = "success"
        globals.show_msg['content'] = "keep going, Everything is okay"

    # If no CURRENT_STATE do not start
    if not CURRENT_STATE: 
        if (starting_pose_correct(angles)):
            CURRENT_STATE = STATES['UP']
            globals.show_msg['type'] = "success"
            globals.show_msg['content'] = "keep going, Everything is okay"
        else:
            # Waiting user to be in frame with correct starting pose
            # show msg
            print('Not correct pose')
            globals.show_msg['type'] = "error"
            globals.show_msg['content'] = "Take starting position of push ups now"
            return COUNTER


    if LAST_STATE == STATES['DOWN'] and CURRENT_STATE == STATES['UP']:
        COUNTER += 1
    

    LAST_STATE = CURRENT_STATE

    CURRENT_STATE = get_current_state(angles, CURRENT_STATE, LAST_STATE)

    if(have_strait_back(angles)):
        globals.show_msg['type'] = "success"
        globals.show_msg['content'] = "keep going, Everything is okay"
    else:
        globals.show_msg['type'] = "error"
        globals.show_msg['content'] = "Dahrek Ya ANSA, Dahrk Ya OSAZ"



    print(CURRENT_STATE)
    print(COUNTER)
    return COUNTER

if __name__ == "__main__":
    
    with open('./test/framesposfortestvid.json', 'r') as f:
        data = json.load(f)

    for frame in data:
        process_frame(frame)





