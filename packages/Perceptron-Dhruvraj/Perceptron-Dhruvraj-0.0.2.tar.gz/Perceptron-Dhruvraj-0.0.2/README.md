# perceptron_pypi
perceptron_pypi


## How to use it

```python
from oneNeuron.perceptron import Perceptron

X, y = prepare_data(df)

model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)
```