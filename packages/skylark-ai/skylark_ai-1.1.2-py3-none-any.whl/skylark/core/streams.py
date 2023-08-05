import cv2
import time
import asyncio
import math
import threading
import json
from skylark.core.clients import RealTimeClient


class StreamClient:
	def __init__(self, fps, batch_size, sampling_rate, service, show_stream, token):
		self.fps = fps
		self.frames = []
		self.json = ""
		self.syncid = -1
		self.batch_size = batch_size
		self.sampling_rate = sampling_rate
		self.sample_length = int(fps / sampling_rate)
		self.delay_sec = 1 / self.fps
		self.show_stream = show_stream
		self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		self.service = service
		self.token = token
		self.client = RealTimeClient(service, self.on_receive, batch_size, self.on_network_status_change, token)
		self.response_jsons = []
		self.createTasks()

	def createTasks(self):
		# running these three tasks on a seperate thread so that the main thread does'nt gets blocked
		tasks = [
			asyncio.ensure_future(self.start_stream()),
			asyncio.ensure_future(self.client.receive_message()),
			asyncio.ensure_future(self.show_stream()),
		]
		mythread = threading.Thread(target=self.run_tasks, args=(asyncio.get_event_loop(), tasks))
		mythread.setDaemon(True)
		mythread.start()

	async def on_network_status_change(self):
		# method to restart tasks stopped if some network issue occurs and websocket connection gets closed
		print("re-running tasks")
		await self.client.re_connect()
		await asyncio.sleep(1)
	
	def stop_tasks(self):
		print("###########################do something to stop here###################################")

	def run_tasks(self, loop, tasks):
		# runs the tasks sent as a list here
		asyncio.set_event_loop(loop)
		loop.run_until_complete(asyncio.wait(tasks))

	def on_receive(self, json):
		try:
			# whenever a message is received we store them in a list
			if "results" in json and self.frames.__len__() > 0:
				self.response_jsons.append(json)
				print(len(self.response_jsons))
				print("results there in response hence appended")
			else:
				print(json)

		except Exception as e:
			print(str(e))

	async def start_stream(self):
		# variable used to maintain the count of frames already sampled
		counter = 0
		while True:
			try:
				print("inside start stream")
				start = time.time()
				ret, frame = self.vid.read()
				cv2.imshow('inputstream', frame)
				self.frames.append(frame)
				# print(self.frames.__len__())
				# for every frames equal to sample_length picking one frame from the middle and sending for processing
				counter = (counter + 1) % self.sample_length
				if counter == 0:
					# print("len:")
					# print(self.frames.__len__())
					selected_frame = self.frames[-self.sample_length:][
						-int(math.floor(math.floor(self.sample_length / 2)))]
					# scale_percent = 72 # percent of original size
					# width = int(selected_frame.shape[1] * scale_percent / 100)
					# height = int(selected_frame.shape[0] * scale_percent / 100)
					# dim = (width, height)
					#
					# resized_image = cv2.resize(selected_frame, dim)
					if selected_frame is not None:
						byte_array = cv2.imencode('.jpg', selected_frame)[1].tostring()
						await self.client.start_stream(byte_array)
				time_spent = time.time() - start
				rem_time = max(self.delay_sec - time_spent, 0)
				await asyncio.sleep(rem_time)
				# if q is pressed we stop showing output stream
				if cv2.waitKey(1) & 0xFF == ord('q'):
					self.vid.release()
					cv2.destroyAllWindows()
					break
			except Exception as e:
				print(str(e))
