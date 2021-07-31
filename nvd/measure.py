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
    # todo
    tpr = true_positives / (true_positives + false_negatives)
    tnr = true_negatives / (true_negatives + false_positives)
    return (tpr + tnr) / 2


def predicted_positive_condition_rate(false_negatives, true_positives, true_negatives, false_positives):
    # todo
    return (true_positives + false_positives) / (false_negatives + true_positives + true_negatives + false_positives)


def f_beta(false_negatives, true_positives, true_negatives, false_positives, beta=1):
    # todo
    precision_score = precision(false_negatives, true_positives, true_negatives, false_positives)
    recall_score = recall(false_negatives, true_positives, true_negatives, false_positives)
    return (1 + beta ** 2)((precision_score * recall_score) / ((beta ** 2) * precision_score + recall_score))


def true_or_false(predicted, y_test, classes):
    true_positive = {}
    true_negative = {}
    false_positive = {}
    false_negative = {}
    true = {}
    false = {}
    for predicted_item, res in zip(predicted, y_test):
        if predicted_item == res:
            if res not in true:
                true[res] = 0
            true[res] += 1
        else:
            if res not in false:
                false[res] = 0
            false[res] += 1
    for c in classes:
        if c not in true:
            true[c] = 0
        true_positive[c] = true[c]
        true_negative[c] = sum(true.values()) - true[c]
        if c not in false:
            false[c] = 0
        false_positive[c] = false[c]
        false_negative[c] = sum(false.values()) - false[c]
    return false_negative, true_positive, true_negative, false_positive
