import pandas as pd
import sqlite3
from eric_chen_forward import util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
import pickle

class Classifier:

    def __init__(self) -> None:
        self.eda_util = util.EDA(alpha=0.2)
        self.categories = []

    def train(self, labels_file, passages_file, csv_file=None):
        if csv_file:
            df = pd.read_csv(csv_file)
            labels = df['label'].to_list()
            passages = df['passage'].to_list()
        else:
            with open(labels_file) as f:
                labels = f.read().splitlines()
            with open(passages_file) as f:
                passages = f.read().splitlines()

        eda_passages = self.eda_util.run_data_augmentation(passages)

        passages.extend(eda_passages)
        labels.extend(labels)
        assert(len(passages) == len(labels))

        self.categories = list(set(labels))

        eda_df = pd.DataFrame()
        eda_df['label'] = labels
        eda_df['passage'] = passages
        eda_df['cleaned_text'] = eda_df['passage'].apply(lambda x: util.clean_document(x))
        eda_df['num_years'] = eda_df['passage'].apply(lambda x: util.num_years(x))

        X = eda_df[['cleaned_text', 'num_years']]
        y = eda_df['label']
        column_transformer = ColumnTransformer([
            ('tfidf', TfidfVectorizer(), 'cleaned_text')
        ])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0, stratify=y)

        sgd = Pipeline([('preprocess', column_transformer),
                ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=0, tol=None))])
        sgd.fit(X_train, y_train)
        y_pred = sgd.predict(X_test)
        print('SVM with SGD')
        print(f'accuracy: {accuracy_score(y_pred, y_test)}')
        print(classification_report(y_test, y_pred))
        print('-' * 55)

        log_reg = Pipeline([('preprocess', column_transformer),
                ('clf', LogisticRegression(C=1e5))])

        log_reg.fit(X_train, y_train)
        y_pred = log_reg.predict(X_test)
        print('Logistic Regression')
        print(f'accuracy: {accuracy_score(y_pred, y_test)}')
        print(classification_report(y_test, y_pred))
        print('-' * 55)

        choice = input('Which model to save (SVM or LR): ').strip().upper()
        while choice != 'SVM' and choice != 'LR':
            print('Invalid selection.')
            choice = input('Which model to save (SVM or LR): ').upper()

        model_name = input('Enter model name: ')
        with open(f'{model_name}.pkl', 'wb') as f:
            if choice == 'SVM':
                pickle.dump(sgd, f)
            elif choice == 'LR':
                pickle.dump(log_reg, f)
            print(f'Saving {choice} model at {model_name}.pkl')

    def get_categories(self):
        return self.categories
