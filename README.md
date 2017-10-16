
# CS676A: Computer Vision and Image Processing

Project: Pedestrian Detection using R-CNN
Instructor: Prof. Vinay P. Namboodiri
TA: Samrath Patidar

### Members-
    1. Deepak Kumar (12228)
    2. Mohit Singh Solanki (12419)

### PAPERS FOLLOWED
    1. Geoffrey E. Hinton Alex Krizhevsky, Ilya Sutskever. Imagenet classification with deep convolutional neural networks. NIPS, 2012.
    2. Ross Girshick. Fast r-cnn. In International Conference on Computer Vision (ICCV), 2015.
    3. Ross Girshick, Jeff Donahue, Trevor Darrell, and Jitendra Malik. Rich feature hierarchies for accurate object detection and semantic segmentation. In Computer Vision and Pattern Recognition, 2014.
    4. Gevers2 J.R.R. Uijlings, van de Sande and A.W.M. Smeulders2. Selective search for object recognition. ICCV, 2011.
    5. Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. Faster R-CNN: Towards real-time object detection with region proposal networks. In Advances in Neural Information Processing Systems (NIPS), 2015.

### PLATFORM SPECS 
EC2 Linux Instance on Amazon Web Service

    1. OS - Ubuntu 14.04
    2. GPU - 1x NVIDIA GRID (Kepler G104) + 8 x hardware hyperthreads from Intel Xeon E5-2670
    3. Memory - 15GB
    4. HardDisk - 90GB SSD
    Refer to AWS documentation on creation of EC2 linux instance and setup




### INSTALLATION STEPS
    1. Login to your AWS instance
    2. Install OpenCV as described in this blog: http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/ (Ignore the step-8. We don't want to install virtualenv. Also ignore all commands that have virtualenv usage in them)
    3. Install CAFFE as described in this blog: https://github.com/BVLC/caffe/wiki/Install-Caffe-on-EC2-from-scratch-(Ubuntu,-CUDA-7,-cuDNN)
    Note:
        - Don't forget to do "make pycaffe" at the end
        - Edit the Makefile.config and change 'WITH_PYTHON_LAYER := 1'
    4. Download the changed fast-rcnn files from the my github: ```git clone --recursive  https://github.com/kumardeepakr3/fast-rcnn```
    5. Download INRIA dataset.
    6. Install vnc4server (Matlab installation needs Display)
    7. Install Matlab on Linux Instance. (We used Matlab 2012. You know how to do it :p )



### TRAINING

    1. For training we use the images under the train/pos/ directory.
    2. Organise the train data as follows:
    3. /home/ubuntu/INRIA
				|-- data
					|-- Annotations
						|-- *.txt (Annotation Files)
					|-- Images
						|-- *.png (Image Files)
					|-- ImageSets
						|-- train.txt
    4. The train.txt contains all the names(without extensions) of images files that will be used for training.
        For Eg:
	crop_000011
	crop_000603
	crop_000606
	crop_000607
	crop_000608

    5. Construct IMDB
	- cd $FRCNN_ROOT/lib/datasets
	- Edit the file inria.py and set self._classes [Do nothing if using git cloned from my repo]
	- Create your own annotation function like _load_inria_annotation in inria.py. [Do nothing if using git cloned from my repo]
	- Add 'import inria' to the files [Do nothing if using git cloned from my repo]
	- Edit factory.py and set inria_devkit_path to point to the /home/ubuntu/INRIA directory.

    6. Run Selective Search
	- cd $FRCNN_ROOT/selective_search
	- Edit selective_search.m and add image_db = 'home/ubuntu/INRIA/'[Do nothing if using git cloned from my repo]
	- Change the last line to
	selective_search_rcnn(image_filenames, 'train.mat');
	- Run this matlab code
	- This generates train.mat [Takes around 15min for this]
	- Place it in /home/ubuntu/INRIA

    7. Modify Prototxt
	- Edit train.prototxt in $FRCNN_ROOT/models/VGG_CNN_M_1024.
	- Set num_classes to C [In INRIA data C=2, i.e. Pedestrian and Background]
	- Set num_output in the cls_score layer to C
	- Set num_output in the bbox_pred layer to 4 * C

    8. Run the followin g in $FRCNN_ROOT/
	./tools/train_net.py --gpu 0 --solver models/VGG_CNN_M_1024/solver.prototxt \
    --weights data/imagenet_models/VGG_CNN_M_1024.v2.caffemodel --imdb inria_train

    9. This creates the trained model in $FRCNN_ROOT/output/models folder



### TESTING
    1. Delete the contents in the INRIA folder created during training.
    2. Create New set of directories in the following way:
       /home/ubuntu/INRIA
			|-- data
				|-- Annotations
					|-- *.txt (Annotation Files)
				|-- Images
					|-- *.png (Image Files)
				|-- ImageSets
					|-- test.txt
			|-- results
				|-- test (Empty Directory)
			|-- VOCcode
    3. The test.txt contains all the names(without extensions) of images files that will be used for training.
    For example:
	crop_000001
	crop_000002
	crop_000003
	crop_000004
	crop_000005
    4. Copy the files from $FRCNN_ROOT/help/INRIA/VOCcode to the /home/ubuntu/INRIA/VOCcode folder.
    5. Run Selective Search again. (Rename the output to test.mat)
    6. Place the test.mat file in /home/ubuntu/INRIA folder
    7. Modify Prototxt
	- Edit test.prototxt in $FRCNN_ROOT/models/VGG_CNN_M_1024.
	- Set num_output in the cls_score layer to C [In INRIA data C=2, i.e. Pedestrian and Background]
	- Set num_output in the bbox_pred layer to 4 * C
    8. Run in $FRCNN_ROOT/ directory:
	./tools/test_net.py --gpu 0 --def models/VGG_CNN_M_1024/test.prototxt \
    --net output/default/train/vgg_cnn_m_1024_fast_rcnn_iter_40000.caffemodel --imdb inria_test




### VIEW YOUR RESULTS
    1. Look for the file in INRIA/results/test directory. This file has info about the bounding box in each image along with the probability with which it detects it as person
    2. Edit the file cvPlotBox.py:
	- Set fileName variable to the above file
	- Set imagePath to /home/ubuntu/INRIA/data/Images/
	- Set OutPath to the folder where you want to extract your resultant images with box around detected persons.



