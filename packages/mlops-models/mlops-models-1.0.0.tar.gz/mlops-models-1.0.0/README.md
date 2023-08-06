# Sample model 

![Unit tests](https://github.com/FRI-Machine-Learning-Operations-22-23/mlops-01-hands-on/actions/workflows/test-package.yml/badge.svg)

Test repo for hands-on part of the first MLOps lecture.


## How to use it




```python
from mlops_models import ConstantPredictionModel

model = ConstantPredictionModel(0)
model.predict("")
> 0
```


```python
from mlops_models import ConstantPredictionModel

model = ConstantPredictionModel(1)
model.predict("")
> 1
```


## How to build it

To build a python package, run the following command:

```bash
python setup.py sdist bdist_wheel
```

This will generate a `dist` folder with the following structure:

```
mlops_models-0.1.0-py3-none-any.whl
mlops_models-0.1.0.tar.gz
```

## How to test it

To run the tests, run the following command:

```bash
python -m pytest
```

## How to install it

To install the package, run the following command:

```bash
pip install mlops_models-0.1.0-py3-none-any.whl
```

To install it in development mode, run the following command:

```bash 
pip install -e .
```

## How to run it

To run the package, run the following command:

```bash
python -m mlops_models
```

## How to publish it

To publish the package, run the following command:

```bash
python -m twine upload dist/*
```

To publish package in GitHub, run the following command:

```bash
python -m github-release upload --tag v0.1.0 --user FRI-Machine-Learning-Operations-22-23 --repo mlops-01-hands-on --name "mlops_models-0.1.0-py3-none-any.whl" --file dist/mlops_models-0.1.0-py3-none-any.whl
```

## How to contribute

To contribute, run the following commands:

```bash
git clone
```