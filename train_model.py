import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ------------------------
# ID3 Algorithm
# ------------------------
def entropy(y):
    values, counts = np.unique(y, return_counts=True)
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs))

def information_gain(X, y, feature):
    values, counts = np.unique(X[feature], return_counts=True)
    weighted_entropy = np.sum([
        (counts[i] / np.sum(counts)) * entropy(y[X[feature] == values[i]])
        for i in range(len(values))
    ])
    return entropy(y) - weighted_entropy

def id3(X, y, features):
    if len(np.unique(y)) == 1:
        return y.iloc[0]
    if len(features) == 0:
        return y.mode()[0]

    gains = [information_gain(X, y, f) for f in features]
    best_feature = features[np.argmax(gains)]

    tree = {best_feature: {}}
    for value in np.unique(X[best_feature]):
        sub_X = X[X[best_feature] == value]
        sub_y = y[X[best_feature] == value]
        remaining_features = [f for f in features if f != best_feature]
        tree[best_feature][value] = id3(sub_X, sub_y, remaining_features)
    return tree

# ------------------------
# Load dataset
# ------------------------
data = pd.read_csv("mushrooms.csv")

# Chỉ dùng 3 feature để khớp với web form
features = ["odor", "cap-color", "gill-color"]
X = data[features]
y = data["class"]

# Train-test split để đánh giá
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train ID3
tree = id3(X_train, y_train, features)

# ------------------------
# Đánh giá nhanh
# ------------------------
def predict(tree, sample, default="e"):
    if not isinstance(tree, dict):
        return tree
    feature = next(iter(tree))
    value = sample.get(feature, None)
    if value in tree[feature]:
        return predict(tree[feature][value], sample, default)
    else:
        return default

y_pred = [predict(tree, X_test.iloc[i].to_dict()) for i in range(len(X_test))]
print("🎯 Accuracy:", accuracy_score(y_test, y_pred))

# ------------------------
# Save model
# ------------------------
with open("mushroom_model.pkl", "wb") as f:
    pickle.dump(tree, f)

print("✅ Mô hình đã huấn luyện và lưu thành mushroom_model.pkl")
