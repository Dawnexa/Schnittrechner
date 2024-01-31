# Schnittrechner 
This Python script calculates the average of grades from a PDF file. It is specifically designed for collective certificates from the University of Vienna. (More universities in progress)


## Requirements

- Python 3.*
- The Python libraries `os`, `numpy`, `fitz`, `re`, and `PyQt` must be installed.

## Installation

To install the required libraries, run the following command:

```console
pip3 install numpy PyMuPDF PyQt6
```

## Usage

Run the [Schnittrechner.py](Rechner/src/Schnittrechner.py) script. A window will open where you can select the PDF files. After selecting the files, click on the "Calculate" button. The PDF file should be in the "Data" folder and the grades and ECTS points should be indicated in the format "Grade (decimal number) ECTS".

The script reads the PDF file, extracts the grades and ECTS points, and calculates the weighted av



## Lizenz

This project is licensed under the MIT License. This means you are free to use, modify, and distribute it as long as you comply with the terms of the license. A copy of the license can be found in the LICENSE file in this repository.

Please note that this project is provided without any warranty. The authors are not responsible for any damages or losses that could arise from using the project.

A copy of the license can be found [here](LICENSE).

