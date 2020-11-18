import datetime
import os

import cv2
import imutils

from core.crop import Crop

# TO DO
# a crop can take another tracker's box if they're close - ok, better way


if __name__ == "__main__":
    Crop.delete_imgs()

    file_name = "race.mp4"

    cap = cv2.VideoCapture(os.path.join("videos",file_name))
    # crop_cap = cv2.VideoCapture(os.path.join("videos",file_name))

    splited_name = file_name.split(".")
    file_name = splited_name[0]+"-"+splited_name[1]

    crop = Crop(file_name=file_name,
                resize={"bool":True, "width": 700})

    time_to_start = crop.set_start_video()
    time_to_end = crop.set_end_video()
    pad = crop.add_pad()

    crop.update_time_video(cap, time_to_start)
    bboxes, draw_frame = crop.select_bboxes(cap)
    multiTracker = crop.init_tracker(bboxes=bboxes, frame=draw_frame)

    names_of_frames = {}
    while True:

        retval, draw_frame = cap.read()

        # end of video
        if not retval:
            break

        #resize the frame
        if crop.resize["bool"]:
            draw_frame = imutils.resize(draw_frame, width=crop.resize["width"])

        crop_frame = draw_frame.copy()

        if crop.get_current_time(cap) >= time_to_end:
            cv2.destroyAllWindows()

            print(f"\n-> Current time in video: {datetime.timedelta(seconds=crop.get_current_time(cap)/1000)}")
            if crop.extract_more():              
                while True:
                    time_to_start = crop.set_start_video()
                    if time_to_start > crop.get_current_time(cap):
                        break
                
                cap = crop.update_time_video(cap, time_to_start)
                
                while True:
                    time_to_end = crop.set_end_video()
                    if time_to_end > time_to_start:
                        break
                pad = crop.add_pad()
                bboxes, draw_frame = crop.select_bboxes(cap)                
                crop.n_of_slices += 1                
                multiTracker = crop.init_tracker(bboxes=bboxes, frame=draw_frame)
                names_of_frames.clear()
            else: 
                break
      
        success, boxes = multiTracker.update(draw_frame)

        for i, newbox in enumerate(boxes):
            x, y, w, h = newbox
            x, y, w, h = int(x), int(y), int(w), int(h)
            p1 = (x, y)
            p2 = (x + w, y + h)
            p1_pad = (p1[0] - pad, p1[1] - pad)
            p2_pad = (p2[0] + pad, p2[1] + pad)

            # crop_frame = draw_frame.copy()

            ROI = crop_frame[y-pad:y+h+pad, x-pad:x+w+pad]
            crop.create_img_folder()         

            if not names_of_frames.get(i):
                names_of_frames[i] = 1

            crop.crop_img(ROI, i, names_of_frames)
            names_of_frames[i] += 1
            
            cv2.rectangle(draw_frame, p1_pad, p2_pad, crop.colors[i], thickness=2)

        cv2.imshow('IC - D&D', draw_frame)
        
        # close
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break

    cap.release()
    cv2.destroyAllWindows()
