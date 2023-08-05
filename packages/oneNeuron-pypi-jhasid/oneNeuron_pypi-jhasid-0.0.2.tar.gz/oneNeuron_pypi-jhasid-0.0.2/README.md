# oneNeuron_pypi
oneNeuron_pypi

# Reference

[Packaging Reference](https://packaging.python.org/tutorials/packaging-projects/)

[git hub docs for git hub actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registeries)

## How to use

```python
from oneNeuron.pereceptron import Perceptron  #src file

## get X,Y and then use as below
model = Perceptron(eta=eta,epochs=epochs)
model.fit(x,y)
```
