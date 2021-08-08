# Breast Imaging Reporting & Data System (BIRADS)
###### This project was an image processing computer science assignment. All repository content/files are for educational purposes only.

_The Breast Imaging Report and Data System (BIRADS) of the American College of Radiology (ACR) is today largely used in most of the countries where breast cancer screening is implemented. It is a tool defined to reduce variability between radiologists when creating the reports in mammography, ultrasonography or MRI._

This BIRADS Classifier with GUI was made using Python and image processing, machine learning libraries. It trains the SVM with Haralick Features and Co-occurrence Matrix based on the chosen user parameters. It can classify the first 4 BIRADS categories (1-4).

### Features
* Graphical Interface
* Image Visualizer
* Image Processing (Crop, Quantization, Equalization)
* Classifier Parameters Selector

![Screenshot](/static/screenshot.PNG)

### Requirements (Python 3.8+)
* Pillow
* Tkinter
* Numpy
* SkImage
* SkLearn

**Usage**: _py app.py_
