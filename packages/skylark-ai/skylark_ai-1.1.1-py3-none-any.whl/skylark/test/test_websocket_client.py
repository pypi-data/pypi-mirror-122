
import sys


sys.path.append('C:/Users/jrish/work/python-sdk/skylark_ai/skylark')
print(sys.path)

from core.clients import Service
from core.face_mask_stream import FaceMaskStreamClient
from core.face_detect_stream import FaceDetectStreamClient
from core.weapon_detection_stream import WeaponDetectionStreamClient
from core.facial_landmark_stream import FacialLandmarkStream
from core.lie_detection_stream import LieDetectionStreamClient
from core.night_day_stream import NightDayStreamClient
import time




# user will add authorization token here
token = "e22a8efa08231e851a5b8b8de45fff9eefc53d4b8ad59ded636fa8bcdcf0713a"

# user will send fps of incoming stream, size of batch that will be formed while processing ,
# the rate at which sampling is done, and the token
c = FaceMaskStreamClient(
	fps=2,
	batch_size=1,
	sampling_rate=1,
	token=token
)

# user can continue to perform any further tasks as per need
try:

	i=0
	while True:
			time.sleep(1)

except KeyboardInterrupt:
	print("exiting")
	exit()
	
