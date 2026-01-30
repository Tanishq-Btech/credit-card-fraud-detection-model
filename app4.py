from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("credit_card_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("credit_card.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        row = request.form["rowdata"]

        values = row.strip().replace(",", " ").split()

        if len(values) != 30:
            return render_template("credit_card.html",
                                   prediction_text="Please paste exactly 30 values!")

        features = [float(v) for v in values]
        arr = np.array(features).reshape(1, -1)

        prediction = model.predict(arr)[0]

        if prediction == 1:
            result = "⚠️ Fraudulent Transaction Detected"
        else:
            result = "✅ Legitimate Transaction"

        return render_template("credit_card.html",
                               prediction_text=result)

    except:
        return render_template("credit_card.html",
                               prediction_text="Invalid input format!")

if __name__ == "__main__":
    app.run(debug=True)
