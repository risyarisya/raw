import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math
import glob
import skimage.io
import skimage.transform

def loadRawDataFromFile(filename, width, height, chNum):	
	img = np.fromfile(filename, dtype=np.uint8)
	if chNum==0:
		print("error!")
		return false;
	img.shape = (height, width, chNum)
	result = img.transpose(2, 0, 1).astype(np.float32)
	return result

def makePatch(data, block_size, output_size):
	data /= 255
	block_offset = (block_size - output_size) / 2
	h_blocks = int(math.floor(data.shape[1]/output_size)) + (0 if data.shape[1] % output_size == 0 else 1)
	w_blocks = int(math.floor(data.shape[2]/output_size)) + (0 if data.shape[2] % output_size == 0 else 1)
	h = block_offset + h_blocks * output_size + block_offset
	w = block_offset + w_blocks * output_size + block_offset
	pad_top = block_offset
	pad_left = block_offset
	pad_bottom = (h - block_offset) - data.shape[1]
	pad_right = (w - block_offset) - data.shape[2]
	data = np.pad(data, ((0, 0), (pad_top, pad_bottom), (pad_left, pad_right)), 'edge')

	lst = []
	for i in range(0, data.shape[1], output_size):
		if i + block_size > data.shape[1]:
			continue
		for j in range(0, data.shape[2], output_size):
			if j + block_size > data.shape[2]:
				continue
			block = data[:, i:(i+block_size), j:(j+block_size)]
			lst.append(block)
	result = np.asarray(lst)
	return result 

def cropPatch(data, output_size):
        lstc = []
	lst = []
	offset = (data.shape[2] - output_size) / 2
        for i in range(0, data.shape[0]):
                tmp = data[i]
                ctmp = tmp[:, offset:offset+output_size, offset:offset+output_size]
		tmp = tmp.transpose(1, 2, 0)
		tmp = skimage.transform.rescale(tmp, 0.5)
		tmp = skimage.transform.rescale(tmp, 2.)
                lstc.append(ctmp)
		lst.append(tmp.transpose(2, 0, 1))
        #result = np.asarray(lst)
        return lst, lstc

