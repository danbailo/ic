import cv2
from core.crop import Crop
import imutils

if __name__ == "__main__":

    cap = cv2.VideoCapture("videos/race.mp4")

    crop = Crop(cap, resize={"bool":True, "width": 700})

    time_to_start = crop.set_start_video()
    time_to_end = crop.set_end_video()
    pad = crop.add_pad()

    crop.update_time_video(time_to_start)
   
    bboxes, init_frame = crop.select_bboxes()

    # Create MultiTracker object
    multiTracker = cv2.MultiTracker_create()

    # Initialize MultiTracker 
    for bbox in bboxes:
        multiTracker.add(cv2.TrackerCSRT_create(), init_frame, bbox)

    while cap.isOpened():
        retval, frame = cap.read()
        if not retval:
            break		
        
        #resize the frame
        if crop.resize["bool"]:
            frame = imutils.resize(frame, width=crop.resize["width"])

        success, boxes = multiTracker.update(frame)

        for i, newbox in enumerate(boxes):
            x, y, w, h = newbox
            p1 = (int(x), int(y))
            p2 = (int(x + w), int(y + h))
            cv2.rectangle(frame, p1, p2, crop.colors[i], 2)

        # show frame        
        cv2.imshow('MultiTracker', frame)
        
        # quit on ESC button or q button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break