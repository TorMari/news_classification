from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def run_experiment(X_train, X_test, y_train, y_test):

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

    vectorizer = pipeline.named_steps["tfidf"]
    clf = pipeline.named_steps["clf"]

    errors_df = pd.DataFrame({
        "text": X_test,
        "gold_label": y_test,
        "predicted_label": y_pred,
        "comment": ""
    })
    errors_df = errors_df[errors_df["gold_label"] != errors_df["predicted_label"]]
    errors_df = errors_df.reset_index().rename(columns={"index": "text_id"})

    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average="macro")
    report = classification_report(y_test, y_pred)
    print("Accuracy:", acc)
    print("Macro F1:", macro_f1)
    print("Classification report:\n", report)
    print("\n")

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(10,8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Прогнозований клас")
    plt.ylabel("Справжній клас")
    plt.title("Confusion matrix")
    plt.tight_layout()
    plt.show()

    
    return acc, macro_f1, report, vectorizer, clf, errors_df
