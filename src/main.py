import imutils
import cv2
import os
from utils import (create_args,
				   delete_imgs,
				   set_start_video,
				   get_end_video,
				   add_pad)

#################
# TO DO
# multitrack
#################

if __name__ == "__main__":
	args = create_args()
	tracker = cv2.TrackerCSRT_create()
	temp = None
	# initialize the bounding box coordinates of the object we are going
	# to track
	initBB = None
	
	cap = cv2.VideoCapture(args["video"])
	time_to_start = set_start_video(cap)
	cap.set(cv2.CAP_PROP_POS_MSEC, (time_to_start))
	time_to_end = get_end_video(cap)

	img_n = -1
	key = ord("s")

	delete_imgs()

	pad = add_pad()

	while cap.isOpened():
		# grab the current frame, then handle if we are using a VideoCapture object
		ret, frame = cap.read()

		if cap.get(cv2.CAP_PROP_POS_MSEC) >= time_to_end:
			cv2.destroyAllWindows()
			extract_more = input("\nDo you wanna extract more frames? (Y) or (N): ")

			if extract_more.lower() in ["s","y"]:
				print(cap.get(cv2.CAP_PROP_POS_MSEC))
				
				#RESET THE TRACKING
				tracker.clear()
				tracker = cv2.TrackerCSRT_create()
				initBB = None
				
				while True:
					time_to_start = set_start_video(cap)
					if time_to_start > cap.get(cv2.CAP_PROP_POS_MSEC):
						break
				cap.set(cv2.CAP_PROP_POS_MSEC, (time_to_start))
				
				while True:
					time_to_end = get_end_video(cap)
					if time_to_end > time_to_start:
						break

				#set the frame to the new position
				ret, frame = cap.read()
				key = ord("s")
				print(cap.get(cv2.CAP_PROP_POS_MSEC))
			else: 
				break

		# check to see if we have reached the end of the stream
		if not ret:
			break

		# resize the frame (so we can process it faster) and grab the frame dimensions
		frame = imutils.resize(frame, width=1000)
		(H, W) = frame.shape[:2]

		# check to see if we are currently tracking an object
		if initBB is not None:
			img_n += 1
			# grab the new bounding box coordinates of the object
			(success, box) = tracker.update(frame)

			# check to see if the tracking was a success
			if success:
				(x, y, w, h) = [int(v) for v in box]

				# adding pad in imgs
				ROI = frame[y-int(pad):y+h+int(pad), x-int(pad):x+w+int(pad)]
				cv2.imwrite(f'images/frame_{img_n}.jpg', ROI)		
				cv2.rectangle(frame, (x - int(pad), y  - int(pad)), (x + w +int(pad), y + h +int(pad)), (0, 255, 0), 2)

		# show the output frame
		cv2.imshow("Frame", frame)

		# if the 's' key is selected, we are going to "select" a bounding
		# box to track
		if key == ord("s"):
			# select the bounding box of the object we want to track (make
			# sure you press ENTER or SPACE after selecting the ROI)
			initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
			
			# start OpenCV object tracker using the supplied bounding box coordinates
			tracker.init(frame, initBB)

		# if the `q` key was pressed, break from the loop
		elif key == ord("q"):
			break

		key = cv2.waitKey(1) & 0xFF

	# When everything done, release the video capture object
	cap.release()

	# close all windows
	cv2.destroyAllWindows()


