# MIT License
#
# Copyright (c) 2023 Dechin CHEN
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
os.environ['GLOG_v'] = '4'
from mindspore import Tensor, nn, ops
from mindspore import numpy as msnp

class Quaternion(nn.Cell):
    """ Quaternion object based on MindSpore.
    Args:
        q(Tensor): The input Tensor to construct a quaternion.
    """
    def __init__(self, q):
        super().__init__()
        if q.shape[-1] not in [4, 3, 1]:
            raise ValueError("The defined quaternion at least 4 elements should be given but got {}.".format(
                q.shape[-1]))
        if len(q.shape) == 1:
            q = q[None, :]
        if q.shape[-1] == 4:
            self.s = q[:, 0][:, None]
            self.v = q[:, 1:]
        elif q.shape[-1] == 1:
            self.s = q[:, 0][:, None]
            self.v = msnp.zeros((q.shape[0], 3))
        else:
            self.s = msnp.zeros((q.shape[0], 1))
            self.v = q[:, 0:]

    def __str__(self):
        return str(msnp.hstack((self.s, self.v)).asnumpy())

    def __abs__(self):
        q = msnp.hstack((self.s, self.v))
        return q.norm(axis=-1)

    def __len__(self):
        return self.s.shape[0]

    def __add__(self, other):
        q = msnp.hstack((self.s, self.v))
        oq = msnp.hstack((other.s, other.v))
        return Quaternion(q + oq)

    def _get_mul(self, other):
        s = self.s * other.s
        d = msnp.dot(self.v[:, None, :], other.v[:, :, None]).reshape(s.shape)
        s -= d
        v = msnp.zeros_like(self.v)
        v += self.s * other.v
        v += self.v * other.s
        v += msnp.cross(self.v, other.v, axisc=-1)
        q = msnp.hstack((s, v))
        return Quaternion(q)

    def __mul__(self, other):
        q = msnp.hstack((self.s, self.v))
        if isinstance(other, Tensor):
            if other.size == 1:
                return Quaternion(q * other)
            elif other.size == q.shape[0]:
                if len(other.shape) == 1:
                    other = other[:, None]
                return Quaternion(q * other)
            elif other.shape[-1] == 3:
                if len(other.shape) == 1:
                    other = other[None, :]
                zeros = msnp.zeros((other.shape[0], 1))
                other = msnp.hstack((zeros, other))
                return self._get_mul(Quaternion(other))
        else:
            try:
                return self._get_mul(other)
            except:
                raise ValueError("The input object is not a Quaternion.")

    def to_tensor(self, quater=None):
        if quater is not None:
            q = msnp.hstack((quater.s, quater.v))
        else:
            q = msnp.hstack((self.s, self.v))
        return q

    def rotate(self, other):
        return self.to_tensor(self.__mul__(other))[:, 1:]