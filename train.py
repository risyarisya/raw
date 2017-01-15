import chainer
from chainer import computational_graph
from chainer import cuda
from chainer import optimizers
from chainer import serializers
import numpy as np
import argparse
import net

parser = argparse.ArgumentParser(description='Chainer example: MNIST')
parser.add_argument('--initmodel', '-m', default='',
                    help='Initialize the model from given file')
parser.add_argument('--resume', '-r', default='',
                    help='Resume the optimization from snapshot')
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
parser.add_argument('--epoch', '-e', default=100, type=int,
                    help='number of epochs to learn')
parser.add_argument('--batchsize', '-b', type=int, default=100,
                    help='learning minibatch size')
parser.add_argument('--test', action='store_true',
                    help='Use tiny datasets for quick tests')

args = parser.parse_args()

batchsize = args.batchsize
n_epoch = args.epoch


train = np.load('train.npy').astype(np.float32)
expect = np.load('expect.npy').astype(np.float32)

x_train = train[0:100]
x_expect= expect[0:100]
N=30

model = net.SRCNN()
optimizer = optimizers.MomentumSGD(lr=0.01, momentum=0.9)
optimizer.setup(model)
print(train.dtype)
if args.initmodel:
    print('load model from', args.initmodel)
    serializers.load_npz(args.initmodel, model)
if args.resume:
    print('load optimizer state from', args.resume)
    serializers.load_npz(args.reusme, optimizer)

for epoch in range(1, n_epoch+1):
    print('epoch', epoch)

    perm = np.random.permutation(N)
    sum_loss = 0
    for i in range(0, N, batchsize):
        x = chainer.Variable(x_train[perm[i:i+batchsize]])
        t = chainer.Variable(x_expect[perm[i:i+batchsize]])
        optimizer.update(model.get_loss_func(), x, t)
        sum_loss += float(model.loss.data) * len(x.data)
    print('train mean loss={}'.format(sum_loss/N))
    optimizer.lr *= 0.97

serializers.save_npz('srcnn.model', model)
serializers.save_npz('srcnn.state', optimizer)

