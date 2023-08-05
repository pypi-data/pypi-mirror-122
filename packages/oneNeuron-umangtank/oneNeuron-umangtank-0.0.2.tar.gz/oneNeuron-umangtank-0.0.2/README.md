# oneNeuron_pypi

**what is pypi?**

- The Python Package Index (PyPI) is a repository of software for the Python programming language.

It's use for publishing any python package.

# How to use-
* install the latest package 

> * in jupyter notebook -
```
    !pip install oneNeuron-umangtank
```
> * in command prompt -
```bash    
    pip install oneNeuron-umangtank
```
* Now run below snippets of code in your jupyter-notebooks cell to perform perceptron.

```python
from oneNeuron.Perceptron import Perceptron

## get X and y and then use below commands

# eta = learning rate
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
```

#### pypi
[oneNeuron-umangtank](https://pypi.org/project/oneNeuron-umangtank/)

#### Author
[Umang Tank](https://www.linkedin.com/in/umangtank/)