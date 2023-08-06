# GammaLearn

<p align="left">
<img src="https://gammalearn.pages.in2p3.fr/pages/images/glearn.png" width="60px" >
<b><i>Deep learning applied to the Cherenkov Telescope Array data analysis.</b></i>
</p>

GammaLearn is a collaborative project to apply deep learning to the analysis of low-level Imaging Atmospheric Cherenkov Telescopes such as CTA.    
It provides a framework to easily train and apply models from a configuration file.

[Learn more about the GammaLearn project and its developments on its wiki page](https://gitlab.lapp.in2p3.fr/GammaLearn/GammaLearn/wikis/home)


## Table of Contents

1. [Implementation](#implementation)
1. [Contributing](#contributing)
1. [License](#license)


## Implementation

### Dependencies

- PyTorch (>= 1.7)
- Numpy
- PyTables
- Matplotlib
- scikit-image
- PyTorch Lightning (>=1.4.6)
- TensorBoard
- IndexedConv (>=1.3)
- ctapipe
- dl1-data-handler
- lstchain (0.7.3)
- torch-tb-profiler

### Installation procedure

We recommend the use of Anaconda with Python 3.8. 
```
conda create -n glearn python=3.8
conda activate glearn
```
Install PyTorch
```
conda install pytorch torchvision cudatoolkit=11.1 -c pytorch -c nvidia
```
Install other dependencies
```
conda env update -f environment.yml
```
Then you need to install dl1-data-handler
```
git clone https://github.com/cta-observatory/dl1-data-handler.git
cd dl1-data-handler
python setup_light.py
cd ..
```
Finally install GammaLearn
```
conda install gammalearn -c http://conda.anaconda.org/gammalearn
```

Install with pip
```
pip install gammalearn
```

Install from source:
```
git clone --shallow-since 2019-04-01 https://lapp-gitlab.in2p3.fr/GammaLearn/GammaLearn
cd GammaLearn
python setup.py install
```


## Usage
First activate your conda environment

To run an experiment
```
gammalearn path_to_your_experiment_settings_file.py
```
you can find an example of setting file in https://gitlab.lapp.in2p3.fr/GammaLearn/GammaLearn/-/tree/master/examples and some sample data in https://lapp-gitlab.in2p3.fr/GammaLearn/GammaLearn/share/data

To visualise the results from your experiment, GammaLearn integrates with
[GammaBoard](https://github.com/vuillaut/ctaplot) that provides high-level metrics and plots to assess IACTs reconstruction performances

To visualise the convolution kernels of your trained network (experimental feature)
```
gexplore-net path_to_your_experiments experiment_name checkpoint_version
```


## Contributing
Contributions are very much welcome.   
Open an issue to first discuss potential changes/additions.

**[Back to top](#table-of-contents)**

## License

#### MIT License


Copyright (c), 2018, GammaLearn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.




**[Back to top](#table-of-contents)**
