import os
import cv2
import imutils

class Crop:

    #RGB (OpenCV works on BGR)
    colors = [
        (255, 0, 0), # red
        (0, 255, 0), # green
        (0, 0, 255), # blue
        (255, 128, 0), # orange
        (255, 255, 0), # yellow
        (255, 0, 127), #pink
        (0, 0, 0), # black
        (127, 0, 255), #purple
        (0, 255, 255), #ciano
        (128, 128, 128), #grey
    ]    

    def __init__(self, file_name, video, resize=None):
        self.file_name = file_name
        self.video = video
        self.resize = resize
        self.n_of_slices = 0

    def select_bboxes(self):
        self.n_of_trackers = 1
        bboxes = []
        retval, init_frame = self.video.read()
        if not retval:
            print('Failed to read video')
            exit()
        while True:
            # draw bounding boxes over objects
            # selectROI's default behaviour is to draw box starting from the center
            # when fromCenter is set to false, you can draw box starting from top left corner
            if self.resize["bool"]:
                init_frame = imutils.resize(init_frame, width=self.resize["width"])
            print()
            bbox = cv2.selectROI('IC - D&D', init_frame)
            
            if bbox == (0, 0, 0, 0): #esc pressed
                exit()

            if len(bbox) == 0: #esc pressed
                print("\nNo one bounding box detected, exiting...")
                exit()

            bboxes.append(bbox)
            print(f"\nNUMBER OF TRACKERS: {self.n_of_trackers}")
            create_more = input("Do you wanna CREATE more trackers? ")
            if create_more.lower() in ["n"]:
                break
            self.n_of_trackers += 1
            # print("Press q to quit selecting boxes and start tracking")
            # print("Press any other key to select next object")
            # k = cv2.waitKey(0) & 0xFF
            # if (k == 113):  # q is pressed
            #     break
        return bboxes, init_frame

    def update_time_video(self, time_to_start):
        self.video.set(cv2.CAP_PROP_POS_MSEC, (time_to_start))
        self.video.read()

    def get_current_time(self):
        return self.video.get(cv2.CAP_PROP_POS_MSEC)

    def create_img_folder(self):
        for i in range(self.n_of_trackers):
            path = os.path.join(".","imgs",self.file_name+"_slice-"+str(self.n_of_slices)+"_track-"+str(i))
            if not os.path.isdir(path):
                os.makedirs(path)

    @staticmethod
    def init_tracker(bboxes, frame):
        multiTracker = cv2.MultiTracker_create()
        for bbox in bboxes:
            multiTracker.add(cv2.TrackerCSRT_create(), frame, bbox)
        return multiTracker

    @staticmethod
    def set_start_video():
        start = float(input("\nInput the time that you wish start the cut: "))
        return start*1000.0

    @staticmethod
    def set_end_video():
        end = float(input("Input the time that you wish end the cut: "))
        return end*1000.0

    @staticmethod
    def add_pad():
        return int(input("Input the value of the pad: "))

    @staticmethod
    def extract_more():
        extract_more = input("\nDo you wanna EXTRACT more frames? ")
        return True if extract_more.lower() in ["s","y"] else False

    @staticmethod
    def delete_imgs(path=os.path.join("imgs","")):
        # op = input("Delete all images folders? ")
        op = "y"
        if op.lower() in ["s","y"]:
            filelist = [f for f in os.listdir(path)]
            for f in filelist:
                os.removedirs(os.path.join(path,f))
    