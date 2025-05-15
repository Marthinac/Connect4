import pandas as pd
import numpy as np
from math import log2
from collections import Counter


# Discretization function using optimal binning
def discretize_iris(data):
    discretized = data.copy()
    bins = {
        'sepallength': [0, 5.4, 6.9, 10],
        'sepalwidth': [0, 2.8, 3.2, 10],
        'petallength': [0, 2.0, 5.0, 10],
        'petalwidth': [0, 0.8, 1.8, 10]
    }
    labels = ['small', 'medium', 'large']

    for feature in bins:
        discretized[feature] = pd.cut(data[feature], bins=bins[feature],
                                      labels=labels, include_lowest=True)
    return discretized


# Calculate entropy
def entropy(labels):
    counts = Counter(labels)
    probs = [count / len(labels) for count in counts.values()]
    return -sum(p * log2(p) for p in probs if p > 0)


# Calculate information gain
def information_gain(data, feature, target):
    total_entropy = entropy(data[target])
    values = data[feature].unique()

    weighted_entropy = 0
    for value in values:
        subset = data[data[feature] == value]
        weighted_entropy += (len(subset) / len(data)) * entropy(subset[target])

    return total_entropy - weighted_entropy


# Decision tree node class
class DecisionNode:
    def __init__(self, feature=None, children=None, leaf_value=None):
        self.feature = feature
        self.children = children or {}
        self.leaf_value = leaf_value


# ID3 algorithm implementation
def id3(data, features, target, parent_entropy=0):
    if len(data[target].unique()) == 1:
        return DecisionNode(leaf_value=data[target].iloc[0])

    if not features:
        majority_class = data[target].mode()[0]
        return DecisionNode(leaf_value=majority_class)

    best_feature = max(features, key=lambda f: information_gain(data, f, target))
    remaining_features = [f for f in features if f != best_feature]

    node = DecisionNode(feature=best_feature)
    for value in data[best_feature].unique():
        subset = data[data[best_feature] == value]
        if subset.empty:
            node.children[value] = DecisionNode(leaf_value=data[target].mode()[0])
        else:
            node.children[value] = id3(subset, remaining_features, target)

    return node


# Classification function
def classify(tree, sample):
    if tree.leaf_value is not None:
        return tree.leaf_value
    feature_value = sample[tree.feature]
    if feature_value in tree.children:
        return classify(tree.children[feature_value], sample)
    else:
        return None  # Handle unseen values


# Main execution
if __name__ == "__main__":
    # Load and preprocess data
    iris = pd.read_csv('data/iris.csv')
    features = ['sepallength', 'sepalwidth', 'petallength', 'petalwidth']
    target = 'class'

    # Discretize features
    discretized = discretize_iris(iris)

    # Split data
    train = discretized.sample(frac=0.8, random_state=42)
    test = discretized.drop(train.index)

    # Build tree
    tree = id3(train, features, target)

    # Test accuracy
    correct = 0
    for _, row in test.iterrows():
        prediction = classify(tree, row)
        if prediction == row[target]:
            correct += 1

    print(f"Accuracy: {correct / len(test):.2%}")
