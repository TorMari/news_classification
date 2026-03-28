from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline, FeatureUnion
import pandas as pd

ukr_stopwords = [
        "про", "що", "та", "для", "це", "як", "але", "або", "він", "ми", 
        "щоб", "році", "року", "бути", "стати", "щодо", "його", "які",
        "на", "2025", "сказав", "який", "від", "також", "лютого", "про це", 
        "місце", "серед", "те", "2026", "зокрема" "пам", "рік", 
    ]

def run_linear_svc(X_train, X_test, y_train, y_test):
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="word",
            ngram_range=(1,2),
            max_features=30000,
            min_df=3,
            stop_words=ukr_stopwords
        )),
        ("clf", LinearSVC(C=1.0, max_iter=2000))
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("Accuracy:", acc)
    print("Macro F1:", f1)
    print("Classification report:\n", classification_report(y_test, y_pred))
    print("\n")

    return pipeline, y_pred, acc, f1


def run_linear_svc_char(X_train, X_test, y_train, y_test):
    pipeline = Pipeline([
        ("features", FeatureUnion([
            ("word_tfidf", TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 2), 
                max_features=20000,
                min_df=3,
                stop_words=ukr_stopwords
            )),
            ("char_tfidf", TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 5), 
                max_features=15000,
                min_df=5
            ))
        ])),
        ("clf", LinearSVC(C=1.0, max_iter=2000, random_state=42))
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="macro")
    print("Accuracy:", acc)
    print("Macro F1:", f1)
    print("Classification report:\n", classification_report(y_test, y_pred))
    print("\n")

    return pipeline, y_pred, acc, f1


def run_linear_svc_balanced(X_train, X_test, y_train, y_test):
    pipeline_balanced = Pipeline([
        ("features", FeatureUnion([
            ("word_tfidf", TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 2), 
                max_features=20000,
                min_df=3,
                stop_words=ukr_stopwords
            )),
            ("char_tfidf", TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(3, 5), 
                max_features=15000,
                min_df=5
            ))
        ])),
        ("clf", LinearSVC(C=1.0, class_weight="balanced", max_iter=2000, random_state=42))
    ])

    pipeline_balanced.fit(X_train, y_train)
    y_pred_balanced = pipeline_balanced.predict(X_test)

    acc = accuracy_score(y_test, y_pred_balanced)
    f1 = f1_score(y_test, y_pred_balanced, average="macro")
    print("Accuracy:", acc)
    print("Macro F1:", f1)
    print("Classification report:\n", classification_report(y_test, y_pred_balanced))
    print("\n")

    return pipeline_balanced, y_pred_balanced, acc, f1
