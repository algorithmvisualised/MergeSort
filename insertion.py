import bpy
import numpy as np
import random

SHOW_CODE_ANIMATION = False

if SHOW_CODE_ANIMATION:
    TOTAL_NUMBERS = 16
    UNSORTED_ARRAY =  np.random.randint(low = 1, high = 10, size=TOTAL_NUMBERS)
    print(UNSORTED_ARRAY)
    UNSORTED_ARRAY = [8, 3, 1, 6, 4, 2, 9, 5 ]
else:
    TOTAL_NUMBERS = 3
    UNSORTED_ARRAY =  np.random.randint(low = 1, high = 3 , size=TOTAL_NUMBERS)
    UNSORTED_ARRAY = [12, 11, 13, 5, 6, 7 ]
    print(UNSORTED_ARRAY)

TOTAL_BLOCKS = len(UNSORTED_ARRAY)

if SHOW_CODE_ANIMATION:
    X_AxisReferencePosition = 5.8
    Z_AxisReferencePosition = 0
else:
    X_AxisReferencePosition = -0
    Z_AxisReferencePosition = -7


BLOCK_SIZE = 1
BASE_BUFFER_WIDTH = 2
BASE_WIDTH = TOTAL_BLOCKS * BLOCK_SIZE
BASE_DEPTH = COLUMN_DEPTH = 1
BASE_HEIGHT = 0.05
COLUMN_BUFFER_HEIGHT = 5
COLUMN_HEIGHT = np.amax(UNSORTED_ARRAY)  + COLUMN_BUFFER_HEIGHT
COLUMN_WIDTH = 0.05
frame_num = 1
FRAME_RATE = 2
FRAME_RATE_MULTIPLIER = 1
UNIT_PER_FRAME = BLOCK_SIZE / FRAME_RATE
ELEMENT_STRING = 'element_{0}_value_{1}'
CODE_LINE_HEIGHT = 2.8


text_animation_map = {}
red = bpy.data.materials.new('Red')
blue = bpy.data.materials.new('Blue')
yellow = bpy.data.materials.new('Yellow')

bpy.context.scene.frame_set(frame_num)

color_map = {}
highlight_frame_map = {}
i_watcher_frame_map = {}
j_watcher_frame_map = {}
key_watcher_frame_map = {}
arr_j_watcher_frame_map = {}

HIGHLIGHT_FRAME_STRING = 'startFrame_{0}_endframe_{1}'

INACTIVE_CODE_COLOR = (1, 0.05, 0.16, 1)
INACTIVE_CODE_MATERIAL_NAME = 'material_inactive_code'

ACTIVE_CODE_COLOR = (0, 0, 1, 1)
ACTIVE_CODE_MATERIAL_NAME = 'material_active_code'

INACTIVE_CODE_MATERIAL = False
ACTIVE_CODE_MATERIAL = False

WATCHER_COLOR = (0.748, 0.159, 0.568, 1)




def createMaterials():
    global INACTIVE_CODE_MATERIAL, ACTIVE_CODE_MATERIAL

    INACTIVE_CODE_MATERIAL = bpy.data.materials.new(INACTIVE_CODE_MATERIAL_NAME)
    #INACTIVE_CODE_MATERIAL.name = INACTIVE_CODE_MATERIAL_NAME
    INACTIVE_CODE_MATERIAL.diffuse_color = INACTIVE_CODE_COLOR
    #bpy.context.object.active_material.metallic = 1
    #INACTIVE_CODE_MATERIAL.metallic = 0.1

    ACTIVE_CODE_MATERIAL = bpy.data.materials.new(ACTIVE_CODE_MATERIAL_NAME)
    ACTIVE_CODE_MATERIAL.diffuse_color = ACTIVE_CODE_COLOR
    #ACTIVE_CODE_MATERIAL.metallic = 0.1

def mapColorToValues():
    global color_map, UNSORTED_ARRAY
    for i in range(1, 100):
        color_map[i] = get_random_color()
    return


def setColorToElementFromMap(obj, obj_id, val):
    global color_map
    material = setColor(obj, obj_id, color_map.get(val))
    #material.metallic = 0.1
    return

def setColor(obj, obj_id, color):
    material = bpy.data.materials.new('material_' + obj_id)
    material.diffuse_color = color
    #material.specular_hardness = 200
    obj.data.materials.append(material)
    return material


