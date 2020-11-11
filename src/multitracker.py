import cv2
from core.crop import Crop
import imutils

def init_tracker(bboxes, frame):
    # Create MultiTracker object
    multiTracker = cv2.MultiTracker_create()

    # Initialize MultiTracker 
    for bbox in bboxes:
        multiTracker.add(cv2.TrackerCSRT_create(), frame, bbox)

    return multiTracker

if __name__ == "__main__":

    cap = cv2.VideoCapture("videos/race.mp4")

    crop = Crop(cap, resize={"bool":True, "width": 700})

    time_to_start = crop.set_start_video()
    time_to_end = crop.set_end_video()
    pad = crop.add_pad()

    crop.update_time_video(time_to_start)
   
    bboxes, frame = crop.select_bboxes()

    multiTracker = init_tracker(bboxes=bboxes, frame=frame)

    while True:

        retval, frame = crop.video.read()

        # end of video
        if not retval:
            break

        #resize the frame
        if crop.resize["bool"]:
            frame = imutils.resize(frame, width=crop.resize["width"])        

        if crop.get_current_time() >= time_to_end:
            cv2.destroyAllWindows()

            if crop.extract_more():
              
                while True:
                    time_to_start = crop.set_start_video()
                    if time_to_start > crop.get_current_time():
                        break

                crop.update_time_video(time_to_start)
                
                while True:
                    time_to_end = crop.set_end_video()
                    if time_to_end > time_to_start:
                        break
                pad = crop.add_pad()

                bboxes, frame = crop.select_bboxes()
                multiTracker = init_tracker(bboxes=bboxes, frame=frame)

            else: 
                break
      
        success, boxes = multiTracker.update(frame)

        for i, newbox in enumerate(boxes):
            x, y, w, h = newbox
            p1 = (int(x), int(y))
            p2 = (int(x + w), int(y + h))
            cv2.rectangle(frame, p1, p2, crop.colors[i], 2)

        # show frame        
        cv2.imshow('IC - D&D', frame)
        
        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break