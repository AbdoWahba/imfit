def init ():
    global recording
    global pushupsCount
    global inpushup
    global squatscount
    global insquats
    global x
    global y
    global xall
    global yall
    global testnet
    global t
    global lasttime
    global quitcap
    



    # OpenPose
    global show_msg
    global quitcapPose
    global poseState
    global posecounter




    x=[]
    y=[]
    xall=[]
    xall2=[]
    yall=[]
    testnet=[]
    t=0
    lasttime=0

    recording=False
    inpushup=False
    insquats=False
    pushupsCount=0
    squatscount=0

    quitcap=False

    # OpenPose
    quitcapPose=False
    poseState=''
    posecounter=0
    show_msg = {
    "type": "",
    "content": ""
}
