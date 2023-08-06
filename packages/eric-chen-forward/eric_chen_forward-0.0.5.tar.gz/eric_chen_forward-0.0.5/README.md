# eric_chen_forward

To train the model:
```python
from eric_chen_forward.model import Classifier

model = Classifier()

# option 1
# text files of labels and passages respectively, separated by newlines
model.train("labels_file_path", "passages_file_path")

# option 2
# csv file with a 'label' column and 'passage' column, the column names are hardcoded
model.train(csv_file="csv_file_path")
```

To use the saved model in code:
```python
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
```

To run the classifier demo:
```python
from eric_chen_forward import url_classifier_demo

url_classifier_demo.Demo()
```
