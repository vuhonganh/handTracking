import numpy as np
import argparse
import cv2

# init frame, region of interesting (roiPts), select mode (while selecting roi)
frame = None
roiPts = []
selectMode = False


def selectROI(event, x, y, flags, param):
	# get the reference to the current frame, 
	global frame, roiPts, selectMode

	# mouse left click 4 times to select the ROI 
	if selectMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
		roiPts.append((x, y))
		cv2.circle(frame, (x, y), 4, (255, 0, 0), 3)
		cv2.imshow("frame", frame)

def main():
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()

	# for loading a video: python camsiftTrack.py --video path-to-the-video
	ap.add_argument("-v", "--video",
		help = "path to the (optional) video file")
	args = vars(ap.parse_args())

	# get the reference to the current frame, list of ROI
	# points and whether or not it is ROI selection mode
	global frame, roiPts, selectMode

	# if the video path was not supplied, choose the webcam
	if not args.get("video", False):
		camera = cv2.VideoCapture(0)

	# otherwise, load the video
	else:
		camera = cv2.VideoCapture(args["video"])

	# setup the mouse callback (executed when a mouse event take place)
	cv2.namedWindow("frame")
	cv2.setMouseCallback("frame", selectROI)

	# initialize the termination criteria for cam shift, indicating
	# a maximum of 15 iterations or movement by a least one pixel
	# along with the bounding box of the ROI
	termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 1)
	roiBox = None

	# keep looping over the frames
	while True:
		# get the current frame
		grabbed, frame = camera.read()

		# check to see if we have reached the end of the video
		if not grabbed:
			break

		# if the ROI has been computed
		if roiBox is not None:
			# convert the current frame to the HSV color space
			# and perform mean shift
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)

			# apply cam shift to the back projection, convert the
			# points to a bounding box, and then draw them
			(r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
			pts = np.int0(cv2.cv.BoxPoints(r))
			cv2.polylines(frame, [pts], True, (255, 0, 0), 2)

		# show the frame and record if the user presses a key
		cv2.imshow("frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# handle if the 's' key is pressed, then go into ROI
		# selection mode
		if key == ord("s") and len(roiPts) < 4:
			# indicate that we are in select mode and clone the current frame (orig)
			selectMode = True
			orig = frame.copy()

			# keep looping until 4 reference ROI points have been selected
			# press any key to exit ROI selction mode once 4 points have been selected
			while len(roiPts) < 4:
				cv2.imshow("frame", frame)
				cv2.waitKey(0)

			# determine the top-left and bottom-right points
			roiPts = np.array(roiPts)
			s = roiPts.sum(axis = 1)
			tl = roiPts[np.argmin(s)]
			br = roiPts[np.argmax(s)]

			# grab the ROI for the bounding box and convert it to HSV color space
			roi = orig[tl[1]:br[1], tl[0]:br[0]]
			roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
			#roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

			# compute a HSV histogram for the ROI and store the bounding box
			roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
			roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
			roiBox = (tl[0], tl[1], br[0], br[1])

		# if the 'q' key is pressed, stop the loop
		elif key == ord("q"):
			break

	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
