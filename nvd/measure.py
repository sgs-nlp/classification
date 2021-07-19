def precision(false_negatives, true_positives, true_negatives, false_positives):
    return true_positives / (true_positives + false_positives)


def recall(false_negatives, true_positives, true_negatives, false_positives):
    return true_positives / (false_negatives + true_positives)


def accuracy(false_negatives, true_positives, true_negatives, false_positives):
    return (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)


def balanced_accuracy(false_negatives, true_positives, true_negatives, false_positives):
    tpr = true_positives / (true_positives + false_negatives)
    tnr = true_negatives / (true_negatives + false_positives)
    return (tpr + tnr) / 2


def predicted_positive_condition_rate(false_negatives, true_positives, true_negatives, false_positives):
    return (true_positives + false_positives) / (false_negatives + true_positives + true_negatives + false_positives)


def f_beta(false_negatives, true_positives, true_negatives, false_positives, beta=1):
    precision_score = precision(false_negatives, true_positives, true_negatives, false_positives)
    recall_score = recall(false_negatives, true_positives, true_negatives, false_positives)
    return (1 + beta ** 2)((precision_score * recall_score) / ((beta ** 2) * precision_score + recall_score))
