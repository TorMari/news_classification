from sklearn.metrics import confusion_matrix, precision_recall_curve, precision_score, recall_score, f1_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(y_test, y_pred, title):
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Прогнозований клас")
    plt.ylabel("Справжній клас")
    plt.title(title)
    plt.tight_layout()
    plt.show()

def evaluate_thresholds(y_true, y_scores, class_id, strategy="balance", class_names=None):
    y_binary = (y_true == class_id).astype(int)
    scores = y_scores[:, class_id]
    
    precision, recall, thresholds = precision_recall_curve(y_binary, scores)
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
    
    if strategy == "balance":
        idx = np.argmax(f1_scores)
        reason = "Максимальний F1 (Баланс)"
    elif strategy == "precision-first":
        mask = precision >= 0.90
        if any(mask):
            idx = np.where(mask)[0][0]
            reason = "Precision >= 90% (Мінімум помилкових спрацювань)"
        else:
            idx = np.argmax(precision)
            reason = "Максимально можливий Precision"
    elif strategy == "recall-first":
        mask = recall >= 0.90
        if any(mask):
            idx = np.where(mask)[0][-1] 
            reason = "Recall >= 90% (Мінімум пропущених новин)"
        else:
            idx = np.argmax(recall)
            reason = "Максимально можливий Recall"
    
    final_idx = min(idx, len(thresholds) - 1)
    chosen_threshold = thresholds[final_idx]
    
    plt.figure(figsize=(8, 6))
    plt.plot(thresholds, precision[:-1], label='Precision', color='blue', linestyle='--')
    plt.plot(thresholds, recall[:-1], label='Recall', color='green', linestyle='-')
    plt.plot(thresholds, f1_scores[:-1], label='F1 Score', color='red', lw=2)
    
    plt.axvline(x=chosen_threshold, color='black', linestyle=':', label=f'Обраний поріг: {chosen_threshold:.2f}')
    
    class_name = class_names[class_id] if class_names else f"ID {class_id}"
    plt.title(f"Підбір порогу для класу '{class_name}'\nСтратегія: {strategy} ({reason})")
    plt.xlabel("Поріг (Decision Score)")
    plt.ylabel("Метрика")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
    
    print(f"--- Результати для '{class_name}' ({strategy}) ---")
    print(f"Поріг: {chosen_threshold:.4f}")
    print(f"Precision: {precision[final_idx]:.4f}")
    print(f"Recall: {recall[final_idx]:.4f}")
    print(f"F1 Score: {f1_scores[final_idx]:.4f}")
    
    return chosen_threshold

def apply_custom_thresholds(y_scores, threshold_dict):
    y_pred_custom = np.argmax(y_scores, axis=1) 
    
    for class_id, threshold in threshold_dict.items():
        mask = y_scores[:, class_id] >= threshold
        y_pred_custom[mask] = class_id
        
    return y_pred_custom


def plot_pr_curve_with_thresholds(y_test, y_score, class_id=0, thresholds_to_show=[0.0, 0.5], class_names=None):
    y_binary = (y_test == class_id).astype(int)
    scores = y_score[:, class_id]
    
    precision, recall, thresholds = precision_recall_curve(y_binary, scores)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, lw=2, label="PR curve")
    
    for t in thresholds_to_show:
        idx = np.argmin(np.abs(thresholds - t))
        plt.scatter(recall[idx], precision[idx], s=80, label=f"t={thresholds[idx]:.2f}")
    
    class_name = class_names[class_id] if class_names else f"Клас {class_id}"
    
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"PR-крива для класу '{class_name}'")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
    
    print(f"--- Порівняння порогів для '{class_name}' ---")
    for t in thresholds_to_show:
        y_pred = (scores >= t).astype(int)
        p = precision_score(y_binary, y_pred)
        r = recall_score(y_binary, y_pred)
        f1 = f1_score(y_binary, y_pred)
        
        print(f"t = {t:.2f} → Precision={p:.3f}, Recall={r:.3f}, F1={f1:.3f}")
