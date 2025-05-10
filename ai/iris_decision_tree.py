import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from id3 import ID3Tree

def load_and_discretize_iris():
    """
    Carrega o dataset Iris e discretiza os valores numéricos.
    """
    iris = load_iris()
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    
    for column in iris.feature_names:
        data[column] = pd.qcut(data[column], q=3, labels=['low', 'medium', 'high'])
    
    return data

if __name__ == "__main__":
    iris_data = load_and_discretize_iris()
    X = iris_data.drop(columns=['target'])
    y = iris_data['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    tree = ID3Tree()
    tree.fit(X_train, y_train)
    print("\nÁrvore de Decisão para o Iris Dataset:")
    print(tree.tree)

    predictions = tree.predict(X_test)
    accuracy = (predictions == y_test).mean() * 100
    print(f"Acurácia no conjunto de teste: {accuracy:.2f}%")