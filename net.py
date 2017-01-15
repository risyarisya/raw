import chainer
import chainer.functions as F
import chainer.links as L

class SRCNN(chainer.Chain):
    insize = 64
    outputisze = 52

    def __init__(self):
        super(SRCNN, self).__init__(
            conv1=F.Convolution2D(3, 64, 9),
            conv2=F.Convolution2D(64, 32, 1),
            conv3=F.Convolution2D(32, 3, 5),
        )

    def __call__(self, x):
        return self.forward(x)

    def forward(self, x):
        h = F.relu(self.conv1(x))
        h = F.relu(self.conv2(h))
        h = F.relu(self.conv3(h))
        return h

    def get_loss_func(self, train=True):
        def lf(x, t):
            h = self.forward(x)
            loss = F.mean_squared_error(h, t)
            self.loss = loss
            return self.loss
        return lf

