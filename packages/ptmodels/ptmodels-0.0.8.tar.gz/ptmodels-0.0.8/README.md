
<h1 align="center">
  <br>
  <a href="https://rafsunsheikh.github.io/Web"><img src="https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.png" alt="Markdownify" width="200"></a>
  <br>
  ptmodels
  <br>
</h1>

<h4 align="center">ptmodels uses pre-trained models to evaluate image datasets and helps to understand which model works better.<a href="http://electron.atom.io" target="_blank">Electron</a>.</h4>

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

![screenshot](https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.gif)

## Installation

* Install ptmodels by simply use the snippet into the terminal
```bash
pip install ptmodels
```
## How To Use

To clone and run this application, use git clone on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/rafsunsheikh/ptmodels

# Go into the repository
$ cd ptmodels

# Install dependencies
$ npm install

# Run the app
$ npm start
```

> **Note**
> If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.


## Classification

```bash
from ptmodels.Classifier import PreTrainedModels
from tensorflow.keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

model = PreTrainedModels(NUM_CLASSES=10, BATCH_SIZE=32, EPOCHS=2, LEARNING_RATE=0.001, MOMENTUM=0.9)
df = model.fit(x_train, y_train, x_test, y_test)
print(df)
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

<a href="https://www.buymeacoffee.com/5Zn8Xh3l9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/amitmerchant">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## You may also like...

- [Pomolectron](https://github.com/amitmerchant1990/pomolectron) - A pomodoro app
- [Correo](https://github.com/amitmerchant1990/correo) - A menubar/taskbar Gmail App for Windows and macOS

## License

MIT

---

> [rafsunsheikh.github.io/Web](https://rafsunsheikh.github.io/Web) &nbsp;&middot;&nbsp;
> GitHub [@rafsunsheikh](https://github.com/rafsunsheikh) &nbsp;&middot;&nbsp;
> Twitter [@RafsunSheikh](https://twitter.com/RafsunSheikh) &nbsp;&middot;&nbsp;
> LinkedIn [@md-rafsun-sheikh](https://www.linkedin.com/in/md-rafsun-sheikh-b3898882/)

