import statistics


def precision(true_positives, false_positives):
    res = {}
    for tp, fp in zip(true_positives.items(), false_positives.items()):
        if tp[1] + fp[1] != 0:
            res[tp[0]] = tp[1] / (tp[1] + fp[1])
    return statistics.mean(res.values()) * 100


def recall(false_negatives, true_positives):
    res = {}
    for tp, fn in zip(true_positives.items(), false_negatives.items()):
        if tp[1] + fn[1] != 0:
            res[tp[0]] = tp[1] / (tp[1] + fn[1])
    return statistics.mean(res.values()) * 100


def accuracy(false_negatives, true_positives, true_negatives, false_positives):
    true = {}
    false = {}
    for tp, tn, fp, fn in zip(true_positives.items(), true_negatives.items(), false_positives.items(),
                              false_negatives.items()):
        true[tp[0]] = tp[1] + tn[1]
        false[fp[0]] = fp[1] + fn[1]
    true = sum(true.values())
    false = sum(false.values())
    return true / (true + false) * 100


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
