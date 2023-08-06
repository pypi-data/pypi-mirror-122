# Welcome to the Dheeraj Kumar Open Source Contribution

    This Binsearchpy package is developed with base of Binary search algorith, which helps to search the given Integer or String element in given list.
    This package has Two modules

        1) binarySearchlist

        2) binarySearchstring

#  How to Import Modules

```python
from Binsearch.BinarySearch import BinarySearchList
    
BinarySearchList(array, 0, len(array)-1, givenValue)

from Binsearch.BinarySearch import BinarySearchString

BinarySearchString(array, givenString)
```

# Commands to upload pypi package

        1)  python setup.py register

        2)  python setup.py sdist

        3)  twine upload dist/*