def clearAllMaterial():
    #return
    for material in bpy.data.materials:
        #material.user_clear()
        bpy.data.materials.remove(material)
    return

def clearObject():
    for ob in bpy.context.scene.objects:
        print(ob.type)
    objs = [ob for ob in bpy.context.scene.objects if ob.type in ('MESH', 'FONT')]
    bpy.ops.object.delete({"selected_objects": objs})
    return

def createBase():
    bpy.ops.mesh.primitive_cube_add(location=(X_AxisReferencePosition, 0, Z_AxisReferencePosition), scale=(BASE_WIDTH, BASE_DEPTH, BASE_HEIGHT))
    cube = bpy.context.object
    cube.name = 'cube_base'
    return

def createColumn():
    bpy.ops.mesh.primitive_cube_add(
        location=(0-COLUMN_WIDTH - BASE_WIDTH/2, 0, COLUMN_HEIGHT/2),
        scale=(COLUMN_WIDTH, COLUMN_DEPTH, COLUMN_HEIGHT)
    )
    cube = bpy.context.object
    cube.name = 'cube_column'
    return

def getElName(i, val):
    txt = ELEMENT_STRING
    return txt.format(i, val)

def getIndexAndValueFromElName(elName):
    split = elName.split('_')
    return split[1], split[3]


def getXPositionBasedUponIndex(index):
    extreme_left = X_AxisReferencePosition - BASE_WIDTH/2
    return extreme_left + BLOCK_SIZE * (index + 0.5)

def createElements():
    extreme_left = X_AxisReferencePosition - BASE_WIDTH/2
    for i, val in enumerate(UNSORTED_ARRAY):
        #print("POSITION WOULD BE" + str(extreme_left + BLOCK_SIZE * (i+0.5)))
        element_location = (getXPositionBasedUponIndex(i) , 0, Z_AxisReferencePosition + val/2)
        element_scale = (BLOCK_SIZE, BASE_DEPTH, val)
        #print("ELEMENT SCALE WOULD BE")
        print(element_scale)
        bpy.ops.mesh.primitive_cube_add(
            location=element_location,
            #scale=element_scale
        )
        element = bpy.context.object
        element.dimensions = element_scale
        element.name = getElName(i, val)
        element.display.show_shadows = False
        setColorToElementFromMap(element, element.name, val)
    return


def createAxis():
    createBase()
    #createColumn()
    return

def renderChart():
    createAxis()
    createElements()
    #createElementsAsNumber()
    return


def registerHighlightCodeFrames(codeLine, startFrame, endFrame):
    global highlight_frame_map
    highlight_frame_map[HIGHLIGHT_FRAME_STRING.format(startFrame, endFrame)] = {
        'startFrame': startFrame,
        'endFrame': endFrame,
        'activeline': codeLine
    }
    return

def registerIWatcherFrame(value, startFrame, endFrame):
    global i_watcher_frame_map
    i_watcher_frame_map[HIGHLIGHT_FRAME_STRING.format(startFrame, endFrame)] = {
        'startFrame': startFrame,
        'endFrame': endFrame,
        'value': value
    }
    return

def registerKeyWatcherFrame(value, startFrame, endFrame):
    global key_watcher_frame_map
    key_watcher_frame_map[HIGHLIGHT_FRAME_STRING.format(startFrame, endFrame)] = {
        'startFrame': startFrame,
        'endFrame': endFrame,
        'value': value
    }
    return

def registerJWatcherFrame(value, startFrame, endFrame):
    global j_watcher_frame_map
    #print("REGISTERING J WATCHER WITH VALUE {0} START FRAME {1} END FRAME {2}".format(value, startFrame, endFrame))
    j_watcher_frame_map[HIGHLIGHT_FRAME_STRING.format(startFrame, endFrame)] = {
        'startFrame': startFrame,
        'endFrame': endFrame,
        'value': value
    }
    return
def registerArrjWatcherFrame(value, startFrame, endFrame):
    global arr_j_watcher_frame_map
    arr_j_watcher_frame_map[HIGHLIGHT_FRAME_STRING.format(startFrame, endFrame)] = {
        'startFrame': startFrame,
        'endFrame': endFrame,
        'value': value
    }
    return

