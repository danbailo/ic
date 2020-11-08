import argparse
import imutils
import cv2
import os

#################
# TO DO
# selecionar tempo para inicio e fim do track
# multitrack
#################


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
args = vars(ap.parse_args())

# "csrt": cv2.TrackerCSRT_create,
# "kcf": cv2.TrackerKCF_create,
# "boosting": cv2.TrackerBoosting_create,
# "mil": cv2.TrackerMIL_create,
# "tld": cv2.TrackerTLD_create,
# "medianflow": cv2.TrackerMedianFlow_create,
# "mosse": cv2.TrackerMOSSE_create

tracker = cv2.TrackerCSRT_create()

temp = None

# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

cap = cv2.VideoCapture(args["video"])

# loop over frames from the video stream
img_n = -1
key = ord("s")

op = input("Delete all images? ")
if op.lower() in ["s","y"]:
	filelist = [ f for f in os.listdir("images") if f.endswith(".jpg") ]
	for f in filelist:
		os.remove(os.path.join("images", f))

padding = input("add padding? ")

while cap.isOpened():
	# grab the current frame, then handle if we are using a VideoCapture object
	ret, frame = cap.read()

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

			# adding padding in imgs
			ROI = frame[y-int(padding):y+h+int(padding), x-int(padding):x+w+int(padding)]
			cv2.imwrite(f'images/frame_{img_n}.jpg', ROI)		
			cv2.rectangle(frame, (x - int(padding), y  - int(padding)), (x + w +int(padding), y + h +int(padding)), (0, 255, 0), 2)

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