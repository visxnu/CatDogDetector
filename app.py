from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
model = load_model('model/cat_dog_classifier.h5')

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))  # adjust size as per model
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    prediction = model.predict(img_tensor)[0]
    return "Dog" if prediction[0] > 0.5 else "Cat"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        img = request.files['file']
        path = os.path.join('static/uploads', img.filename)
        img.save(path)
        prediction = predict_image(path)
        return render_template('index.html', prediction=prediction, img_path=path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
