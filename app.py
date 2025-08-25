from flask import Flask, render_template, request
import pickle

# Load model
with open("mushroom_model.pkl", "rb") as f:
    tree = pickle.load(f)

# Hàm dự đoán
def predict(tree, sample, default="e"):
    if not isinstance(tree, dict):
        return tree
    feature = next(iter(tree))
    value = sample.get(feature, None)
    if value in tree[feature]:
        return predict(tree[feature][value], sample, default)
    else:
        return default

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    odor = cap = gill = None

    if request.method == "POST":
        odor = request.form.get("odor")
        cap = request.form.get("cap_color")
        gill = request.form.get("gill_color")

        sample = {
            "odor": odor,
            "cap-color": cap,
            "gill-color": gill
        }

        prediction = predict(tree, sample)

        if prediction == "e":
            result = "🍄 Nấm ăn được (Edible)"
        elif prediction == "p":
            result = "☠️ Nấm độc (Poisonous)"
        else:
            result = "⚠️ Không xác định"

    return render_template("index.html", result=result, odor=odor, cap=cap, gill=gill)


if __name__ == "__main__":
    app.run(debug=True)
