# Import Pillow:
from PIL import Image
import os.path

from config import spectrogramsPath, slicesPath
from config import spectrogramsPath_predict, slicesPath_predict

#Slices all spectrograms
def createSlicesFromSpectrograms(desiredSize):
	for filename in os.listdir(spectrogramsPath):
		if filename.endswith(".png"):
			sliceSpectrogram(filename,desiredSize)

def createSlicesFromSpectrograms_predict(desiredSize):
	for filename in os.listdir(spectrogramsPath_predict):
		if filename.endswith(".png"):
			sliceSpectrogram_predict(filename,desiredSize)

#Creates slices from spectrogram
#TODO Improvement - Make sure we don't miss the end of the song
def sliceSpectrogram(filename, desiredSize):
	genre = filename.split("_")[0] 	#Ex. Dubstep_19.png

	# Load the full spectrogram
	img = Image.open(spectrogramsPath+filename)

	#Compute approximate number of 128x128 samples
	width, height = img.size
	nbSamples = int(width/desiredSize)
	width - desiredSize

	#Create path if not existing
	slicePath = slicesPath+"{}/".format(genre)
	if not os.path.exists(os.path.dirname(slicePath)):
		try:
			os.makedirs(os.path.dirname(slicePath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#For each sample
	for i in range(nbSamples):
		print("Creating slice: ", (i+1), "/", nbSamples, "for", filename)
		#Extract and save 128x128 sample
		startPixel = i*desiredSize
		imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
		imgTmp.save(slicesPath+"{}/{}_{}.png".format(genre,filename[:-4],i))

def sliceSpectrogram_predict(filename, desiredSize):
	genre = filename.split("_")[0] 	#Ex. Dubstep_19.png

	# Load the full spectrogram
	img = Image.open(spectrogramsPath_predict+filename)

	#Compute approximate number of 128x128 samples
	width, height = img.size
	nbSamples = int(width/desiredSize)
	width - desiredSize

	genre = 'predict'
	#Create path if not existing
	slicePath = slicesPath_predict+"{}/".format(genre)
	if not os.path.exists(os.path.dirname(slicePath)):
		try:
			os.makedirs(os.path.dirname(slicePath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#For each sample
	for i in range(nbSamples):
		print("Creating slice: ", (i+1), "/", nbSamples, "for", filename)
		#Extract and save 128x128 sample
		startPixel = i*desiredSize
		imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
		imgTmp.save(slicesPath_predict+"{}/{}_{}.png".format(genre,filename[:-4],i))

