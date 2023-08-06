# OKNPATCH PYTHON PACKAGE LIBRARY MANUAL
## Description
This program will fix or rerun the web experiment related functions.

There are 2 types of oknpatch which are:
1.  **trial_data_lost** which is to fix the data lost of trial csv by referencing the gaze.csv.  
2.  **update** plot which is to rerun the given trial csv by the updater function of the oknserver.  

## Installation requirements and guide
### Anaconda
To install this program, `Anaconda python distributing program` and `Anaconda Powershell Prompt` are needed.  
If you do not have `Anaconda`, please use the following links to download and install:  
Download link: https://www.anaconda.com/products/distribution  
Installation guide link: https://docs.anaconda.com/anaconda/install/  
### PIP install
To install `oknpatch`, you have to use `Anaconda Powershell Prompt`.  
After that, you can use the `oknpatch` from any command prompt.  
In `Anaconda Powershell Prompt`:
```
pip install oknpatch
```  
## Usage guide
### Example usage
```
oknpatch -t "(type)" -i "(first input)" -si "(second input)" -ti "(third input)"
```
### To upgrade version  
In `Anaconda Powershell Prompt`,
```
pip install -U oknpatch
```
or
```
pip install --upgrade oknpatch
```
