import boto3
import time
from moviepy.editor import *
from pseyepy import Camera, Display, Stream
from pyaxidraw import axidraw


BUCKET_NAME = 'plotguydatastore'
TABLE = 'plotguy_v0'
AD = axidraw.AxiDraw()

S3 = boto3.client(
	's3',
	aws_access_key_id=ACCESS_KEY,
	aws_secret_access_key=SECRET_KEY
)

DB = boto3.client(
	'dynamodb',
	aws_access_key_id=ACCESS_KEY,
	aws_secret_access_key=SECRET_KEY,
	region_name='us-west-1')


class Cam:
	def __init__(self):
		self.camera = Camera()

	def startRecording(self):
		self.s = Stream(self.camera, file_name = self.file_name)

	def stopRecording(self):
		self.s.end()
		self.camera.end()

	def convertToGif(self):
		clip = VideoFileClip(f"{self.file_name}_0.avi")
		clip.write_gif(f"{self.file_name}.gif")
		return f"{self.file_name}.gif"


def queryDynamo():
	return DB.query(
		TableName = TABLE,
		IndexName = 'completed-index',
		ExpressionAttributeValues = {
			':v1': {
				'N': '0'
			},
		},
		KeyConditionExpression='completed = :v1',
	)


def updateDynamo(drawing):
	DB.update_item(TableName = TABLE, 
		Key = {
			'email': drawing['email'],
		},
		UpdateExpression="SET completed= :var1",
		ExpressionAttributeValues={
			':var1': {'N': '1'},
		}
	)


def getNextDrawing():
	response = queryDynamo()
	drawings = response.get('Items')

	if len(drawings) > 0:
		drawing = drawings[0]
		updateDynamo(drawing)
		return drawing

	return None
	

def scan():
	drawing = getNextDrawing()

	if drawing:
		S3.download_file(BUCKET_NAME, 
		                 drawing['filepath']['S'], 
		                 drawing['filepath']['S']
		                )
		return drawing['filepath']['S']

	return None


def draw():
	file = scan()

	if file:
		try:
			ad.plot_setup(file)
			cam = Cam(file_name = file.split('.')[0])

			cam.startRecording()
			ad.plot_run()   # plot the document
			cam.stopRecording()

			gif = cam.convertToGif()
			S3.upload_file(gif, BUCKET_NAME, gif)

		except:
			print('broke at some point')


if __name__ == '__main__':

	while True:
		draw()
		time.sleep(2)