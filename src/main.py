import datetime
import os

import cv2
import imutils

from core.crop import Crop

# TO DO
# test the pad - OK
# crop images, save each group in a folder - OK

if __name__ == "__main__":
    Crop.delete_imgs()

    file_name = "race.mp4"

    cap = cv2.VideoCapture(os.path.join("videos",file_name))

    splited_name = file_name.split(".")
    file_name = splited_name[0]+"-"+splited_name[1]

    crop = Crop(file_name=file_name,
                video=cap,
                resize={"bool":True, "width": 700})

    time_to_start = crop.set_start_video()
    time_to_end = crop.set_end_video()
    pad = crop.add_pad()

    crop.update_time_video(time_to_start)
    bboxes, frame = crop.select_bboxes()
    multiTracker = crop.init_tracker(bboxes=bboxes, frame=frame)

    names_of_frames = {}
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

            print(f"\n-> Current time in video: {datetime.timedelta(seconds=crop.get_current_time()/1000)}")
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
                crop.n_of_slices += 1                
                multiTracker = crop.init_tracker(bboxes=bboxes, frame=frame)
                names_of_frames.clear()
            else: 
                break
      
        success, boxes = multiTracker.update(frame)

        for i, newbox in enumerate(boxes):
            x, y, w, h = newbox
            x, y, w, h = int(x), int(y), int(w), int(h)
            p1 = (x, y)
            p2 = (x + w, y + h)
            p1_pad = (p1[0] - pad, p1[1] - pad)
            p2_pad = (p2[0] + pad, p2[1] + pad)
        
            ROI = frame[y-pad:y+h+pad, x-pad:x+w+pad]
            crop.create_img_folder()         

            if not names_of_frames.get(i):
                names_of_frames[i] = 1

            crop.crop_img(ROI, i, names_of_frames)
            names_of_frames[i] += 1
            
            cv2.rectangle(frame, p1_pad, p2_pad, crop.colors[i], 2)

        cv2.imshow('IC - D&D', frame)
        
        # close
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break

    crop.video.release()
    cap.release()
    cv2.destroyAllWindows()
