# core-bioimage-io-python

Python specific core utilities for running models in the [BioImage Model Zoo](https://bioimage.io)

## Installation

### Via Conda

The `bioimageio.core` package supports various back-ends for running BioimageIO networks:

* Pytorch/Torchscript:
  ```bash
  # cpu installation (if you don't have an nvidia graphics card)
  conda install -c pytorch -c conda-forge -c ilastik-forge bioimageio.core pytorch torchvision cpuonly

  # gpu installation
  conda install -c pytorch -c conda-forge -c ilastik-forge bioimageio.core pytorch torchvision cudatoolkit
  ```

* Tensorflow
  ```bash
  # currently only cpu version supported
  conda install -c conda-forge -c ilastik-forge bioimageio.core tensorflow
  ```

* ONNXRuntime
  ```bash
  # currently only cpu version supported
  conda install -c conda-forge -c ilastik-forge bioimageio.core onnxruntime
  ```

### Set up Development Environment

To set up a development conda environment run the following commands:
```
conda env create -f dev/environment-base.yaml
conda activate bio-core-dev
pip install -e . --no-deps
```

There are different environment files that only install tensorflow or pytorch as dependencies available.

## Command Line

You can list all the available command line options:
```
bioimageio
```

Test a model:
```
bioimageio test -m <MODEL>
```

Run prediction:
```
bioimageio predict -m <MODEL> -i <INPUT> -o <OUTPUT>
```

This is subject to change, see https://github.com/bioimage-io/core-bioimage-io-python/issues/87.


## Running network predictions:

TODO

## Model Specification

The model specification and its validation tools can be found at https://github.com/bioimage-io/spec-bioimage-io.
