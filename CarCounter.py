from ultralytics import YOLO
import cv2
import cvzone
import math
import torch
from sort import *

def car(path = "E:/Object_Counter/Videos/cars.mp4",li = [400, 297, 673, 297],obj='Car'):
    # Check if CUDA (GPU) is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    '''
    #for WebCam
    cap = cv2.VideoCapture(0)
    cap.set(3,1280) #Width
    cap.set(4,720) #Height
    '''
    cap = cv2.VideoCapture(path)#"Videos/cars.mp4"

    model = YOLO('Yolo-Weights/yolov8l.pt')

    #Detected class
    if obj == 'Car':
        detected = ['car','motorbike','bus','truck']
    else:
        detected = ['person']

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

    #mask = cv2.imread('Region.png')
    #tracking
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

    limits = li
    totalCount = []

    #Cam Loop
    while True:
        success , img = cap.read()

        results = model(img,stream=True)

        detections = np.empty((0,5))

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

                currentClass = classNames[cls]
                if currentClass in detected and conf>0.3:
                    #cvzone.putTextRect(img,f'{currentClass} {conf}',(max(0,x1),max(35,y1)),scale=1,thickness=1,offset=3)
                    #cvzone.cornerRect(img,(x1,y1,w,h),l=9)
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currentArray))

            resultsTracker = tracker.update(detections)
            cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)

            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(result)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                cvzone.putTextRect(img, f' {int(id)}', (max(0, x1), max(35, y1)),
                                scale=2, thickness=3, offset=10)
        
                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        
                if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
                    if totalCount.count(id) == 0:
                        totalCount.append(id)
                        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

            cv2.putText(img,str(len(totalCount)),(255,100),cv2.FONT_HERSHEY_PLAIN,5,(50,50,255),8)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break