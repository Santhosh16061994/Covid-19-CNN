# -*- coding: utf-8 -*-=
"""
Created on Fri Jun 30 03:12:09 2023

@author: Santhosh T N
"""

import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np

# Load the trained model
#classifier = load_model('D:/1. DS Simplilearn/Covid 19/2. covid_19_disease_detection-main/my_1model.h5')

classifier = load_model('my_1model.h5')

# Streamlit app title
st.title("Model for Covid-19 Disease Detection using X-ray Image Classification")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    st.image(uploaded_file)

    # Preprocess the uploaded image
    img = Image.open(uploaded_file)
    img_array = np.array(img)
    cv2.imwrite('temp.jpg', img_array)
    test_image = image.load_img('temp.jpg', target_size=(64, 64, 3))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    # Make predictions
    result = classifier.predict(test_image)

    if result[0][0] == 1:
        prediction = 'COVID-19 Positive'
    else:
        prediction = 'COVID-19 Negative'

    # Display the prediction
    st.write("Prediction:", prediction)
