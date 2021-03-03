
import numpy as np
BLOCK_SIZE = 0.2
MOVING_SIZE = BLOCK_SIZE
SHOW_CODE_ANIMATION = False
BASE_DEPTH = COLUMN_DEPTH = 1

if SHOW_CODE_ANIMATION:
    X_AxisReferencePosition = 6
    Z_AxisReferencePosition = -10
else:
    X_AxisReferencePosition = -0
    Z_AxisReferencePosition = -7



if SHOW_CODE_ANIMATION:
    TOTAL_NUMBERS = 20
    UNSORTED_ARRAY = [8, 3, 1, 6, 4, 2, 9, 5 ]
    UNSORTED_ARRAY =  np.random.randint(low = 1, high = 15 , size=TOTAL_NUMBERS)
    #UNSORTED_ARRAY =  np.random.randint(low = 1, high = 10, size=TOTAL_NUMBERS)
    print(UNSORTED_ARRAY)

else:
    TOTAL_NUMBERS = 340
    UNSORTED_ARRAY =  np.random.randint(low = 1, high = 40 , size=TOTAL_NUMBERS)
    #UNSORTED_ARRAY = [5, 3, 6, 1, 9, 3, 4, 8, 2, 7]
    print(UNSORTED_ARRAY)


TOTAL_BLOCKS = len(UNSORTED_ARRAY)
BASE_WIDTH = TOTAL_BLOCKS * BLOCK_SIZE

ELEMENT_STRING = 'element_{0}_value_{1}'
FRAME_RATE = 1
FRAME_RATE_MULTIPLIER = 1
PAUSE_FRAME = FRAME_RATE * FRAME_RATE_MULTIPLIER
WATCHER_COLOR = (0.748, 0.159, 0.568, 1)