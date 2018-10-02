import boto3
import time
from moviepy.editor import *
from pseyepy import Camera, Display, Stream
from pyaxidraw import axidraw

BUCKET_NAME = 'plotguydatastore'
TABLE = 'plotguy_v0'

ad = axidraw.AxiDraw()

def getNextDrawing():

	db_client = boto3.client(
		'dynamodb',
		aws_access_key_id=ACCESS_KEY,
		aws_secret_access_key=SECRET_KEY,
		region_name='us-west-1')

	response = db_client.query(
		TableName = TABLE,
		IndexName = 'completed-index',
		ExpressionAttributeValues = {
			':v1': {
				'N': '0'
			},
		},
		KeyConditionExpression='completed = :v1',
	)

	drawings = response.get('Items')

	if len(drawings) > 0:
		drawing = drawings[0]
		#db_client.delete_item(TableName = 'plotguy_v1', Item=drawing)
		#drawing['completed']['N'] = '1'
		db_client.update_item(TableName = TABLE, 
			Key = {
				'email': drawing['email'],
			},
			UpdateExpression="SET completed= :var1",
			ExpressionAttributeValues={
				':var1': {'N': '1'},
			}
		)
		return drawing
	else:
		print("No items")

	return None
	

def scan():

	drawing = getNextDrawing()

	if drawing:

		s3_client = boto3.client(
			's3',
			aws_access_key_id=ACCESS_KEY,
			aws_secret_access_key=SECRET_KEY
		)

		s3_client.download_file(BUCKET_NAME, drawing['filepath']['S'], drawing['filepath']['S'])

		return drawing['filepath']['S']
	return None

def draw():

	file = scan()

	if file:
		try:
			ad.plot_setup(file)
			ad.options.speed_pendown = 50 # Set maximum  pen-down speed to 50%
			ad.plot_run()   # plot the document
		except:
			print('broke at some point')



if __name__ == '__main__':

	while True:
		draw()
		time.sleep(2)



