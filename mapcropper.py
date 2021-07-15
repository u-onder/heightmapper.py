import sys
import getopt
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = 9999999999

def usage():
    print('mapcropper.py -i <input file> -w <crop width> -h <crop height> -x <x offset> -y <y offset> -o <output file>')
    print('\nNote: assume image origin as top-left of the image')

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"i:w:h:x:y:o:",[])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    myInput = ""
    myWidth = ""
    myHeight = ""
    myXOfffset = ""
    myYOffset = ""
    myOutput = ""

    for opt, arg in opts:
        if opt == "-i":
            myInput = arg
        elif opt == "-w":
            myWidth = arg
        elif opt == "-h":
            myHeight = arg
        elif opt == "-x":
            myXOfffset = arg
        elif opt == "-y":
            myYOffset = arg
        elif opt == "-o":
            myOutput = arg

    if ((myInput == '') or (myWidth == '') or (myHeight == '') or (myXOfffset == '') or (myYOffset == '') or (myOutput == '')):
        usage()
        sys.exit(2)        

    inputFile = myInput
    width = int(myWidth)
    height = int(myHeight)
    xOfffset = int(myXOfffset)
    yOffset = int(myYOffset)
    outputFile = myOutput

    print("Loading image...")
    img = Image.open(inputFile)
    imgArr = np.asarray(img)
    
    imgWidth = imgArr.shape[1]
    imgHeigth = imgArr.shape[0]

    outarr = imgArr[yOffset:yOffset+height, xOfffset:width+xOfffset]
    
    print("writing image...")
    image = Image.fromarray(outarr)
    image.save(outputFile)

if __name__ == "__main__":
   main(sys.argv[1:])

