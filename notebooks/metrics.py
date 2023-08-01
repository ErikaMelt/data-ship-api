import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, roc_auc_score, roc_curve


class ClassificationPlots:
    """
    A class to create and display classification evaluation plots.
    """

    def plot_roc_curve(self, y_test, y_pred_prob):
        """
        Plots the Receiver Operating Characteristic (ROC) curve and displays the Gini value.

        Parameters:
             y_test (array-like): True labels of the test set.
             y_pred_prob (array-like): Predicted probabilities for the positive class.

        Returns:
             None (displays the plot)
        """
        roc_auc = roc_auc_score(y_test, y_pred_prob)
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
        gini_value = 2 * roc_auc - 1

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='blue', lw=2,
                 label='ROC curve (AUC = {:.2f})'.format(roc_auc))
        plt.plot([0, 1], [0, 1], color='gray', linestyle='--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=14)
        plt.ylabel('True Positive Rate', fontsize=14)
        plt.title(
            'Receiver Operating Characteristic (ROC) Curve', fontsize=16)
        plt.legend(loc='lower right', fontsize=12)
        plt.text(0.6, 0.2, 'Gini = {:.2f}'.format(gini_value), fontsize=12)
        plt.show()

    def plot_confusion_matrix(self, y_test, y_pred):
        """
        Plots the confusion matrix.

        Parameters:
            y_test (array-like): True labels of the test set.
            y_pred (array-like): Predicted labels.

        Returns:
            None (displays the plot)
        """
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    annot_kws={"size": 14}, cbar=False)
        plt.xlabel('Predicted Labels', fontsize=12)
        plt.ylabel('True Labels', fontsize=12)
        plt.title('Confusion Matrix', fontsize=16)
        plt.show()

    def plot_precision_and_recall(self, y_test, y_pred_prob):
        """
        Plots the precision-recall curve in function of confidence (probability threshold).

        Parameters:
            y_test (array-like): True labels of the test set.
            y_pred_prob (array-like): Predicted probabilities for the positive class.

        Returns:
            None (displays the plot)
        """
        thresholds = np.linspace(0, 1, 100)
        precisions = []
        recalls = []

        for threshold in thresholds:
            y_pred_threshold = (y_pred_prob >= threshold).astype(int)
            precision = precision_score(
                y_test, y_pred_threshold, zero_division=1)
            recall = recall_score(y_test, y_pred_threshold)
            precisions.append(precision)
            recalls.append(recall)

        plt.figure(figsize=(8, 6))
        plt.plot(thresholds, precisions, color='blue',
                 lw=2, label='Precision')
        plt.plot(thresholds, recalls, color='red', lw=2, label='Recall')
        plt.xlabel('Confidence (Probability Threshold)', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        plt.title(
            'Precision vs Recall in function of Confidence', fontsize=16)
        plt.legend(loc='best', fontsize=12)
        plt.show()

    def get_classification_report(self, y_test, y_pred):
        return classification_report(y_test, y_pred)
