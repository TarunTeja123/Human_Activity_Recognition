import cv2 
import argparse
import os
import subprocess
from random import randrange

folder = 'frames'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="optional path to video file")
args = vars(ap.parse_args())

def FrameCapture(path):     
    vidObj = cv2.VideoCapture(path)     
    count = 0
    success = 1
    #while success:
    while count<=25:
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read() 
  
        # Saves the frames with frame-count 
        cv2.imwrite("frames/frame%d.jpg" % count, image) 
  
        count += 1
  
# Driver Code 
if __name__ == '__main__':   
    # Calling the function 
    FrameCapture(args["input"])
    inputImage = "frames/frame"+str(randrange(25))+".jpg"
    runvalue  = "classify_image.py -i "+inputImage
    subprocess.call("python "+runvalue)
    harActivity = "human_activity_reco.py --model resnet-34_kinetics.onnx --classes action_recognition_kinetics.txt --input "+args["input"]
    subprocess.call("python "+harActivity)
    scores = "Reportgenearation.py"
    subprocess.call("python "+scores)
