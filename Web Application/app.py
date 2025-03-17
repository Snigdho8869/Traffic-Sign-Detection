import os
from flask import Flask, request, render_template, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import numpy as np
import pandas as pd
import cv2
from flask import jsonify


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
model = load_model('traffic.h5')

df = pd.read_csv('label_names.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def traffic_predict():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        img = cv2.imread(file_path)
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0

        pred = model.predict(np.expand_dims(img, axis=0), verbose=False)[0].argmax()
        classid_value = pred
        filtered_df = df[df['ClassId'] == classid_value]
        signature = filtered_df['Name'].values[0]

        response = {'signature': signature}
        return jsonify(response)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
