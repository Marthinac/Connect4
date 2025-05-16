import pandas as pd
from math import log2


# --- Discretização automática por frequências ---
def equal_frequency_discretization(df, columns, bins=3):
    result = df.copy()
    for col in columns:
        result[col] = pd.qcut(result[col], q=bins, labels=['low', 'mid', 'high'])
    return result


# --- Cálculo da entropia ---
def entropy(series):
    counts = series.value_counts()
    probabilities = counts / len(series)
    return -sum(p * log2(p) for p in probabilities if p > 0)


# --- Ganho de informação ---
def info_gain(df, feature, target):
    total_entropy = entropy(df[target])
    values = df[feature].unique()

    weighted_entropy = 0
    for val in values:
        subset = df[df[feature] == val]
        weight = len(subset) / len(df)
        weighted_entropy += weight * entropy(subset[target])

    return total_entropy - weighted_entropy


# --- Nó da árvore ---
class Node:
    def __init__(self, feature=None, prediction=None):
        self.feature = feature
        self.prediction = prediction
        self.children = {}


# --- Algoritmo ID3 ---
def id3(df, features, target):
    # Se todas as instâncias têm a mesma classe
    if len(df[target].unique()) == 1:
        return Node(prediction=df[target].iloc[0])

    # Se não há mais atributos
    if not features:
        return Node(prediction=df[target].mode()[0])

    # Selecionar o melhor atributo
    gains = {f: info_gain(df, f, target) for f in features}
    best_feature = max(gains, key=gains.get)

    root = Node(feature=best_feature)
    for val in df[best_feature].unique():
        subset = df[df[best_feature] == val]
        if subset.empty:
            root.children[val] = Node(prediction=df[target].mode()[0])
        else:
            remaining = [f for f in features if f != best_feature]
            root.children[val] = id3(subset, remaining, target)
    return root


# --- Classificação ---
def predict(node, sample):
    while node.prediction is None:
        val = sample[node.feature]
        if val in node.children:
            node = node.children[val]
        else:
            return None
    return node.prediction


# --- Execução principal ---
if __name__ == "__main__":
    df = pd.read_csv("../data/iris.csv")
    features = ['sepallength', 'sepalwidth', 'petallength', 'petalwidth']
    target = 'class'

    # Discretização automática
    df_discretized = equal_frequency_discretization(df, features, bins=3)

    # Divisão em treino e teste
    train = df_discretized.sample(frac=0.8, random_state=1)
    test = df_discretized.drop(train.index)

    # Construir árvore
    tree = id3(train, features, target)

    # Avaliar acurácia
    correct = sum(
        predict(tree, row) == row[target]
        for _, row in test.iterrows()
    )
    accuracy = correct / len(test)
    print(f"Acurácia: {accuracy:.2%}")
