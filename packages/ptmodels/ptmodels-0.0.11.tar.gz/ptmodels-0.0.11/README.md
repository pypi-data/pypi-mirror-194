
<h1 align="center">
  <br>
  <a href="https://rafsunsheikh.github.io/Web"><img src="https://github.com/rafsunsheikh/ptmodels/blob/master/image_sources/logo_hi.png" alt="ptmodels" width="200"></a>
  <br>
  ptmodels
  <br>
</h1>

<h4 align="center">ptmodels uses pre-trained models to evaluate image datasets and helps to understand which model works better.<a href="https://pypi.org/project/ptmodels/" target="_blank">ptmodels</a>.</h4>

<p align="center">
  <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://badge.fury.io/js/electron-markdownify.svg"
         alt="Gitter">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify"><img src="https://badges.gitter.im/amitmerchant1990/electron-markdownify.svg"></a>
  <a href="https://saythanks.io/to/bullredeyes@gmail.com">
      <img src="https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg">
  </a>
  <a href="https://www.paypal.me/AmitMerchant">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#classification">Classification</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

![screenshot](https://github.com/rafsunsheikh/ptmodels/blob/master/image_sources/evaluation_01.png)

## Installation


* Install ptmodels by simply using the snippet into the terminal
```bash
pip install ptmodels
```
## How To Use
- Open up Kaggle Notebook or Google Colab.
- Choose runtime with GPU support. (as the models are very large, it will be difficult to run it on your local machine and also without GPU.)
- Install ptmodels in one cell.
```
!pip install ptmodels
```
- Run the cell by pressing shift + enter
- In another cell run the following.

```bash
from ptmodels.Classifier import PreTrainedModels
from tensorflow.keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

model = PreTrainedModels(NUM_CLASSES=10, BATCH_SIZE=32, EPOCHS=2, LEARNING_RATE=0.001, MOMENTUM=0.9)
df = model.fit(x_train, y_train, x_test, y_test)
print(df)
```
- You can initialize the PreTrainedModels class without any arguments.
- Default values for the parameters are:
> NUM_CLASSES = 2
> BATCH_SIZE  = 32
> EPOCHS = 1
> LEARNING_RATE = 1e-4
> MOMENTUM = 0.9 	
- You can also consuly my [Google Colab Notebook](https://colab.research.google.com/drive/19BJ0LAQrqTEZiMqRAXZDZH5dhgwQeRI_?usp=sharing)


## Classification
![screenshot](https://github.com/rafsunsheikh/ptmodels/blob/master/image_sources/evaluation_02.png)

```bash

Starting Training: VGG16
1563/1563 [==============================] - 24s 10ms/step - loss: 0.2274 - accuracy: 0.5063
1563/1563 [==============================] - 11s 7ms/step
313/313 [==============================] - 2s 7ms/step
appended successfully

Starting Training: VGG19
1563/1563 [==============================] - 19s 11ms/step - loss: 0.2313 - accuracy: 0.4969
1563/1563 [==============================] - 14s 9ms/step
313/313 [==============================] - 3s 9ms/step
appended successfully

Starting Training: ResNet50
1563/1563 [==============================] - 27s 14ms/step - loss: 0.2331 - accuracy: 0.4970
1563/1563 [==============================] - 18s 10ms/step
313/313 [==============================] - 4s 12ms/step
appended successfully

Starting Training: ResNet50V2
1563/1563 [==============================] - 26s 14ms/step - loss: 0.2843 - accuracy: 0.3291
1563/1563 [==============================] - 17s 10ms/step
313/313 [==============================] - 3s 10ms/step
appended successfully

Starting Training: ResNet101
1563/1563 [==============================] - 43s 23ms/step - loss: 0.2363 - accuracy: 0.4896
1563/1563 [==============================] - 31s 18ms/step
313/313 [==============================] - 6s 20ms/step
appended successfully

Starting Training: ResNet101V2
1563/1563 [==============================] - 43s 22ms/step - loss: 0.2923 - accuracy: 0.3033
1563/1563 [==============================] - 30s 18ms/step
313/313 [==============================] - 6s 19ms/step
appended successfully

Starting Training: ResNet152
1563/1563 [==============================] - 61s 32ms/step - loss: 0.2327 - accuracy: 0.5006
1563/1563 [==============================] - 44s 26ms/step
313/313 [==============================] - 9s 28ms/step
appended successfully

Starting Training: ResNet152V2
1563/1563 [==============================] - 62s 33ms/step - loss: 0.2959 - accuracy: 0.3003
1563/1563 [==============================] - 44s 26ms/step
313/313 [==============================] - 9s 27ms/step
appended successfully

Starting Training: MobileNet
1563/1563 [==============================] - 14s 8ms/step - loss: 0.3206 - accuracy: 0.1784
1563/1563 [==============================] - 8s 5ms/step
313/313 [==============================] - 2s 5ms/step
appended successfully

Starting Training: MobileNetV2
1563/1563 [==============================] - 20s 11ms/step - loss: 0.3165 - accuracy: 0.1961
1563/1563 [==============================] - 13s 8ms/step
313/313 [==============================] - 2s 7ms/step
appended successfully

Starting Training: DenseNet121
1563/1563 [==============================] - 42s 21ms/step - loss: 0.2424 - accuracy: 0.4628
1563/1563 [==============================] - 30s 18ms/step
313/313 [==============================] - 6s 19ms/step
appended successfully

Starting Training: DenseNet169
1563/1563 [==============================] - 55s 28ms/step - loss: 0.2432 - accuracy: 0.4567
1563/1563 [==============================] - 41s 24ms/step
313/313 [==============================] - 7s 23ms/step
appended successfully

Starting Training: EfficientNetV2B1
1563/1563 [==============================] - 33s 14ms/step - loss: 0.2233 - accuracy: 0.5198
1563/1563 [==============================] - 28s 17ms/step
313/313 [==============================] - 5s 15ms/step
appended successfully

Starting Training: EfficientNetV2B2
1563/1563 [==============================] - 35s 15ms/step - loss: 0.2279 - accuracy: 0.5117
1563/1563 [==============================] - 29s 17ms/step
313/313 [==============================] - 5s 16ms/step
appended successfully

Starting Training: EfficientNetV2B3
1563/1563 [==============================] - 39s 17ms/step - loss: 0.2584 - accuracy: 0.4208
1563/1563 [==============================] - 34s 20ms/step
313/313 [==============================] - 6s 19ms/step
appended successfully

Starting Training: EfficientNetV2S
1563/1563 [==============================] - 47s 20ms/step - loss: 0.2455 - accuracy: 0.4598
1563/1563 [==============================] - 43s 25ms/step
313/313 [==============================] - 7s 24ms/step
appended successfully

Starting Training: EfficientNetV2M
1563/1563 [==============================] - 66s 28ms/step - loss: 0.3221 - accuracy: 0.2315
1563/1563 [==============================] - 60s 35ms/step
313/313 [==============================] - 11s 35ms/step
appended successfully

Starting Training: EfficientNetV2L
1563/1563 [==============================] - 95s 40ms/step - loss: 0.2644 - accuracy: 0.4007
1563/1563 [==============================] - 83s 48ms/step
313/313 [==============================] - 15s 48ms/step
appended successfully

Starting Training: ConvNeXtTiny
1563/1563 [==============================] - 60s 30ms/step - loss: 0.1644 - accuracy: 0.6741
1563/1563 [==============================] - 45s 27ms/step
313/313 [==============================] - 9s 27ms/step
appended successfully

Starting Training: ConvNeXtSmall
1563/1563 [==============================] - 103s 53ms/step - loss: 0.1573 - accuracy: 0.6885
1563/1563 [==============================] - 83s 49ms/step
313/313 [==============================] - 16s 50ms/step
appended successfully

Starting Training: ConvNeXtBase
1563/1563 [==============================] - 105s 54ms/step - loss: 0.1435 - accuracy: 0.7221
1563/1563 [==============================] - 83s 50ms/step
313/313 [==============================] - 15s 48ms/step
appended successfully

Starting Training: ConvNeXtLarge
1563/1563 [==============================] - 117s 62ms/step - loss: 0.1237 - accuracy: 0.7662
1563/1563 [==============================] - 91s 55ms/step
313/313 [==============================] - 18s 58ms/step
appended successfully

Starting Training: ConvNeXtXLarge
1563/1563 [==============================] - 129s 69ms/step - loss: 0.1178 - accuracy: 0.7845
1563/1563 [==============================] - 104s 63ms/step
313/313 [==============================] - 20s 64ms/step
appended successfully

              Models Accuracy train Precision train Recall train  \
0              VGG16          0.621           0.621        0.621   
1              VGG19          0.602           0.602        0.602   
2           ResNet50          0.622           0.622        0.622   
3         ResNet50V2          0.412           0.412        0.412   
4          ResNet101          0.614           0.614        0.614   
5        ResNet101V2          0.386           0.386        0.386   
6          ResNet152          0.622           0.622        0.622   
7        ResNet152V2          0.379           0.379        0.379   
8          MobileNet          0.205           0.205        0.205   
9        MobileNetV2          0.234           0.234        0.234   
10       DenseNet121          0.578           0.578        0.578   
11       DenseNet169          0.557           0.557        0.557   
12  EfficientNetV2B1          0.652           0.652        0.652   
13  EfficientNetV2B2          0.641           0.641        0.641   
14  EfficientNetV2B3          0.593           0.593        0.593   
15   EfficientNetV2S          0.610           0.610        0.610   
16   EfficientNetV2M          0.384           0.384        0.384   
17   EfficientNetV2L          0.561           0.561        0.561   
18      ConvNeXtTiny          0.776           0.776        0.776   
19     ConvNeXtSmall          0.786           0.786        0.786   
20      ConvNeXtBase          0.815           0.815        0.815   
21     ConvNeXtLarge          0.855           0.855        0.855   
22    ConvNeXtXLarge          0.863           0.863        0.863   

   f1_score train Accuracy test Precision test Recall test f1_score test  
0           0.621         0.595          0.595       0.595         0.595  
1           0.602         0.585          0.585       0.585         0.585  
2           0.622         0.594          0.594       0.594         0.594  
3           0.412         0.397          0.397       0.397         0.397  
4           0.614         0.578          0.578       0.578         0.578  
5           0.386         0.382          0.382       0.382         0.382  
6           0.622         0.590          0.590       0.590         0.590  
7           0.379         0.367          0.367       0.367         0.367  
8           0.205         0.201          0.201       0.201         0.201  
9           0.234         0.230          0.230       0.230         0.230  
10          0.578         0.553          0.553       0.553         0.553  
11          0.557         0.539          0.539       0.539         0.539  
12          0.652         0.631          0.631       0.631         0.631  
13          0.641         0.630          0.630       0.630         0.630  
14          0.593         0.583          0.583       0.583         0.583  
15          0.610         0.601          0.601       0.601         0.601  
16          0.384         0.381          0.381       0.381         0.381  
17          0.561         0.547          0.547       0.547         0.547  
18          0.776         0.740          0.740       0.740         0.740  
19          0.786         0.759          0.759       0.759         0.759  
20          0.815         0.785          0.785       0.785         0.785  
21          0.855         0.829          0.829       0.829         0.829  
22          0.863         0.831          0.831       0.831         0.831  
```

## Credits

This software uses the following open source packages:

- [Tensorflow](https://tensorflow.org/)
- [Keras](https://keras.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)
- [highlight.js](https://highlightjs.org/)

## Related

[LazyPredict](https://github.com/shankarpandala/lazypredict) - Classification using basic models

## Support

<a href="https://www.buymeacoffee.com/rafsunSheikh" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/LevDropStudio">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## You may also like...

- [Signature Fraud Detection](https://github.com/rafsunsheikh/signatureFraud) - A Django app to detect signature fraud from Bank checks.
- [AIST](https://github.com/rafsunsheikh/IDP_AIST) - Artificial Intelligence Surveillance Tower
- [Parliament Bhaban](https://github.com/rafsunsheikh/openGL_project) - A fun OpenGL project for 2D animation.
- [Mancala](https://github.com/rafsunsheikh/mancala_repo) - A simple AI Mancala game built in Python

## License

MIT

---

> [rafsunsheikh.github.io/Web](https://rafsunsheikh.github.io/Web) &nbsp;&middot;&nbsp;
> GitHub [@rafsunsheikh](https://github.com/rafsunsheikh) &nbsp;&middot;&nbsp;
> Twitter [@RafsunSheikh](https://twitter.com/RafsunSheikh) &nbsp;&middot;&nbsp;
> LinkedIn [@md-rafsun-sheikh](https://www.linkedin.com/in/md-rafsun-sheikh-b3898882/)