def insertionSort(arr):
    global frame_num, FRAME_RATE
    original_arr = np.copy(arr)
    for i in range(1, len(arr)):
        #print("FRAME NUM IS !!!" + str(frame_num))
        registerHighlightCodeFrames( 'line0', frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        registerIWatcherFrame(i, frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        registerKeyWatcherFrame("", frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        registerJWatcherFrame("", frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        frame_num += moveElementToDestinationZ(
            'codeFrame',
            10.3,
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        #print("FRAME NUM IS ****" + str(frame_num))
        key = arr[i]
        keyValue = getValueFromElName(key)
        moveElementToDestinationX(
            'IText',
            getXPositionBasedUponIndex(i),
                #getXPositionBasedUponIndex(j + 1),
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        moveElementToDestinationX(
            'KeyText',
            getXPositionBasedUponIndex(i),
                #getXPositionBasedUponIndex(j + 1),
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        registerHighlightCodeFrames( 'line1', frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        registerKeyWatcherFrame(keyValue, frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        frame_num += moveElementToDestinationZ(
            'codeFrame',
            7.1,
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        j = i -1

        #######
        finalKeyPositionX = bpy.data.objects[arr[j]].location[0]
        ######
        registerHighlightCodeFrames( 'line2', frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        registerJWatcherFrame(j, frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        registerArrjWatcherFrame(getValueFromElName(arr[j]), frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        moveElementToDestinationX(
            'JText',
            getXPositionBasedUponIndex(j),
                #getXPositionBasedUponIndex(j + 1),
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        frame_num += moveElementToDestinationZ(
            'codeFrame',
            3.8,
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        while (j >= 0 and True):
            #print("JTH VALUE IS " + str(getValueFromElName(arr[j])))
            registerHighlightCodeFrames( 'line3', frame_num, frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
            registerJWatcherFrame(j, frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
            registerArrjWatcherFrame(getValueFromElName(arr[j]), frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
            moveElementToDestinationX(
                'JText',
                getXPositionBasedUponIndex(j),
                #getXPositionBasedUponIndex(j + 1),
                frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
            )
            frame_num += moveElementToDestinationZ(
                'codeFrame',
                0.43,
                frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
            )
            if( not(keyValue < getValueFromElName(arr[j])) ):
                break
            #registerHighlightCodeFrames( 'line4', frame_num, frame_num + 2 * FRAME_RATE)
            # frame_num += moveElementToDestinationZ(
            #     'codeFrame',
            #     2,
            #     frame_num,
            #     frame_num + 2 * FRAME_RATE
            # )
            # swapElementsWithAnimation(
            #     arr[i],
            #     arr[min_idx],
            #     current_frame,
            #     current_frame + FRAME_RATE
            # )

            jthplueOneElement = arr[j+1]
            jthElement = arr[j]
            print("J+1 is {0} and J is {1}".format(jthplueOneElement, jthElement))
            arr[j+1] = arr[j]
            registerHighlightCodeFrames( 'line4', frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)

            frame_num += moveElementToDestinationZ(
                'codeFrame',
                -2.8,
                frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
            )
            # frame_num += hideJthPlusOneAndMoveJthElementToIt(
            #     jthElement,
            #     jthplueOneElement,
            #     frame_num,
            #     frame_num + 2 * FRAME_RATE
            # )
            frame_num += moveElementToDestinationX(
                jthElement,
                getXPositionBasedUponIndex(j + 1),
                #getXPositionBasedUponIndex(j + 1),
                frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
            )
            j -= 1
            if( j >= 0):
                finalKeyPositionX = bpy.data.objects[arr[j]].location[0]
            ####
            registerHighlightCodeFrames( 'line5', frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
            registerJWatcherFrame(j, frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
            if(j >= 0):
                registerArrjWatcherFrame(getValueFromElName(arr[j]), frame_num, frame_num + 2 * FRAME_RATE)
            else :
                registerArrjWatcherFrame("", frame_num,
                    frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
            frame_num += moveElementToDestinationZ(
                'codeFrame',
                -6.2,
                frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        finalSwapJPlueOne = arr[j+1]
        finalSwapJ = key
        #print("FINAL SWAP J+1 is {0} and final Swap is {1}".format(finalSwapJPlueOne, finalSwapJ))
        arr[j+1] = key
        registerHighlightCodeFrames( 'line6', frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE)
        frame_num += moveElementToDestinationZ(
            'codeFrame',
            -9.4,
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        print("SHOULD MOVE ELEMENT {0} to {1}".format(finalSwapJ, finalKeyPositionX))
        #getXPositionBasedUponIndex

        moveElementToDestinationX(
            'KeyText',
            getXPositionBasedUponIndex(j + 1),
                #getXPositionBasedUponIndex(j + 1),
            frame_num,
            frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )
        frame_num += moveElementToDestinationX(
                finalSwapJ,
                getXPositionBasedUponIndex(j + 1),
                frame_num,
                frame_num + FRAME_RATE_MULTIPLIER * FRAME_RATE
        )

        #frame_num += hideJthPlusOneAndMoveJthElementToIt(
        #        key,
        #        jthplueOneElement,
        #        frame_num,
        #        frame_num + 2 * FRAME_RATE
        #)
        #print("ARR WOULD BE")
        #print(arr)
    return arr

def mergeSort(arr):
    if len(arr) > 1:

         # Finding the mid of the array
        mid = len(arr)//2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        mergeSort(L)

        # Sorting the second half
        mergeSort(R)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return


def hideJthPlusOneAndMoveJthElementToIt(jthElementId, jthPlusOneElementId, startFrame, endFrame):
    global frame_num, FRAME_RATE
    jthPlusOneElement = bpy.data.objects[jthPlusOneElementId]
    #jthPlusOneElementId.hide()
    #element_1 = bpy.data.objects[el_1]
    #element_2 = bpy.data.objects[el_2]

    #print("ELEMENT IDs are " + el_1 + " , " + el_2 )
    #element_1_x = jthPlusOneElement.location[0]
    element_2_x = jthPlusOneElement.location[0]

    #print("ELEMENT LOCATIONs are " + str(element_1_x) + " , " + str(element_2_x) )
    #print("SHOULD MOVE ELEMENT {0} to {1}".format(finalSwapJ, finalKeyPositionX))
    return moveElementToDestinationX(
                    jthElementId,
                    element_2_x,
                    startFrame,
                    endFrame
    )

def getValueFromElName(el):
    idxEl, idxVal = getIndexAndValueFromElName(el)
    return int(idxVal)


def moveElementToDestinationZ(elId, destination_z, startFrame, endFrame):
    if SHOW_CODE_ANIMATION:
        element = bpy.data.objects[elId]
        source_z = element.location[2]
        delta = source_z - destination_z
        delta_abs = abs(delta)
        total_frames = endFrame - startFrame
        #print("START FRAME IS " + str(startFrame) + " END FRAME IS " + str(endFrame))
        element.keyframe_insert(data_path="location", frame = startFrame, index = -1 )
        if(total_frames > 0 ):
            distance_per_delta = delta / total_frames
            current_frame = startFrame

            #print("MOVING " + elId + "BY " + str(delta) + "IN " + str(total_frames) + "FRAMES")
            for i in range(int(total_frames)):
                loc = element.location[2] - 1 *  distance_per_delta
                #print("LOCATION IS "+ str(loc) + "DESTINATION WAS " + str(destination_z) )
                current_frame += 1
                element.location[2] = loc
                #print("CURRENT FRAME IS "+ str(current_frame))
                element.keyframe_insert(data_path="location", frame = current_frame, index = -1 )
                bpy.context.scene.frame_set(current_frame)

        element.location[2] = destination_z
        element.keyframe_insert(data_path="location", frame = endFrame, index = -1 )
        #current_frame += 1
        bpy.context.scene.frame_set(endFrame)
        return total_frames
    return 0


def moveElementToDestinationX(indexElId, destination_x, startFrame, endFrame):
    indexEl = bpy.data.objects[indexElId]
    source_x = indexEl.location[0]
    delta = source_x - destination_x
    delta_abs = abs(delta)
    total_frames = endFrame - startFrame
    indexEl.keyframe_insert(data_path="location", frame = startFrame, index = -1 )
    #print("TOTLA FRAMSE ARE ", str(total_frames))
    if(total_frames > 0):
        distance_per_delta = delta / total_frames
        current_frame = startFrame

        #print("MOVING " + indexElId + "BY " + str(delta) + "IN " + str(total_frames) + "FRAMES")
        for i in range(int(total_frames)):
            loc = indexEl.location[0] - 1 *  distance_per_delta
            #print("LOCATION IS "+ str(loc))
            current_frame += 1
            indexEl.location[0] = loc
            #print("CURRENT FRAME IS "+ str(current_frame))
            indexEl.keyframe_insert(data_path="location", frame = current_frame, index = -1 )
            bpy.context.scene.frame_set(current_frame)

    indexEl.location[0] = destination_x
    indexEl.keyframe_insert(data_path="location", frame = endFrame, index = -1 )
    #current_frame += 1
    bpy.context.scene.frame_set(endFrame)
    return total_frames


def moveIndexElement(indexElId, destination, startFrame, endFrame):
    #return 0
    destination_x = destination.location[0]
    return moveElementToDestinationX(
        indexElId,
        destination_x,
        startFrame,
        endFrame
    )

def moveIndex(sourceEl, destinationEl):
    global frame_num, FRAME_RATE
    source = bpy.data.objects[sourceEl]
    destination = bpy.data.objects[destinationEl]
    JTextIndex = bpy.data.objects['JText']

    source_x = source.location[0]
    destination_x = destination.location[0]

    delta = source_x - destination_x
    delta_abs = abs(delta)
    total_frames = delta_abs / UNIT_PER_FRAME
    distance_per_delta = delta / total_frames

    current_frame = frame_num

    #print('DELTA IS '+ str(delta))
    #print('DELTA ABS IS '+ str(delta_abs))
    #print('TOTAL FRAMES ARE ' + str(total_frames))
    #print('distance_per_delta ' + str(distance_per_delta))

    for i in range(int(total_frames)):
        JTextIndex.location[0] = JTextIndex.location[0] - 1 *  distance_per_delta
        JTextIndex.keyframe_insert(data_path="location", frame = current_frame + 1, index = -1 )
        current_frame += 1
        bpy.context.scene.frame_set(current_frame)

    JTextIndex.location[0] = destination_x
    JTextIndex.keyframe_insert(data_path="location", frame = current_frame + 1, index = -1 )
    current_frame += 1
    bpy.context.scene.frame_set(current_frame)

    return current_frame



def swapElementsWithAnimation(el_1, el_2, startFrame, endFrame, updateFrameNum = False):
    #return 0
    global frame_num, FRAME_RATE
    element_1 = bpy.data.objects[el_1]
    element_2 = bpy.data.objects[el_2]

    print("ELEMENT IDs are " + el_1 + " , " + el_2 )
    element_1_x = element_1.location[0]
    element_2_x = element_2.location[0]

    print("ELEMENT LOCATIONs are " + str(element_1_x) + " , " + str(element_2_x) )
    moveElementToDestinationX(
                    el_1,
                    element_2_x,
                    startFrame,
                    endFrame
    )
    return moveElementToDestinationX(
                    el_2,
                    element_1_x,
                    startFrame,
                    endFrame
    )

def get_random_color():
    ''' generate rgb using a list comprehension '''
    r, g, b = [random.random() for i in range(3)]
    return r, g, b, 1

def renderIndex():
    extreme_left = X_AxisReferencePosition - BASE_WIDTH/2
    i = 1
    TEXT_SIZE = 0.7
    JtextLeft = extreme_left + BLOCK_SIZE * (0.5)
    ItextLeft = extreme_left + BLOCK_SIZE * (i + 0.5)
    MintextLeft = extreme_left + BLOCK_SIZE * (0.5)
    text_dimension = (0.6, 0.6, 0.6)
    indexColor = (0.01,0.01,0.01,1)

    JPlusOneLeft = extreme_left + BLOCK_SIZE * (i+1.5)
    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(JtextLeft, -2, Z_AxisReferencePosition + -1.3), scale = text_dimension)
    Jtext = bpy.context.object
    Jtext.name = 'JText'
    Jtext.rotation_euler[0] = 1.5708
    Jtext.data.body = 'J'
    Jtext.data.size = TEXT_SIZE
    #Jtext.dimensions = text_dimension
    #bpy.ops.object.convert(target="MESH")
    Jtext.display.show_shadows = False
    setColor(Jtext, 'JText', indexColor)

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(ItextLeft, -2, Z_AxisReferencePosition + -0.7), scale=(0.6, 0.6, 0.6))
    KeyText = bpy.context.object
    KeyText.name = 'KeyText'
    KeyText.rotation_euler[0] = 1.5708
    KeyText.data.body = 'KEY'
    KeyText.data.size = TEXT_SIZE

    #bpy.ops.object.convert(target="MESH")
    KeyText.display.show_shadows = False
    KeyText.delta_location[0] = -0.3

    setColor(KeyText, 'KeyText', indexColor)

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(ItextLeft, -2, Z_AxisReferencePosition + -2.0), scale=(0.6, 0.6, 0.6))
    IText = bpy.context.object
    IText.name = 'IText'
    IText.rotation_euler[0] = 1.5708
    IText.data.body = 'I'
    IText.data.size = TEXT_SIZE

    #bpy.ops.object.convert(target="MESH")
    IText.display.show_shadows = False
    #IText.delta_location[0] = -0.3
    setColor(IText, 'IText', indexColor)


    return


def renderCode():
    text_dimension = (1,1,1)
    codeColor = (0.01,0.01,0.01,1)
    x_position = -16
    start_z_position = 8.5
    line_height = CODE_LINE_HEIGHT


    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, 0, start_z_position - 0 * line_height ),
    scale = text_dimension)
    line0 = bpy.context.object
    line0.name = 'line0'
    line0.data.body = 'for i in range(1, len(arr)):'
    line0.rotation_euler[0] = 1.5708
    line0.data.materials.append(ACTIVE_CODE_MATERIAL)
    line0.data.materials.append(INACTIVE_CODE_MATERIAL)
    line0.display.show_shadows = False
    #bpy.ops.object.convert(target="MESH")

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, 0, start_z_position - 1 * line_height ),
        scale = text_dimension
    )
    line1 = bpy.context.object
    line1.name = 'line1'
    line1.data.body = '   key = arr[i]'
    line1.rotation_euler[0] = 1.5708
    line1.data.materials.append(ACTIVE_CODE_MATERIAL)
    line1.data.materials.append(INACTIVE_CODE_MATERIAL)
    line1.display.show_shadows = False
    #bpy.ops.object.convert(target="MESH")

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, 0, start_z_position - 2 * line_height ),
        scale = text_dimension
    )
    line2 = bpy.context.object
    line2.name = 'line2'
    line2.data.body = '   j = i-1'
    line2.rotation_euler[0] = 1.5708
    line2.data.materials.append(ACTIVE_CODE_MATERIAL)
    line2.data.materials.append(INACTIVE_CODE_MATERIAL)
    line2.display.show_shadows = False
    #bpy.ops.object.convert(target="MESH")

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, 0, start_z_position - 3 * line_height ),
        scale = text_dimension
    )
    line3 = bpy.context.object
    line3.name = 'line3'
    line3.data.body = '   while j >= 0 and key < arr[j] :'
    line3.rotation_euler[0] = 1.5708
    line3.data.materials.append(ACTIVE_CODE_MATERIAL)
    line3.data.materials.append(INACTIVE_CODE_MATERIAL)
    line3.display.show_shadows = False
    #bpy.ops.object.convert(target="MESH")

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, 0, start_z_position - 4 * line_height ),
        scale = text_dimension
    )
    line4 = bpy.context.object
    line4.name = 'line4'
    line4.data.body = '      arr[j + 1] = arr[j]'
    line4.rotation_euler[0] = 1.5708
    line4.data.materials.append(ACTIVE_CODE_MATERIAL)
    line4.data.materials.append(INACTIVE_CODE_MATERIAL)
    line4.display.show_shadows = False
    #bpy.ops.object.convert(target="MESH")

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, 0, start_z_position - 5 * line_height ),
        scale = text_dimension
    )
    line5 = bpy.context.object
    line5.name = 'line5'
    line5.data.body = '      j -= 1'
    line5.rotation_euler[0] = 1.5708
    line5.data.materials.append(ACTIVE_CODE_MATERIAL)
    line5.data.materials.append(INACTIVE_CODE_MATERIAL)
    line5.display.show_shadows = False
    #bpy.ops.object.convert(target="MESH")

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, 0, start_z_position - 6 * line_height ),
        scale = text_dimension
    )
    line6 = bpy.context.object
    line6.name = 'line6'
    line6.data.body = '   arr[j + 1] = key'
    line6.rotation_euler[0] = 1.5708
    line6.data.materials.append(ACTIVE_CODE_MATERIAL)
    line6.data.materials.append(INACTIVE_CODE_MATERIAL)
    line6.display.show_shadows = False
    #bpy.ops.object.convert(target="MESH")

    renderCodeFrame()

    makeCodeActive('line0')
    #makeCodeActive('line1')

    return

def makeCodeActive(lineItemToActiveName):
    codeLineNameArray = [
        'line0',
        'line1',
        'line2',
        'line3', 'line4', 'line5', 'line6'
    ]
    for lineItemName in codeLineNameArray:
        lineitem = bpy.data.objects[lineItemName]
        lineitem.active_material  = INACTIVE_CODE_MATERIAL

    lineItemToActive = bpy.data.objects[lineItemToActiveName]
    lineItemToActive.active_material  = ACTIVE_CODE_MATERIAL
    return

def renderCodeFrame():
    frameLocation = (-11, 9, 10.3)
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        location=frameLocation,
        #rotate = (0, 90, 90)
        scale=(1, 1, 1)

    )
    codeFrame = bpy.context.object
    codeFrame.dimensions = (2,20,0)
    codeFrame.rotation_euler = (0, 1.5708 , 1.5708)
    codeFrame.name = 'codeFrame'

    material = bpy.data.materials.new('material_' + codeFrame.name)
    material.diffuse_color = (1, 1, 1, 0.1)
    #material.specular_hardness = 200
    codeFrame.data.materials.append(material)
    codeFrame.display.show_shadows = False
    registerHighlightCodeFrames( 'line0', frame_num, frame_num)
    moveElementToDestinationZ('codeFrame', 10.3, frame_num, frame_num)
    return


def animateString(scene):
    global frame_num
    current_frame  = scene.frame_current
    if current_frame in text_animation_map.keys():
        text_animate = text_animation_map.get(current_frame)
        JCounter = bpy.data.objects['JCounter']
        ICounter = bpy.data.objects['ICounter']
        print(text_animate)
        JCounter.data.body = text_animate['j']
        ICounter.data.body = text_animate['i']

    return

def highlightWatcher(scene):
    current_frame  = scene.frame_current
    allIWatcherFrames = list(i_watcher_frame_map.keys())
    for frameKey in allIWatcherFrames:
        startFrame = int(str(frameKey).split('_')[1])
        endFrame = int(str(frameKey).split('_')[3])
        if(startFrame <= current_frame and current_frame <= endFrame):
            frame = i_watcher_frame_map[frameKey]
            if(current_frame == endFrame):
                renderValueOnWatcher('Iwatcher', 'I = {0}'.format(frame['value']))
            break

    allJWatcherFrames = list(j_watcher_frame_map.keys())
    for frameKey in allJWatcherFrames:
        startFrame = int(str(frameKey).split('_')[1])
        endFrame = int(str(frameKey).split('_')[3])
        if(startFrame <= current_frame and current_frame <= endFrame):
            frame = j_watcher_frame_map[frameKey]
            if(current_frame == endFrame):
                renderValueOnWatcher('Jwatcher', 'J = {0}'.format(frame['value']))
            break

    allKeyWatcherFrames = list(key_watcher_frame_map.keys())
    for frameKey in allKeyWatcherFrames:
        startFrame = int(str(frameKey).split('_')[1])
        endFrame = int(str(frameKey).split('_')[3])
        if(startFrame <= current_frame and current_frame <= endFrame):
            frame = key_watcher_frame_map[frameKey]
            if(current_frame == endFrame):
                renderValueOnWatcher('Keywatcher', 'KEY={0}'.format(frame['value']))
            break

    allArrJWatcherFrames = list(arr_j_watcher_frame_map.keys())
    for frameKey in allArrJWatcherFrames:
        startFrame = int(str(frameKey).split('_')[1])
        endFrame = int(str(frameKey).split('_')[3])
        if(startFrame <= current_frame and current_frame <= endFrame):
            frame = arr_j_watcher_frame_map[frameKey]
            if(current_frame == endFrame):
                renderValueOnWatcher('ArrJwatcher', 'arr[J] = {0}'.format(frame['value']))
            break
    return

def highlishtFrameCode(scene):
    current_frame  = scene.frame_current
    allHighLightFrames = list(highlight_frame_map.keys())
    for frameKey in allHighLightFrames:
        startFrame = int(str(frameKey).split('_')[1])
        endFrame = int(str(frameKey).split('_')[3])

        if(startFrame <= current_frame and current_frame <= endFrame):
            frame = highlight_frame_map[frameKey]
            #print("MAKING " + frame['activeline'] + " ACTIVE")
            if(current_frame == endFrame):
                makeCodeActive(frame['activeline'])
            return
    return

def setValueToCounter(i, j):
    print("I is " + str(i))
    global frame_num
    text_animation_map[frame_num] = {
        'i': 'I={0}'.format(i),
        'j': 'J={0}'.format(j)
    }
    return





def renderCounter():
    extreme_left = 0 - BASE_WIDTH/2
    i = 0
    JtextLeft = extreme_left - 1.3
    counterColor = (0.5,0.8,0.1,1)
    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(JtextLeft, -2, 2), scale=(0.6, 0.6, 0.6))
    JCounter = bpy.context.object
    JCounter.name = 'JCounter'
    JCounter.rotation_euler[0] = 1.5708
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    setColor(JCounter, 'JCounter', counterColor)
    JCounter.data.size = 0.6

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(JtextLeft, -2, 4), scale=(0.6, 0.6, 0.6))
    ICounter = bpy.context.object
    ICounter.name = 'ICounter'
    ICounter.rotation_euler[0] = 1.5708
    #Itext.data.body = 'I=0'
    #bpy.ops.object.convert(target="MESH")
    setColor(ICounter, 'ICounter', counterColor)
    setValueToCounter(0,0)
    ICounter.data.size = 0.6
    return



def renderWatcher():
    global frame_num
    extreme_left = 0 - BASE_WIDTH/2
    watcherColor = WATCHER_COLOR
    x_position = 4
    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, -2, -5), scale=(0.6, 0.6, 0.6))
    Iwatcher = bpy.context.object
    Iwatcher.name = 'Iwatcher'
    Iwatcher.rotation_euler[0] = 1.5708
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    Iwatcher.display.show_shadows = False

    setColor(Iwatcher, 'Iwatcher', watcherColor)
    #Iwatcher.data.size = 0.6
    registerIWatcherFrame(0, frame_num, frame_num)

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, -2, -8), scale=(0.6, 0.6, 0.6))
    Jwatcher = bpy.context.object
    Jwatcher.name = 'Jwatcher'
    Jwatcher.rotation_euler[0] = 1.5708
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    Jwatcher.display.show_shadows = False
    setColor(Jwatcher, 'Jwatcher', watcherColor)
    registerJWatcherFrame('', frame_num, frame_num)

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position + 4, -2, -8), scale=(0.6, 0.6, 0.6))
    Keywatcher = bpy.context.object
    Keywatcher.name = 'Keywatcher'
    Keywatcher.rotation_euler[0] = 1.5708
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    Keywatcher.display.show_shadows = False
    setColor(Keywatcher, 'Keywatcher', watcherColor)
    registerKeyWatcherFrame('', frame_num, frame_num)

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position + 4, -2, -5),
        scale=(0.6, 0.6, 0.6))
    ArrJwatcher = bpy.context.object
    ArrJwatcher.name = 'ArrJwatcher'
    ArrJwatcher.rotation_euler[0] = 1.5708
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    ArrJwatcher.display.show_shadows = False
    setColor(ArrJwatcher, 'ArrJwatcher', watcherColor)
    registerArrjWatcherFrame('', frame_num, frame_num)

    #ArrJwatcher
    return

