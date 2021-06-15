import sys
import getopt
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = 9999999999

def usage():
    print('heightmapsplit.py -i <input file> -w <split width> -h <split height> -x <x offset> -y <y offset> -p <output file prefix>')
    print('\nNote: assume image origin as top-left of the image')

# old API key is dmlO1fVQRPKI-GrVIYJ1YA
# my  API key is hUYXm28xTuq1x7qLoLuKwA
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"i:w:h:x:y:p:",[])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    myInput = ""
    myWidth = ""
    myHeight = ""
    myXOfffset = ""
    myYOffset = ""
    myPrefix = ""

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
        elif opt == "-p":
            myPrefix = arg

    if ((myInput == '') or (myWidth == '') or (myHeight == '') or (myXOfffset == '') or (myYOffset == '') or (myPrefix == '')):
        usage()
        sys.exit(2)        

    inputFile = myInput
    width = int(myWidth)
    height = int(myHeight)
    xOfffset = int(myXOfffset)
    yOffset = int(myYOffset)
    prefix = myPrefix

    print("Loading image...")
    img = Image.open(inputFile)
    imgArr = np.asarray(img)
    
    imgWidth = imgArr.shape[1]
    imgHeigth = imgArr.shape[0]

    x = xOfffset
    xCount = 0
    while x < imgWidth:
        if (x + width > imgWidth):
            break
        y = yOffset
        yCount = 0
        while y < imgHeigth:
            if (y + height > imgHeigth):
                break
            outFile = prefix + "_X" +str(xCount) + "_Y" + str(yCount) + ".png"
            print("Creating sub-image " + outFile)
            outarr = imgArr[y:y+height, x:x+width]
            image = Image.fromarray(outarr)
            image.save(outFile)
            y += height-1
            yCount += 1
        x += width-1
        xCount += 1


if __name__ == "__main__":
   main(sys.argv[1:])

