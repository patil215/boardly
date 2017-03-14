


import requests

from PIL import Image, ImageFilter, ImageDraw
import math

import json


def manhattan(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

im = Image.open("test.jpg");

desiredWidth = 80.0
desiredHeight = 80.0

width = float(im.width)
height = float(im.height)

if((width / height) > (desiredWidth / desiredHeight)):
    # Image is too wide
    print "too wide"
    newWidth = (desiredWidth / desiredHeight) * height
    print newWidth
    widthDiff = width - newWidth
    im.crop(((widthDiff / 2), 0, width - (widthDiff / 2), height)).save("testout.jpg")
else:
    # Image is to tall
    newHeight = (desiredHeight / desiredWidth) * width
    print "too tall"
    heightDiff = height - newHeight
    print newHeight
    im.crop((0, (heightDiff / 2), width, height - (heightDiff / 2))).save("testout.jpg")

im = Image.open("testout.jpg")

desiredWidth = int(desiredWidth)
desiredHeight = int(desiredHeight)

im.resize((desiredWidth, desiredHeight)).save("testout2.jpg")

im = Image.open("testout2.jpg")
im = im.convert('1')
im.save("testout3.jpg")
im = Image.open("testout3.jpg")
#im = im.filter(ImageFilter.BLUR)
im = im.filter(ImageFilter.FIND_EDGES)

im = im.convert('RGB')


for widthInd in range(0, desiredWidth):
    for heightInd in range(0, desiredHeight):
        r, g, b = im.getpixel((widthInd, heightInd))
        if r < 128:
            im.putpixel((widthInd, heightInd), (255, 255, 255))
        else:
            im.putpixel((widthInd, heightInd), (0, 0, 0))

im.save("testout3.jpg")


im = Image.open("testout3.jpg")
im = im.convert('RGB')

unvisited = set()

output = Image.new("RGB", (desiredWidth, desiredHeight))

for widthInd in range(0, desiredWidth):
    for heightInd in range(0, desiredHeight):
        r, g, b = im.getpixel((widthInd, heightInd))
        output.putpixel((widthInd, heightInd), (255, 255, 255))
        if r < 128:
            unvisited.add((widthInd, heightInd))


draw = ImageDraw.Draw(output)

start = unvisited.pop()


lines = []


import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



while len(unvisited) > 0:
    found = False
    candidates = []
    for pos in unvisited:
        if manhattan(start, pos) > 0 and manhattan(start, pos) < 2:
            candidates.append(pos)
            break
    # pick the furthest one 
    furthestInd = 0
    """for i in range(1, len(candidates)):
        if manhattan(start, candidates[i]) > manhattan(start, candidates[furthestInd]):
            furthestInd = i"""

    if len(candidates) > 0:
        lines.append((start, candidates[furthestInd]))
        start = pos
        unvisited.remove(pos)
    else:
        start = unvisited.pop()

print len(lines)

print lines[0]

# Merge line segments

for i in range(0, 1):
    index = 0
    while index < len(lines) - 1:
        merged = False
        for d in range(index + 1, len(lines)):
            lineA = lines[index]
            lineB = lines[d]
            lineACheck = (lineA[1][0] - lineA[0][0], lineA[1][1] - lineA[0][1])
            lineBCheck = (lineB[1][0] - lineB[0][0], lineB[1][1] - lineB[0][1])
            #if lineA[0] == lineB[1]:
            if(manhattan(lineA[0], lineB[1]) < 0.25):
                if(angle_between(lineACheck, lineBCheck) < 100):
                    lineA = (lineB[0], lineA[1])
                    del lines[d]
                    merged = True
                    break
            #elif lineA[1] == lineB[0]:
            if(manhattan(lineA[1], lineB[0]) < 0.25):
                if(angle_between(lineACheck, lineBCheck) < 100):
                    lineA = (lineA[0], lineB[1])
                    del lines[d]
                    merged = True
                    break
        if not merged:
            index += 1
    
index = 0
for line in lines:
    draw.line([line[0], line[1]], fill=120)
    index += 1

output.save("output.jpg")

outputLines = []
for line in lines:
    outputLines.append(((line[0][0] / float(desiredWidth), line[0][1] / float(desiredHeight)), (line[1][0] / float(desiredWidth), line[1][1] / float(desiredHeight))))

outputLines = outputLines[0:4]
print outputLines

horiz_device_id = "3e0028000547343337373737"
vert_device_id = "TODO"

horizBody = {
        "role": True,
        "lines": outputLines,
        "numLines": len(lines)
}

vertBody = {
        "horiz": False,
        "lines": outputLines,
        "numLines" : len(lines)
}

#horizRequest = requests.post('https://api.particle.io/v1/devices/' + horiz_device_id + '/draw', data={'access_token': '5aed25589b822794ac4351bdaf26d53717694154', 'arg': json.dumps(horizBody)});
jsonStr = json.dumps(horizBody)
print jsonStr
horizRequest = requests.post('https://api.particle.io/v1/devices/' + horiz_device_id + '/draw', data={'access_token': '5aed25589b822794ac4351bdaf26d53717694154', 'arg': jsonStr});


"""vertRequest = requests.post('https://api.particle.io/v1/devices/' + vert_device_id + '/draw', data={'access_toke  n': '5aed25589b822794ac4351bdaf26d53717694154', 'arg':json.dumps(vertBody)});"""

print horizRequest.text
#print vertRequest.text