def renderValueOnWatcher(watcherId, value):
    watcher = bpy.data.objects[watcherId]
    watcher.data.body = value

def mapChartElWithArray(arr):
    # map(lambda (i,x): {'name':x, 'rank':i}, enumerate(ranked_users))
    arrToReturn = []
    for i, val in enumerate(arr):
        arrToReturn.append(getElName(i, val))
    return arrToReturn
    #return map(getElName, enumerate(arr))
    #return map( lambda(i,x): getElName(i,x), enumerate(arr))




def run():
    clearObject()
    # clearAllMaterial()
    # return
    createMaterials()
    mapColorToValues()
    renderChart()
    renderIndex()
    #return
    if SHOW_CODE_ANIMATION:
        renderCode()
        renderWatcher()
    #return
    if animateString in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(animateString)

    if highlightWatcher in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(highlightWatcher)
    if highlishtFrameCode in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(highlishtFrameCode)

    if(SHOW_CODE_ANIMATION):
        bpy.app.handlers.frame_change_pre.append(highlishtFrameCode)
        bpy.app.handlers.frame_change_pre.append(highlightWatcher)

    mappedChartWithArray = mapChartElWithArray(UNSORTED_ARRAY)
    for els in mappedChartWithArray:
        element = bpy.data.objects[els]
        element.keyframe_insert(data_path="location", frame = frame_num, index = -1 )

    insertionSort(mappedChartWithArray)
    print(frame_num)
    return

run()






