# Brforest
Scikit-learn compatible implementation of Random Forest classifier with a Bayesian voting aggregation scheme. The classifier is well suited for imbalanced classification tasks. It was introduced in the paper "Decision-forest voting scheme for classification of rare classes in network intrusion detection" at IEEE SMC 2018.

Paper URL: https://ieeexplore.ieee.org/abstract/document/8616560 (pre-print available on arxiv https://arxiv.org/abs/2107.11862)

# Installation

The package is available at pip:

```
pip install brforest
```

# Usage Example

```
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from brforest import BrForestClassifier

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle = True, random_state = 42)

classifier = BrForestClassifier()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print(f"Accuracy: {sum(y_pred == y_test) / len(y_test)}")
```

More usage examples can be found in tests and in /notebooks.
