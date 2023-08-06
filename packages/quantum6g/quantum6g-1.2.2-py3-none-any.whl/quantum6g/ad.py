import numpy as np
from quantum6g import Quantum6G
import pandas as pd
from sklearn.model_selection import train_test_split
# Load the diabetes dataset from sklearn
from sklearn.datasets import load_diabetes
diabetes = load_diabetes()

# Create a pandas dataframe for the dataset
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
df['target'] = diabetes.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    df[diabetes.feature_names], df['target'], test_size=0.2)
print("X_train shape: ",X_train.shape)
quantum_6g = Quantum6G(num_wires=1,num_layers=8,batch_size=128,learning_rate=0.002)
quantum_6g = quantum_6g.build_model(X_train, y_train, X_test, y_test,epochs=5)
print("Accuracy: {:.2f}%".format(quantum_6g[1][1] * 100))
print("Loss: {:.2f}%".format(quantum_6g[1][0] * 100))
