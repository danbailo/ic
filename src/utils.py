import argparse
import os

def create_args():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v",
					"--video",
					type=str, 
					help="path to input video file")
	return vars(ap.parse_args())	

def delete_imgs():
	op = input("Delete all images? ")
	if op.lower() in ["s","y"]:
		filelist = [ f for f in os.listdir("images") if f.endswith(".jpg") ]
		for f in filelist:
			os.remove(os.path.join("images", f))

def set_start_video(cap):
	start = float(input("Input the time that you wish start the cut: "))
	return start*1000.0

def get_end_video(cap):
	end = float(input("Input the time that you wish end the cut: "))
	return end*1000.0

def add_pad():
	return int(input("Input the value of the pad: "))