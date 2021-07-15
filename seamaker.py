import sys
import getopt
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = 9999999999

def usage():
    print('mapcropper.py -i <input file> -s <slope> -m <max depth> -o <output file>')

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"i:s:m:o:",[])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    myInput = ""
    mySlope = ""
    myMaxDepth = ""
    myOutput = ""

    for opt, arg in opts:
        if opt == "-i":
            myInput = arg
        elif opt == "-s":
            mySlope = arg
        elif opt == "-m":
            myMaxDepth = arg
        elif opt == "-o":
            myOutput = arg

    if ((myInput == '') or (mySlope == '') or (myMaxDepth == '') or (myOutput == '')):
        usage()
        sys.exit(2)        

    inputFile = myInput
    slope = float(mySlope)
    maxDepth = int(myMaxDepth)
    outputFile = myOutput

    print("Loading image...")
    img = Image.open(inputFile)
    imgArr = np.float64(np.asarray(img))
    
    print("processing image....")
    depth = 0
    selection = np.copy(imgArr <= (32768 - depth))*1
    while 1:
        if depth >= maxDepth:
            break
        print(depth)
        if selection.sum() == 0:
            break
        #Image.fromarray(np.uint16(selection * 32000)).save(f"D:/0_{depth}.png")
        selection = shrinkSelection(selection)
        #Image.fromarray(np.uint16(selection * 3200)).save(f"D:/1_{depth}.png")
    
        depth = depth + slope
        imgArr = imgArr - selection * slope


    print("writing image...")
    imgArr = imgArr * (imgArr > 0)
    image = Image.fromarray(np.uint16(imgArr))
    image.save(outputFile)

def shrinkSelection(selection):
    #inverse seleciton and expand it
    ret = selection.copy()
    shiftm1p0 = np.roll(selection, -1, axis = 0)
    shiftm1p0[-1,:] = selection[-1,:]
    shiftp1p0 = np.roll(selection,  1, axis = 0)
    shiftp1p0[0,:] = selection[0,:]
    shiftp0m1 = np.roll(selection, -1, axis = 1)
    shiftp0m1[:,-1] = selection[:,-1] 
    shiftp0p1 = np.roll(selection,  1, axis = 1)
    shiftp0p1[:,0] = selection[:,0]

    return ((ret + shiftm1p0 + shiftp1p0 + shiftp0m1 + shiftp0p1) == 5)*1

def expand(selection, radius):
    cop = np.copy(selection)
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            if (y==0 and x==0) or (x**2 + y**2 > radius **2):
                continue
            shift = np.roll(np.roll(selection, y, axis = 0), x, axis = 1)
            cop += shift

    return cop



if __name__ == "__main__":
   main(sys.argv[1:])

