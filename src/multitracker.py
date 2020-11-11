import cv2

def select_bboxes(frame):
	bboxes = []
	retval, init_frame = cap.read()
	if not retval:
		print('Failed to read video')
		exit()
	while True:
		# draw bounding boxes over objects
		# selectROI's default behaviour is to draw box starting from the center
		# when fromCenter is set to false, you can draw box starting from top left corner
		bbox = cv2.selectROI('MultiTracker', init_frame)
		bboxes.append(bbox)
		print("Press q to quit selecting boxes and start tracking")
		print("Press any other key to select next object")
		k = cv2.waitKey(0) & 0xFF
		if (k == 113):  # q is pressed
			break
	return bboxes, init_frame

if __name__ == "__main__":

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

	cap = cv2.VideoCapture("videos/race.mp4")

	bboxes, init_frame = select_bboxes(cap)

	# Create MultiTracker object
	multiTracker = cv2.MultiTracker_create()

	# Initialize MultiTracker 
	for bbox in bboxes:
		multiTracker.add(cv2.TrackerCSRT_create(), init_frame, bbox)

	while cap.isOpened():
		retval, frame = cap.read()
		if not retval:
			break		
		
		success, boxes = multiTracker.update(frame)

		for i, newbox in enumerate(boxes):
			x, y, w, h = newbox
			p1 = (int(x), int(y))
			p2 = (int(x + w), int(y + h))
			cv2.rectangle(frame, p1, p2, colors[i], 2)

        # show frame
		cv2.imshow('MultiTracker', frame)
        
        # quit on ESC button or q button
		if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
			break