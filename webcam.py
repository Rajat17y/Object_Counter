from ultralytics import YOLO
import cv2
import cvzone
import math
import torch

# Check if CUDA (GPU) is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

'''
#for WebCam
cap = cv2.VideoCapture(0)
cap.set(3,1280) #Width
cap.set(4,720) #Height
'''
cap = cv2.VideoCapture("Videos/motorbikes-1.mp4")

model = YOLO('Yolo-Weights/yolov8l.pt')

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

#Cam Loop
while True:
    success , img = cap.read()
    results = model(img,stream=True)

    #For Boxes
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
            w,h = x2-x1,y2-y1
            #print(x1,y1,x2,y2)

            #For CV2
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            #Confidence
            conf = math.ceil(box.conf[0]*100)/100

            cls = int(box.cls[0])
            cvzone.cornerRect(img,(x1,y1,w,h))
            cvzone.putTextRect(img,f'{classNames[cls]} {conf}',(max(0,x1),max(35,y1)),scale=1.5,thickness=2)

    cv2.imshow("Image",img)
    cv2.waitKey(1)