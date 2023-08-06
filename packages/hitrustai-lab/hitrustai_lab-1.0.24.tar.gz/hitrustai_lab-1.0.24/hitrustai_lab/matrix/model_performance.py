from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc
import numpy as np
import pandas as pd


class ModelPerfornance:
    def __init__(self, score_type="total_score"):
        self.score_type = score_type

    def calculate_prc_auc(self, recall_lst, precision_lst):
        pr_list = list(zip(precision_lst, recall_lst))
        pr_list = [item for item in pr_list if -1 not in item]
        precision_lst, recall_lst = list(zip(*pr_list))
        auc_precision_recall = round(auc(recall_lst, precision_lst), 3)
        return auc_precision_recall

    def performance_output(self, y_test, y_score):
        threshold_lst = []
        tp_lst = []
        fp_lst = []
        tn_lst = []
        fn_lst = []
        accuracy_lst = []
        precision_lst = []
        recall_lst = []
        f1_score_lst = []
        fnr_lst = []
        fpr_lst = []
        npv_lst = []
        fdr_lst = []
        for_lst = []
        tnr_lst = []

        auc_lst = []
        for i in range(0, 11, 1):
            threshold = i / 10
            y_pre = np.where(y_score >= threshold, 1, 0)
            tb = pd.DataFrame({'predict_label': y_pre, 'true_label': y_test})
            tb['tp'] = np.where((tb['true_label'] == 1) &
                                (tb['predict_label'] == 1), 1, 0)
            tb['fp'] = np.where((tb['true_label'] == 0) &
                                (tb['predict_label'] == 1), 1, 0)
            tb['tn'] = np.where((tb['true_label'] == 0) &
                                (tb['predict_label'] == 0), 1, 0)
            tb['fn'] = np.where((tb['true_label'] == 1) &
                                (tb['predict_label'] == 0), 1, 0)
            tp = sum(tb['tp'])
            fp = sum(tb['fp'])
            tn = sum(tb['tn'])
            fn = sum(tb['fn'])

            try:
                accuracy = (tp+tn)/(tp+tn+fp+fn)
                accuracy = round(accuracy, 3)
            except ZeroDivisionError:
                accuracy = -1.0

            try:
                precision = tp/(tp+fp)
                precision = round(precision, 3)
            except ZeroDivisionError:
                precision = -1.0

            try:
                recall = tp/(tp+fn)
                recall = round(recall, 3)
            except ZeroDivisionError:
                recall = -1.0

            try:
                f1_score = (2*precision*recall)/(precision+recall)
                f1_score = round(f1_score, 3)
            except ZeroDivisionError:
                f1_score = -1.0

            try:
                fnr = fn/(tp+fn)
                fnr = round(fnr, 3)
            except ZeroDivisionError:
                fnr = -1.0

            try:
                fpr = fp/(fp+tn)
                fpr = round(fpr, 3)
            except ZeroDivisionError:
                fpr = -1.0

            try:
                npv = tn/(fn+tn)
                npv = round(npv, 3)
            except ZeroDivisionError:
                npv = -1.0

            try:
                fdr = fp/(tp+fp)
                fdr = round(fdr, 3)
            except ZeroDivisionError:
                fdr = -1.0

            try:
                for_ = fn/(fn+tn)
                for_ = round(for_, 3)
            except ZeroDivisionError:
                for_ = -1.0

            try:
                tnr = tn/(fp+tn)
                tnr = round(tnr, 3)
            except ZeroDivisionError:
                tnr = -1.0

            if self.score_type == 'policy_score':
                threshold_lst.append(round(-2*threshold+1, 3))
            elif self.score_type == 'total_score':
                threshold_lst.append(threshold)
            tp_lst.append(tp)
            fp_lst.append(fp)
            tn_lst.append(tn)
            fn_lst.append(fn)
            accuracy_lst.append(accuracy)
            precision_lst.append(precision)
            recall_lst.append(recall)
            f1_score_lst.append(f1_score)
            fnr_lst.append(fnr)
            fpr_lst.append(fpr)
            npv_lst.append(npv)
            fdr_lst.append(fdr)
            for_lst.append(for_)
            tnr_lst.append(tnr)
        auc_precision_recall = self.calculate_prc_auc(fpr_lst, recall_lst)
        auc_lst.append(auc_precision_recall)
        if self.score_type == 'policy_score':
            result = {
                "threshold_lst": threshold_lst[::-1],
                "tp_lst": tp_lst[::-1],
                "fp_lst": fp_lst[::-1],
                "tn_lst": tn_lst[::-1],
                "fn_lst": fn_lst[::-1],
                "accuracy_lst": accuracy_lst[::-1],
                "precision_lst": precision_lst[::-1],
                "recall_lst": recall_lst[::-1],
                "f1_score_lst": f1_score_lst[::-1],
                "fnr_lst": fnr_lst[::-1],
                "fpr_lst": fpr_lst[::-1],
                "npv_lst": npv_lst[::-1],
                "fdr_lst": fdr_lst[::-1],
                "for_lst": for_lst[::-1],
                "tnr_lst": tnr_lst[::-1],
                "auc_lst": auc_lst
            }
        else:
            result = {
                "threshold_lst": threshold_lst,
                "tp_lst": tp_lst,
                "fp_lst": fp_lst,
                "tn_lst": tn_lst,
                "fn_lst": fn_lst,
                "accuracy_lst": accuracy_lst,
                "precision_lst": precision_lst,
                "recall_lst": recall_lst,
                "f1_score_lst": f1_score_lst,
                "fnr_lst": fnr_lst,
                "fpr_lst": fpr_lst,
                "npv_lst": npv_lst,
                "fdr_lst": fdr_lst,
                "for_lst": for_lst,
                "tnr_lst": tnr_lst,
                "auc_lst": auc_lst
            }
        return result

    def model_train(self):
        random_state = 1
        # Create dataset for binary classification with 5 predictors
        X, y = datasets.make_classification(n_samples=1000,
                                            n_features=5,
                                            n_informative=3,
                                            n_redundant=2)
        # n_redundant=2, random_state=random_state)

        # Split into training and test
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.5)
        # test_size=0.5 ,random_state=random_state)

        # Create classifier using logistic regression
        classifier = LogisticRegression(random_state=random_state)
        classifier.fit(X_train, y_train)
        y_score = classifier.predict_proba(X_test)[:, 1]
        # result = self.performance_output(y_test, y_score)
        # return result
        return y_test, y_score


def main():
    mp = ModelPerfornance(score_type='policy_score')
    list_y_test, list_y_score = mp.model_train()
    result = mp.performance_output(list_y_test, list_y_score)
    print(result)


if __name__ == "__main__":
    main()
