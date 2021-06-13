import sys
import getopt
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import math
from pathlib import Path
import os


def usage():
    print('download.py -z <zoomlevel> -t <top Longitude> -b <bottom longitude> -l <left latitude> -r <right latitude> -o <outputfilename> -m <minimum threshold> -x <maimum trhreshold>')

# old API key is dmlO1fVQRPKI-GrVIYJ1YA
# my  API key is hUYXm28xTuq1x7qLoLuKwA
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"z:t:b:l:r:o:x:m:",["zoom=","top=","bottom=","left=","right=","ofile=","max=","min="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    myZoom = ""
    myTop = ""
    myBottom = ""
    myLeft = ""
    myRight = ""
    myMax = "4096"
    myMin = "0"
    myFile = ""


    for opt, arg in opts:
        if opt == "-z":
            myZoom = arg
        elif opt == "-t":
            myTop = arg
        elif opt == "-b":
            myBottom = arg
        elif opt == "-l":
            myLeft = arg
        elif opt == "-r":
            myRight = arg
        elif opt == "-x":
            myMax = arg
        elif opt == "-m":
            myMin = arg
        elif opt == "-o":
            myFile = arg

    if ((myZoom == '') or (myTop == '') or (myBottom == '') or (myLeft == '') or (myRight == '') or (myMax == '') or (myMin == '') or (myFile == '')):
        usage()
        sys.exit(2)        

    zoom = int(myZoom)
    top = getYTerm(int(myZoom), float(myTop))
    bottom = getYTerm(int(myZoom), float(myBottom))
    left = getXTerm(int(myZoom), float(myLeft))
    right = getXTerm(int(myZoom), float(myRight))
    heighThreshold = int(myMax)
    lowThreshold = int(myMin)

    print("top : " + str(top))
    print("bottom : " + str(bottom))
    print("left : " + str(left))
    print("right : " + str(right))

    maxX = (2 ** zoom)

    if (left >= right):
        right = right + maxX

    arr = np.zeros(((bottom-top+1)*256,(right-left+1)*256), dtype=np.uint16)

    x = left
    _x = 0
    for i in range(left, right+1):
        y = top
        _y = 0
        for j in range(top, bottom+1):
            print("/"+str(zoom)+"/"+str(x)+"/"+str(y)+".png")
            img = dowmloadImage(str(zoom),str(x),str(y), 1)
            result = processImage(img, lowThreshold, heighThreshold)
            arr[_y*256:(_y+1)*256,_x*256:(_x+1)*256] = result

            y = y + 1
            _y = _y + 1

        _x = _x + 1
        x = x + 1
        if (x >= maxX):
            x = x - maxX

    resultImage = arrayToImage(arr)
    resultImage.save(myFile)
    resultImage.show()

  
def getXTerm(zoom, longitude):
    xterm = (2**zoom)*(longitude+180)/360
    term = math.floor(xterm)
    if term < 0:
        term = 0
    if term >= (2**zoom):
        term = (2**zoom) - 1
    return term

def getYTerm(zoom, latitude):
    yterm = (1-math.log(math.tan(latitude*math.pi/180)+1/math.cos(latitude*math.pi/180))/math.pi)*(2 ** (zoom-1))
    term = math.floor(yterm)
    if term < 0:
        term = 0
    if term >= (2**zoom):
        term = (2**zoom) - 1
    return term

def dowmloadImage(zoom, xterm, yterm, enableCache):
    if (enableCache):
        fName = "Cache/"+zoom+"_"+xterm+"_"+yterm+".png"
        myFile = Path(fName)
        if myFile.is_file():
            return Image.open(fName)

    response = requests.get("https://tile.nextzen.org/tilezen/terrain/v1/256/terrarium/"+zoom+"/"+xterm+"/"+yterm+".png?api_key=hUYXm28xTuq1x7qLoLuKwA&")

    stream = BytesIO(response.content)
    image = Image.open(stream).convert("RGBA")
    stream.close()

    if (enableCache):
        if not os.path.exists("Cache"):
            os.makedirs("Cache")
        image.save("Cache/"+zoom+"_"+xterm+"_"+yterm+".png")

    return image

def processImage(image, lowThreshold, heighThreshold):
    delta = heighThreshold - lowThreshold
    arr0 = np.asarray(image)
    arr1 = arr0.reshape((-1,4))
    arr2 = 256.0*arr1[:,0] + 1.0*arr1[:,1] - 32768.0
    arr3 = arr2 * (arr2 > lowThreshold)
    arr4 = arr3 * (arr3 < heighThreshold) + (arr3 >= heighThreshold) * heighThreshold
    arr4 = arr4-lowThreshold
    arr4 = arr4/delta
    arr5 = arr4.reshape((256,256))

    return np.uint16(arr5*65535)

def arrayToImage(arr):
    image = Image.fromarray(arr)
    return image


if __name__ == "__main__":
   main(sys.argv[1:])


#lng = 29.0509
#lat = 41.0864
#zoom = 10
#
#xTileNum = (2**zoom)*(lng+180)/360
#yTileNum = (1-math.log(math.tan(lat*math.pi/180)+1/math.cos(lat*math.pi/180))/math.pi)*(2 ** (zoom-1))
#
#print(xTileNum)
#print('\n')
#print(yTileNum)
#
#response = requests.get("https://tile.nextzen.org/tilezen/terrain/v1/256/terrarium/1/1/1.png?api_key=hUYXm28xTuq1x7qLoLuKwA&")
#
#stream = BytesIO(response.content)
#image = Image.open(stream).convert("RGBA")
#stream.close()
#
#threshold = 3072
#arr0 = np.asarray(image)
#arr1 = arr0.reshape((-1,4))
#arr2 = 256.0*arr1[:,0] + 1.0*arr1[:,1] - 32768.0
#arr3 = arr2 * (arr2 > 0)
#arr4 = arr3 * (arr2 < threshold) / threshold + (arr2 >= threshold)
#arr5 = arr4.reshape((256,256))
#
#image2 = Image.fromarray(np.uint16(arr5*65535))
#image2.show()
#
#image2.save("grayscale_1_1_1.png")

#("1", "2", "3", "4")
#("5", "6", "7", "8")
#("a", "b", "c", "d")
#("e", "f", "g", "h")
#
#a00 = np.array(("1","2","5","6")).reshape((2,2))
#a10 = np.array(("3","4","7","8")).reshape((2,2))
#a01 = np.array(("a","b","e","f")).reshape((2,2))
#a11 = np.array(("c","d","g","h")).reshape((2,2))
#
#a0x = np.concatenate((a00,a01), axis=0)
#a1x = np.concatenate((a10,a11), axis=0)
#axx = np.concatenate((a0x,a1x), axis=1)
#
#python download.py -z 1 -l -179 -r 179 -t 84 -b -84 -x 4900