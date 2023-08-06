# FairPy: A Python Library for Machine Learning Fairness

FairPy is a comprehensive python library for machine learning fairness, covering various fairness notions, multiple advanced algorithms, and experimental datasets.
FairPy is a good toolkit for mitigating bias and helping to deliver equitable outcomes from machine learning models.

AI Fairness with few lines of codes:
```python
from fairpy.dataset import Adult
from fairpy.model import LabelBias

dataset = Adult()
split_data = dataset.split()
model = LabelBias()
model.fit(split_data.X_train, split_data.y_train, split_data.s_train)
model.predict(split_data.X_test)
```

Want to learn more about machine learning fairness? Check our actively maintained paper list: [Awesome Machine Learning Fairness](https://github.com/brandeis-machine-learning/awesome-ml-fairness).
