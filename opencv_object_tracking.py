# USAGE
# python opencv_object_tracking.py
# python opencv_object_tracking.py --video dashcam_boston.mp4 --tracker csrt

# import the necessary packages
import argparse
import imutils
import cv2

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

vs = cv2.VideoCapture(args["video"])

# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
img_n = -1
key = ord("s")
while True:
	# grab the current frame, then handle if we are using a VideoStream or VideoCapture object
	frame = vs.read()
	# frame = frame[1] if args.get("video", False) else frame
	frame = frame[1]

	# check to see if we have reached the end of the stream
	if frame is None:
		break

	# resize the frame (so we can process it faster) and grab the
	# frame dimensions
	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]

	# check to see if we are currently tracking an object
	if initBB is not None:
		img_n += 1
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)

		# check to see if the tracking was a success
		if success:		
			(x, y, w, h) = [int(v) for v in box]
			ROI = frame[y:y+h, x:x+w]
			cv2.imwrite(f'images/frame_{img_n}.jpg', ROI)		
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

	# show the output frame
	cv2.imshow("Frame", frame)

	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		
		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		tracker.init(frame, initBB)

	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

	key = cv2.waitKey(1) & 0xFF
vs.release()

# close all windows
cv2.destroyAllWindows()