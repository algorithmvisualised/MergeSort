import bpy, sys
import numpy as np
import random


from constants import *
from colors import COLOR_MAP as color_map
#from merge import moveCodeFrameToLine


def getXPositionBasedUponIndex(index):
    extreme_left = X_AxisReferencePosition - BASE_WIDTH/2
    return extreme_left + BLOCK_SIZE * (index + 0.5)


def getElName(i, val):
    txt = ELEMENT_STRING
    return txt.format(i, val)

def setColorToElementFromMap(obj, obj_id, val):
    global color_map
    material = setColor(obj, obj_id, color_map.get(val))
    #material.metallic = 0.1
    return material

def setColor(obj, obj_id, color):
    material = bpy.data.materials.new('material_' + obj_id)
    material.diffuse_color = color
    #material.specular_hardness = 200
    obj.data.materials.append(material)
    return material

def createElements(arr):
    #extreme_left = X_AxisReferencePosition - BASE_WIDTH/2
    for i, val in enumerate(arr):
        #print("POSITION WOULD BE" + str(extreme_left + BLOCK_SIZE * (i+0.5)))
        element_location = (getXPositionBasedUponIndex(i) , 0, Z_AxisReferencePosition + val/2)
        element_scale = (BLOCK_SIZE, BASE_DEPTH, val)
        #print("ELEMENT SCALE WOULD BE")
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

def clearObject():
    for ob in bpy.context.scene.objects:
        print(ob.type)
    objs = [ob for ob in bpy.context.scene.objects if ob.type in ('MESH', 'FONT')]
    bpy.ops.object.delete({"selected_objects": objs})
    return

def mapChartElWithArray(arr):
    arrToReturn = []
    for i, val in enumerate(arr):
        arrToReturn.append(getElName(i, val))
    return arrToReturn


def getObjFromId(id):
    return bpy.data.objects[id]


def moveElementToDestinationX(indexElId, destination_x, startFrame, endFrame):
    indexEl = bpy.data.objects[indexElId]
    source_x = indexEl.location[0]
    delta = source_x - destination_x
    delta_abs = abs(delta)
    #print("Moving element {0} from {1} to {2}. Delta would be {3} from {4} frame to {5} frame".format(indexElId, source_x, destination_x, delta, startFrame, endFrame))
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
    #print("Moving element {0} from {1} to {2}. Delta would be {3}".format(indexElId, source_x, destination_x, delta))
    indexEl.keyframe_insert(data_path="location", frame = endFrame, index = -1 )
    #current_frame += 1
    bpy.context.scene.frame_set(endFrame)
    return total_frames



CODE_LINE_HEIGHT = 0.8
TEXT_SIZE = 0.8

def renderCode():


    #codeColor = ( 0.01, 0.01, 0.01, 1)
    x_position = -16
    start_z_position = 6
    line_height = CODE_LINE_HEIGHT


    for lineIndex in range(0, 23):
        renderLine('line{}'.format(lineIndex), (x_position, 0, start_z_position - lineIndex * line_height)   )
    #return
    renderCodeFrame()
    #makeCodeActive('line0')
    #makeCodeActive('line1')

    return

def renderWatcher():
    #global frame_num
    #extreme_left = 0 - BASE_WIDTH/2
    watcherColor = WATCHER_COLOR
    x_position = -2
    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, -2, 5))
    Arrwatcher = bpy.context.object
    Arrwatcher.name = 'Arrwatcher'
    Arrwatcher.rotation_euler[0] = 1.5708
    Arrwatcher.data.size = TEXT_SIZE
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    Arrwatcher.display.show_shadows = False

    setColor(Arrwatcher, 'Iwatcher', watcherColor)

    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, -2, 4))
    Levelwatcher = bpy.context.object
    Levelwatcher.name = 'Levelwatcher'
    Levelwatcher.rotation_euler[0] = 1.5708
    Levelwatcher.data.size = TEXT_SIZE
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    Levelwatcher.display.show_shadows = False

    setColor(Levelwatcher, 'Levelwatcher', watcherColor)

    return
    bpy.ops.object.text_add(
        enter_editmode=False,
        location=(x_position, -2, 3))
    OriginalArrayWatcher = bpy.context.object
    OriginalArrayWatcher.name = 'OriginalArrayWatcher'
    OriginalArrayWatcher.rotation_euler[0] = 1.5708
    OriginalArrayWatcher.data.size = TEXT_SIZE
    #Jtext.data.body = 'J=0'
    #bpy.ops.object.convert(target="MESH")
    OriginalArrayWatcher.display.show_shadows = False

    setColor(OriginalArrayWatcher, 'OriginalArrayWatcher', watcherColor)




    #Iwatcher.data.size = 0.6
    #registerIWatcherFrame(0, frame_num, frame_num)
    return


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

