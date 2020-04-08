# aws
## extend volume
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html
lsblk
sudo growpart /dev/nvme1n1 1
lsblk
df -h
sudo resize2fs /dev/nvme1n1p1 
df -h

# prerequisites
https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/prerequisites.md

## cuda10
https://developer.nvidia.com/cuda-downloads
sudo sh cuda_10.2.89_440.33.01_linux.run --silent

## cuDNN7.5
https://developer.nvidia.com/cudnn
https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html

$ tar -xzvf cudnn-10.2-linux-x64-v7.6.5.32.tgz
$ sudo cp cuda/include/cudnn.h /usr/local/cuda/include
$ sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
$ sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*

## test pytorch
https://pytorch.org/get-started/locally/
https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#sphx-glr-beginner-blitz-cifar10-tutorial-py

## install cmake-gui from source
https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/prerequisites.md
## The imported target “Qt5::Gui” references the file “/usr/lib/x86_64-linux-gnu/libGL.so” but this file does not exist. [closed] pay attention to libGL.so or libEGL.so
https://askubuntu.com/questions/616065/the-imported-target-qt5gui-references-the-file-usr-lib-x86-64-linux-gnu-li
## others
https://codeyarns.com/2019/03/20/caffe-cuda_cublas_device_library-error/
https://anglehit.com/how-to-install-the-latest-version-of-cmake-via-command-line/

## install other packages
/data/git-clones/openpose-staf/scripts/ubuntu/install_deps.sh

# install openpose
https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md#openpose-configuration

