import imgproc
import glob
import os
from PIL import Image
import numpy as np

#lst = []
#lstc = []
#filelst = glob.glob('./jpegdata/*')
#for f in filelst:
#        imgdata = np.asarray(Image.open(f)).transpose(2, 0, 1).astype(np.float32)
#        train_tmp = imgproc.makePatch(imgdata, 64, 52)
#        train_tmp, expect_tmp = imgproc.cropPatch(train_tmp, 52)
#        lst.extend(train_tmp)
#        lstc.extend(expect_tmp)

#train = np.asarray(lst)
#expect = np.asarray(lstc)
#print(train.shape)
#print(expect.shape)
#np.save('train.npy', train)
#np.save('expect.npy', expect)

train = np.load('train.npy')
expect = np.load('expect.npy')

img = Image.fromarray(((train[0].transpose(1, 2, 0))*255).astype(np.uint8))
img2 = Image.fromarray(((expect[0].transpose(1, 2, 0))*255).astype(np.uint8))
img.show()
img2.show()

