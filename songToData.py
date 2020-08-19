# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os
from PIL import Image
import eyed3

from sliceSpectrogram import createSlicesFromSpectrograms
from sliceSpectrogram import createSlicesFromSpectrograms_predict
from audioFilesTools import isMono, getGenre
from config import rawDataPath
from config import spectrogramsPath
from config import pixelPerSecond

from config import rawDataPath_predict
from config import spectrogramsPath_predict


#Tweakable parameters
desiredSize = 128

#Define
currentPath = os.path.dirname(os.path.realpath(__file__))

#Remove logs
eyed3.log.setLevel("ERROR")

#Create spectrogram from mp3 files
def createSpectrogram(filename, newFilename):
	#Create temporary mono track if needed
	if isMono(rawDataPath+filename):
		command = "cp '{}' '/tmp/{}.mp3'".format(rawDataPath+filename, newFilename)
	else:
		command = "sox '{}' '/tmp/{}.mp3' remix 1,2".format(
			rawDataPath+filename, newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print(errors)

	#Create spectrogram
	filename.replace(".mp3", "")
	command = "sox '/tmp/{}.mp3' -n spectrogram -Y 200 -X {} -m -r -o '{}.png'".format(newFilename, pixelPerSecond, spectrogramsPath+newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print(errors)

	#Remove tmp mono track
	if os.path.exists("/tmp/{}.mp3".format(newFilename)):
		os.remove("/tmp/{}.mp3".format(newFilename))

def createSpectrogram_predict(filename, newFilename):
	#Create temporary mono track if needed
	if isMono(rawDataPath_predict+filename):
		command = "cp '{}' '/tmp/{}.mp3'".format(rawDataPath_predict+filename, newFilename)
	else:
		command = "sox '{}' '/tmp/{}.mp3' remix 1,2".format(
			rawDataPath_predict+filename, newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print(errors)

	#Create spectrogram
	filename.replace(".mp3", "")
	command = "sox '/tmp/{}.mp3' -n spectrogram -Y 200 -X {} -m -r -o '{}.png'".format(newFilename, pixelPerSecond, spectrogramsPath_predict+newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print(errors)

	#Remove tmp mono track
	if os.path.exists("/tmp/{}.mp3".format(newFilename)):
		os.remove("/tmp/{}.mp3".format(newFilename))

#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio():
	genresID = dict()
	files = os.listdir(rawDataPath)
	files = [file for file in files if file.endswith(".mp3")]
	nbFiles = len(files)

	#Create path if not existing
	if not os.path.exists(os.path.dirname(spectrogramsPath)):
		try:
			os.makedirs(os.path.dirname(spectrogramsPath))
		except OSError as exc:  # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	
	#Rename files according to genre
	tmp_genres = ['Hip-Hop', 'Ballad', 'Korean', 'Pop', 'Dance', 'Soul', 'Rock', 'R&B']
	for index, filename in enumerate(files):
		print(index, filename)
		print("Creating spectrogram for file {}/{}...".format(index+1, nbFiles))
		try:
			fileGenre = getGenre(rawDataPath+filename).decode('ASCII')
			check_idx = fileGenre.replace(" ", "").split('/')
			for i in check_idx:
				if i in tmp_genres:
					fileGenre = i
				elif fileGenre not in tmp_genres:
					fileGenre = 'Etc'

		except Exception as err:
			print(err)
			continue

		print("Genre: ", fileGenre)
		genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
		fileID = genresID[fileGenre]
		newFilename = fileGenre+"_"+str(fileID)
		createSpectrogram(filename, newFilename)

#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio_predict():
	# genresID = dict()
	files = os.listdir(rawDataPath_predict)
	files = [file for file in files if file.endswith(".mp3")]
	nbFiles = len(files)

	#Create path if not existing
	if not os.path.exists(os.path.dirname(spectrogramsPath_predict)):
		try:
			os.makedirs(os.path.dirname(spectrogramsPath_predict))
		except OSError as exc:  # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	
	for index, filename in enumerate(files):
		print(index, filename)
		createSpectrogram_predict(filename, '_predict')

def createSlicesFromAudio():
	print("Creating spectrograms...")
	createSpectrogramsFromAudio()
	print("Spectrograms created!")
	print("Creating slices...")
	createSlicesFromSpectrograms(desiredSize)
	print("Slices created!")


def createSlicesFromAudio_predict():
	print("Creating spectrograms...")
	createSpectrogramsFromAudio_predict()
	print("Spectrograms created!")
	print("Creating slices...")
	createSlicesFromSpectrograms_predict(desiredSize)
	print("Slices created!")
