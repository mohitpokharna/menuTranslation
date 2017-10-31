# MenuTranslation #

A common problem that we encounter when visiting restaurants in foreign places is unfamiliarity with the names on the menu. Therefore, in this project we would like to address this problem by presenting a translated name of the dish along with the image of the dish for better visual understanding of the menu which most certainly will lead to much better experiences.

## What is this repository for? ##

* The aim of this project is to make menu cards with English descriptions understandable for Hindi speaking people
* Version: 0.1.3


## Getting Started

### Prerequisites
[kivy](https://kivy.org/docs/installation/installation-linux.html) - Application framework  
[opencv](https://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html) - For image preprocessing  
[tesseract](https://www.howtoforge.com/tutorial/tesseract-ocr-installation-and-usage-on-ubuntu-16-04/) - For text extraction 


## Built With ##
NOTE: Above code has been tested on Ubuntu 16.04, Python 2.7.11, kivy 1.9.1, opencv 2.4.11


## Contribution guidelines ##

* TASKS involved:  
 01: Collect sample menu from restaurants  
 02: Preprocess all the images (resize, align, denoise, binarize, etc)  
 03: Extract menu items (text)  
 04: Prepare a database (projectdb.sqlite) with menu items, hindi conversions and menu images  
 05: Display new menu with original background and converted texts in place of english menu items. It currently displays the dish image and converted dish name in Hindi.  
 06: Desktop version which takes image as input  
 07: Android version (currently apk can be build using buildozer). Future versions would involve running the apk on android device.  


## Versioning ##
We use [SemVer](http://semver.org/) for versioning.


## Acknowledgements

* [Font and Background Color Independent Text Binarization](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.359.7875&rep=rep1&type=pdf)
