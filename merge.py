import bpy, sys, os
import numpy as np
import random
import math

#sys.path.append('C:/Anand/blender_projects/MergeSort/constants.py')
#sys.path.append('//colors.py')
filepath = bpy.data.filepath
dir = os.path.dirname(filepath)

if not dir in sys.path:
   sys.path.append(dir)

from constants import  BLOCK_SIZE, X_AxisReferencePosition, UNSORTED_ARRAY, Z_AxisReferencePosition, BASE_DEPTH, SHOW_CODE_ANIMATION
from constants import  FRAME_RATE, FRAME_RATE_MULTIPLIER, PAUSE_FRAME, MOVING_SIZE

from colors import COLOR_MAP

from utils import *



frame_num = 0

def getValueFromElName(el):
    idxEl, idxVal = getIndexAndValueFromElName(el)
    return int(idxVal)



def getIndexAndValueFromElName(elName):
    split = elName.split('_')
    return split[1], split[3]


def renderChart():
    createElements(UNSORTED_ARRAY)
    return

def moveELementsToLeft(elementIds, currentLevel = 1):
    global frame_num
    print("FRAME NUM is {0}".format(frame_num)  )
    totalLevel =  math.ceil(math.log2(len(elementIds)))
    for elementId in elementIds:
        element = getObjFromId(elementId)
        currentX = element.location[0]
        futureX = currentX - MOVING_SIZE * len(elementIds) * max( totalLevel, 1)
        #print("MOVING ELEMENT ")
        moveElementToDestinationX(elementId, futureX, frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
    return FRAME_RATE * FRAME_RATE_MULTIPLIER + PAUSE_FRAME

def moveELementsToRight(elementIds, currentLevel = 1):
    global frame_num
    #print("FRAME NUM is {0}".format(frame_num)  )
    totalLevel =  math.ceil(math.log2(len(elementIds)))
    for elementId in elementIds:
        element = getObjFromId(elementId)
        currentX = element.location[0]
        futureX = currentX +  MOVING_SIZE * len(elementIds) * max( totalLevel, 1)
        moveElementToDestinationX(elementId, futureX, frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
    return FRAME_RATE * FRAME_RATE_MULTIPLIER + PAUSE_FRAME

highlight_frame_map = {}
def registerHighlightCodeFrames(codeLine, endFrame):
    global highlight_frame_map
    if SHOW_CODE_ANIMATION:
        highlight_frame_map[endFrame] = {
            'codeLine': codeLine
        }
    return

def highlightFrameCode(scene):
    current_frame  = scene.frame_current
    if current_frame % FRAME_RATE == 0:
        if current_frame in highlight_frame_map:
            makeCodeActive(highlight_frame_map[current_frame]['codeLine'])
    else :
        return
    return

arr_watcher_frame_map = {}
def registerArrWatcherFrame(value, endFrame, level, originalArr):
    #pri#nt("END FRAMES ARE {} with value".format(endFrame))
    #print(value)
    global arr_watcher_frame_map
    if SHOW_CODE_ANIMATION:
        arr_watcher_frame_map[endFrame] = {
            'value': ', '.join([str(getValueFromElName(item)) for item in value ]),
            'level': level,
            #'originalArray': ', '.join([str(getValueFromElName(item)) for item in originalArr ])
        }
    return


def highlightWatcherCode(scene):
    if SHOW_CODE_ANIMATION:
        current_frame  = scene.frame_current
        if current_frame % FRAME_RATE == 0:
            if current_frame in arr_watcher_frame_map:
                #print("SHOULD SHOW CURRENT FRAME {}".format(current_frame) )
                arrwatcher = getObjFromId('Arrwatcher')
                levelwatcher = getObjFromId('Levelwatcher')
                #originalArrayWatcher = getObjFromId('OriginalArrayWatcher')

                value = arr_watcher_frame_map[current_frame]['value']
                level = arr_watcher_frame_map[current_frame]['level']
                #originalArray = arr_watcher_frame_map[current_frame]['originalArray']

                arrwatcher.data.body = 'Input Arr = {}'.format(value)
                levelwatcher.data.body = 'Level = {}'.format(level)
                #originalArrayWatcher.data.body = 'UnSorted = {}'.format(originalArray)
                #  makeCodeActive(highlight_frame_map[current_frame]['codeLine'])
        else :
            return
        return

def moveCodeFrameToLine(toLine):
    if SHOW_CODE_ANIMATION:
        allZFrameLocation = getAllCodeFrameZLocation()
        registerHighlightCodeFrames(toLine, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
        return moveElementToDestinationZ('codeFrame', allZFrameLocation[toLine], frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER) + PAUSE_FRAME
    return 0


def mergeSort(arr, originalArr, level = 1, direction=''):
    global frame_num

    copiedArr = np.copy(arr)
    # if direction == 'L':
    #     #print('Move Arr to Left ')
    #     #print(arr)
    #     frame_num += moveELementsToLeft(arr, level)
    # if direction == 'R':
    #     #print('Move Arr to Right' )
    #     #print(arr)
    #     frame_num +=  moveELementsToRight(arr, level)
    # if direction == '':
    #     print('First Iteration')
    #     #print(arr)
    registerArrWatcherFrame(copiedArr, frame_num, level, originalArr)
    frame_num += moveCodeFrameToLine('line0')
    if len(arr) > 1:



         # Finding the mid of the array
        frame_num += moveCodeFrameToLine('line1')
        mid = len(arr)//2

        # Dividing the array elements
        frame_num += moveCodeFrameToLine('line2')
        L = arr[:mid]
        # into 2 halves
        frame_num += moveCodeFrameToLine('line3')
        R = arr[mid:]

        # Sorting the first half
        frame_num += moveCodeFrameToLine('line4')
        mergeSort(L, originalArr, level+1, 'L')

        # Sorting the second half
        frame_num += moveCodeFrameToLine('line5')
        mergeSort(R, originalArr, level+1, 'R')


        frame_num += moveCodeFrameToLine('line6')
        registerArrWatcherFrame(copiedArr, frame_num, level, originalArr)
        i = j = k = 0
        #print("ARR at {} level is".format(level))
        #print(arr)
        #return arr
        # Copy data to temp arrays L[] and R[]

        orriginal_x = []
        for elemId in L:
            elem = getObjFromId(elemId)
            orriginal_x.append(elem.location[0])
        for elemId in R:
            elem = getObjFromId(elemId)
            orriginal_x.append(elem.location[0])

        frame_num += moveCodeFrameToLine('line7')
        while i < len(L) and j < len(R):
            frame_num += moveCodeFrameToLine('line8')
            if getValueFromElName(L[i]) < getValueFromElName(R[j]):
                frame_num += moveCodeFrameToLine('line9')
                arr[k] = L[i]

                registerArrWatcherFrame(copiedArr, frame_num, level, originalArr)
                #registerArrWatcherFrame(arr, frame_num, level)
                frame_num += moveElementToDestinationX(L[i], orriginal_x[k], frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
                frame_num += PAUSE_FRAME
                frame_num += moveCodeFrameToLine('line10')
                i += 1
            else:
                frame_num += moveCodeFrameToLine('line12')
                arr[k] = R[j]

                registerArrWatcherFrame(copiedArr, frame_num, level, originalArr)
                #registerArrWatcherFrame(arr, frame_num, level)
                frame_num += moveElementToDestinationX(R[j], orriginal_x[k], frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
                frame_num += PAUSE_FRAME
                frame_num += moveCodeFrameToLine('line13')
                j += 1
            frame_num += moveCodeFrameToLine('line14')
            k += 1

        # Checking if any element was left
        frame_num += moveCodeFrameToLine('line15')
        while i < len(L):
            frame_num += moveCodeFrameToLine('line16')
            arr[k] = L[i]
            #registerArrWatcherFrame(arr, frame_num, level)

            registerArrWatcherFrame(copiedArr, frame_num, level, originalArr)
            frame_num += moveElementToDestinationX(L[i], orriginal_x[k], frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
            frame_num += PAUSE_FRAME
            frame_num += moveCodeFrameToLine('line17')
            i += 1
            frame_num += moveCodeFrameToLine('line18')
            k += 1
        frame_num += moveCodeFrameToLine('line19')
        while j < len(R):
            frame_num += moveCodeFrameToLine('line20')
            arr[k] = R[j]

            registerArrWatcherFrame(copiedArr, frame_num, level, originalArr)
            #registerArrWatcherFrame(arr, frame_num, level)
            frame_num += moveElementToDestinationX(R[j], orriginal_x[k], frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
            frame_num += PAUSE_FRAME
            frame_num += moveCodeFrameToLine('line21')
            j += 1
            frame_num += moveCodeFrameToLine('line22')
            k += 1
        # frame_num += PAUSE_FRAME
        # if direction == 'L':
        #     for elementCounter in range(0, k-2):
        #         kthElement = getObjFromId(arr[k-1])
        #         des_x = kthElement.location[0] - MOVING_SIZE * (k -elementCounter)
        #         moveElementToDestinationX(arr[elementCounter], des_x, frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
        # if direction == 'R':
        #     for elementCounter in range(k-1, 1, -1):
        #         zerothElement = getObjFromId(arr[0])
        #         des_x = zerothElement.location[0] + MOVING_SIZE * (elementCounter)
        #         moveElementToDestinationX(arr[elementCounter], des_x, frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
        frame_num += PAUSE_FRAME
    return arr




def getElementToFinalPosition(arr):
    for i, elementId in enumerate(arr):
        #print("POSITION WOULD BE" + str(extreme_left + BLOCK_SIZE * (i+0.5)))
        final_x = getXPositionBasedUponIndex(i)
        moveElementToDestinationX(elementId, final_x, frame_num, frame_num + FRAME_RATE * FRAME_RATE_MULTIPLIER)
    return FRAME_RATE * FRAME_RATE_MULTIPLIER
mappedChartWithArray = []
def run():
    global frame_num, mappedChartWithArray
    clearAllMaterial()
    clearObject()
    #clearAllMaterial()
    # return
    createMaterials()
    #mapColorToValues()
    renderChart()
    #renderIndex()
    #return
    if SHOW_CODE_ANIMATION:
        renderCode()
        registerHighlightCodeFrames('line0', 0)
        renderWatcher()
    #return
    # if animateString in bpy.app.handlers.frame_change_post:
    #     bpy.app.handlers.frame_change_post.remove(animateString)

    if highlightWatcherCode in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(highlightWatcherCode)

    if highlightFrameCode in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(highlightFrameCode)

    if(SHOW_CODE_ANIMATION):
        #bpy.app.handlers.frame_change_pre.append(highlightFrameCode)
        bpy.app.handlers.frame_change_pre.append(highlightWatcherCode)

    mappedChartWithArray = mapChartElWithArray(UNSORTED_ARRAY)
    for els in mappedChartWithArray:
        element = bpy.data.objects[els]
        element.keyframe_insert(data_path="location", frame = frame_num, index = -1 )

    # insertionSort(mappedChartWithArray)
    #print(frame_num)
    sortedArray = mergeSort(mappedChartWithArray, mappedChartWithArray)
    frame_num += PAUSE_FRAME
    getElementToFinalPosition(sortedArray)
    #print(sortedArray)
    #print(arr_watcher_frame_map)
    print(frame_num)
    return

run()