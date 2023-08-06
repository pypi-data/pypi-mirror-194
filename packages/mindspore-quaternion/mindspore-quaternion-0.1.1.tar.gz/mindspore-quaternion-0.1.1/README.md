# mindspore-quaternion--基于MindSpore深度学习框架的四元数数据结构
![](https://img.shields.io/pypi/l/mindspore-quaternion)

四元数在自动化等领域有非常广泛的应用，其必要性在于解决了使用欧拉角旋转的过程中有可能出现的欧拉角死锁问题。
关于更多的四元数的原理和计算方法，可以阅读本readme末尾的参考博客。

## 安装与更新
本软件支持pip一键安装与更新：
```bash
$ python3 -m pip install mindspore-quaternion --upgrade
```
也可以使用源码进行安装：
```bash
$ git clone https://gitee.com/dechin/mindspore-quaternion.git
$ cd mindspore-quaternion
$ python3 setup.py install
```

## 定义四元数
详细的代码可以参考[该链接](https://gitee.com/dechin/mindspore-quaternion/tree/master/examples)下的内容，这里我们只作为简单介绍。首先我们需要import一些必要的软件包：
```python
from quaternion import Quaternion
import numpy as np
import mindspore as ms
from mindspore import Tensor
```
接下来我们可以看一下各个不同shape的四元数定义。首先是定义一个常数的四元数，其实也就是`[s, 0, 0, 0]`这样的一个四元数：
```python
element = Tensor([0.], ms.float32)
element_quaternion = Quaternion(element)
print ('The type of element is: {}'.format(type(element_quaternion)))
print ('The value of element is: {}'.format(element_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of element is: <class 'quaternion.Quaternion'>
The value of element is: [[0. 0. 0. 0.]]
```
还可以定义三维矢量所对应的四元数，是如同`[0, vx, vy, vz]`这样的形式：
```python
vector = Tensor(np.arange(3), ms.float32)
vector_quaternion = Quaternion(vector)
print('The type of vector is: {}'.format(type(vector_quaternion)))
print('The value of vector is: {}'.format(vector_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of vector is: <class 'quaternion.Quaternion'>
The value of vector is: [[0. 0. 1. 2.]]
```
当然，如果一开始我们就定义好了一个完整的四维的四元数`[s, vx, vy, vz]`，那么也是可以用来直接构造一个四元数对象的：
```python
quater = Tensor(np.arange(4), ms.float32)
quater_quaternion = Quaternion(quater)
print('The type of quater is: {}'.format(type(quater_quaternion)))
print('The value of quater is: {}'.format(quater_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of quater is: <class 'quaternion.Quaternion'>
The value of quater is: [[0. 1. 2. 3.]]
```
这里必须要提一个最重要的point，那就是当我们使用一个深度学习框架去实现四元数这样的数据结构的时候，我们当然更多的是考虑到GPU加速在多batch的四元数计算
下的性能优势。所以这里我们也可以去定义一个更高维度的，多batch的四元数：
```python
batch_quater = Tensor(np.arange(16).reshape((4, 4)), ms.float32)
batch_quater_quaternion = Quaternion(batch_quater)
print('The type of batch_quater is: {}'.format(type(batch_quater_quaternion)))
print('The value of batch_quater is: {}'.format(batch_quater_quaternion.to_tensor()))
```
上述代码的执行结果为：
```bash
The type of batch_quater is: <class 'quaternion.Quaternion'>
The value of batch_quater is: [[ 0.  1.  2.  3.]
                               [ 4.  5.  6.  7.]
                               [ 8.  9. 10. 11.]
                               [12. 13. 14. 15.]]
```

## 四元数运算

## 参考博客
1. https://www.cnblogs.com/dechinphy/p/quaternion-calc.html
