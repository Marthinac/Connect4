import pandas as pd
import numpy as np
import os, pickle
from id3 import ID3Tree


# Caminho correto para o notebook
dataset_path = os.path.join("../data/connect4_dataset.csv")

# Carregar o novo dataset
data = pd.read_csv(dataset_path)
print(data.head())
print(data.info())

# Separar características (X) e alvo (y)
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Dividir em treino e teste (80/20)
treino_frac = 0.8
train_size = int(len(X) * treino_frac)

X_train = X[:train_size].copy()
X_test = X[train_size:].copy()
y_train = y[:train_size].copy()
y_test = y[train_size:].copy()

# Garantir que os conjuntos de treino e teste sejam DataFrames e Series
if isinstance(X_train, pd.DataFrame) == False:
    X_train = pd.DataFrame(X_train, columns=[f'cell_{i}' for i in range(42)])
if isinstance(X_test, pd.DataFrame) == False:
    X_test = pd.DataFrame(X_test, columns=[f'cell_{i}' for i in range(42)])
if isinstance(y_train, pd.Series) == False:
    y_train = pd.Series(y_train)
if isinstance(y_test, pd.Series) == False:
    y_test = pd.Series(y_test)

print(f'Tamanho do conjunto de treino: {len(X_train)}')
print(f'Tamanho do conjunto de teste: {len(X_test)}')

# Treinar a árvore ID3
id3_tree = ID3Tree(max_depth=20)
id3_tree.fit(X_train, y_train)

# Previsão
y_pred = id3_tree.predict(X_test)

# Acurácia
accuracy = np.mean(y_pred == y_test) * 100
print(f'Acurácia da Árvore ID3: {accuracy:.2f}%')

# Caminho do arquivo do modelo
model_path = os.path.join("../id3_model.pkl")

# Salvando o modelo treinado
with open(model_path, "wb") as file:
    pickle.dump(id3_tree, file)
print("Modelo ID3 salvo com sucesso!")