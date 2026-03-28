from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

def run_logreg_baseline(X_train, X_test, y_train, y_test):

    ukr_stopwords = [
        "про", "що", "та", "для", "це", "як", "але", "або", "він", "ми", 
        "щоб", "році", "року", "бути", "стати", "щодо", "його", "які",
        "на", "2025", "сказав", "який", "від", "також", "лютого", "про це", 
        "місце", "серед", "те", "2026", "зокрема" "пам", "рік", 
    ]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="word",
            ngram_range=(1,2),
            max_features=30000,
            min_df=3,
            stop_words=ukr_stopwords
        )),
        ("clf", LogisticRegression(max_iter=500, n_jobs=-1))
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