def makeCodeActive(lineItemToActiveName):
    codeLineNameArray = []
    for lineIndex in range(0, 23):
        codeLineNameArray.append('line{}'.format(lineIndex))

    for lineItemName in codeLineNameArray:
        lineitem = bpy.data.objects[lineItemName]
        lineitem.active_material  = INACTIVE_CODE_MATERIAL

    lineItemToActive = bpy.data.objects[lineItemToActiveName]
    lineItemToActive.active_material  = ACTIVE_CODE_MATERIAL
    return

def renderLine(lineKey, location):
    text_dimension = (0.1, 0.1, 0.1)
    bpy.ops.object.text_add(
        enter_editmode=False,
        location= location,
        scale = text_dimension
    )
    line = bpy.context.object
    line.name = lineKey
    line.data.body = getCode()[lineKey]
    line.data.size = TEXT_SIZE
    line.rotation_euler[0] = 1.5708
    #line.data.materials.append(ACTIVE_CODE_MATERIAL)
    line.data.materials.append(INACTIVE_CODE_MATERIAL)
    line.display.show_shadows = False

    return

def getCode():
    objToReturn =  {
        'line0' :'if len(arr) > 1:',
        'line1' :'   mid = len(arr)//2',
        'line2' :'   L = arr[:mid]',
        'line3' :'   R = arr[mid:]',
        'line4' :'   mergeSort(L)',
        'line5' :'   mergeSort(R)',
        'line6' :'   i = j = k = 0',
        'line7' :'   while i < len(L) and j < len(R):',
        'line8' :'       if L[i] < R[j]:',
        'line9' :'          arr[k] = L[i]',
        'line10':'          i += 1',
        'line11':'        else:',
        'line12':'          arr[k] = R[j]',
        'line13':'          j += 1',
        'line14':'        k += 1',
        'line15':'   while i < len(L):',
        'line16':'       arr[k] = L[i]',
        'line17':'       i += 1',
        'line18':'       k += 1',
        'line19':'   while j < len(R):',
        'line20':'       arr[k] = R[j]',
        'line21':'       j += 1',
        'line22':'       k += 1'
    }
    return objToReturn

def getAllCodeFrameZLocation():
    objectToReturn = {
        'line0' : 7.8,
        'line1' : 6.85,
        'line2' : 5.95,
        'line3' : 5.0,
        'line4' : 3.9,
        'line5' : 3.0,
        'line6' : 2.1,
        'line7' : 1.2,
        'line8' : 0.3,
        'line9' : -0.65,
        'line10': -1.5,
        'line11': -2.6,
        'line12': -3.7,
        'line13': -4.6,
        'line14': -5.5,
        'line15': -6.5,
        'line16': -7.4,
        'line17': -8.3,
        'line18': -9.2,
        'line19': -10.2,
        'line20': -11.1,
        'line21': -12,
        'line22': -12.95
    }
    return objectToReturn



def renderCodeFrame():
    frameLocation = (-12, 9, 7.8)
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        location=frameLocation,
        #rotate = (0, 90, 90)
        scale=(0.45, 7.5, 1)

    )
    codeFrame = bpy.context.object
    codeFrame.dimensions = (0.9, 15, 0)
    codeFrame.rotation_euler = (0, 1.5708 , 1.5708)
    codeFrame.name = 'codeFrame'

    material = bpy.data.materials.new('material_' + codeFrame.name)
    material.diffuse_color = (1, 1, 1, 0.1)
    #material.specular_hardness = 200
    codeFrame.data.materials.append(material)
    codeFrame.display.show_shadows = False
    #registerHighlightCodeFrames( 'line0', frame_num, frame_num)
    #moveCodeFrameToLine('line0', 0)
    return



INACTIVE_CODE_COLOR = (1, 0.05, 0.16, 1)
INACTIVE_CODE_MATERIAL_NAME = 'material_inactive_code'

ACTIVE_CODE_COLOR = (0, 0, 1, 1)
ACTIVE_CODE_MATERIAL_NAME = 'material_active_code'

INACTIVE_CODE_MATERIAL = False
ACTIVE_CODE_MATERIAL = False

def createMaterials():
    global INACTIVE_CODE_MATERIAL, ACTIVE_CODE_MATERIAL

    INACTIVE_CODE_MATERIAL = bpy.data.materials.new(INACTIVE_CODE_MATERIAL_NAME)
    INACTIVE_CODE_MATERIAL.diffuse_color = INACTIVE_CODE_COLOR

    ACTIVE_CODE_MATERIAL = bpy.data.materials.new(ACTIVE_CODE_MATERIAL_NAME)
    ACTIVE_CODE_MATERIAL.diffuse_color = ACTIVE_CODE_COLOR

    return

def clearAllMaterial():
    #return
    for material in bpy.data.materials:
        #material.user_clear()
        bpy.data.materials.remove(material)
    return