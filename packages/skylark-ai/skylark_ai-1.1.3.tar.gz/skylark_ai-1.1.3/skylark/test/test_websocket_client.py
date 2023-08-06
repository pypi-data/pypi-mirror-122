
import sys


sys.path.append('C:/Users/jrish/work/python-sdk/skylark_ai')
# print(sys.path)

from skylark.core.clients import Service
from skylark.core.face_mask_stream import FaceMaskStreamClient
from skylark.core.face_detect_stream import FaceDetectStreamClient
from skylark.core.weapon_detection_stream import WeaponDetectionStreamClient
from skylark.core.facial_landmark_stream import FacialLandmarkStream
from skylark.core.lie_detection_stream import LieDetectionStreamClient
from skylark.core.night_day_stream import NightDayStreamClient
import time
from skylark.utils.utils import is_connected




# user will add authorization token here
token = "e22a8efa08231e851a5b8b8de45fff9eefc53d4b8ad59ded636fa8bcdcf0713a"

# user will send fps of incoming stream, size of batch that will be formed while processing ,
# the rate at which sampling is done, and the token
c = FaceMaskStreamClient(
	fps=5,
	batch_size=1,
	sampling_rate=1,
	token=token,
	show_processed_stream=True,
	save_raw_frames=True,
	scale_percent=70,
	quality=40,
)


# user can continue to perform any further tasks as per need
try:
	i=0
	while True:
			print("in main")
			print(is_connected())
			print(str(len(c.frames)))
			time.sleep(1)

except KeyboardInterrupt:
	print("exiting")
	exit()
	
