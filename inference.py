import chainer
from chainer import computational_graph
from chainer import cuda
from chainer import optimizers
from chainer import serializers
import numpy as np
import argparse
import net
import imgproc
from PIL import Image

model = net.SRCNN()
optimizer = optimizers.MomentumSGD(lr=0.01, momentum=0.9)
optimizer.setup(model)

serializers.load_npz('srcnn.model', model)
serializers.load_npz('srcnn.state', optimizer)

img = Image.open('./dog.jpg')
image = img.resize((2*img.size[0], 2*img.size[1]), resample=Image.NEAREST)

x_data = np.asarray(image).transpose(2, 0, 1).astype(np.float32)
print(x_data.shape)

blocks = imgproc.makePatch(x_data, 64, 52)

lst = []
for i in range(0, blocks.shape[0]):
    block = blocks[i]
    block = np.reshape(block, (1,) + block.shape)
    x = chainer.Variable(block)
    y = model(x)
    lst.append(y.data[0])

h_blocks = x_data.shape[1]/52 + (0 if x_data.shape[1] % 52 == 0 else 1) 
w_blocks = x_data.shape[2]/52 + (0 if x_data.shape[2] % 52 == 0 else 1)
print("h=%d w=%d"%(h_blocks, w_blocks))
y_data = np.asarray(lst)
cnt = 0
result_data = np.zeros((3, h_blocks*52, w_blocks*52))
for i in range(0, x_data.shape[1], 52):
#    if i+64 > x_data.shape[1]:
#        continue
    for j in range(0, x_data.shape[2], 52):
#        if j+64 > x_data.shape[2]:
#            continue
        #print("i=%d h=%d"%(i, j))
        result_data[:, i:i+52, j:j+52] = y_data[cnt]
        cnt += 1
           
result_data[result_data<0] = 0
result_data[result_data>1] = 1
result_data *= 255
result_data = result_data[:, 0:x_data.shape[1], 0:x_data.shape[2]]
result_image = Image.fromarray(np.uint8(result_data).transpose(1, 2, 0))
result_image.save('result.jpg')            
