import streamlit as st
from PIL import Image
from tensorflow import keras
import numpy as np

covid19_model = keras.models.load_model('covid19model.h5')

def main():

    st.title("COVID19 Detector based on Deep Learning")
    col1, col2, col3 = st.columns(3)

    img_normal = Image.open("./ref_images/xray_normal.png")
    col1.subheader("NORMAL")
    col1.image(img_normal, use_column_width=True, caption='Normal Chest X-ray')

    img_viral_pneumonia = Image.open("./ref_images/xray_viral_pneumonia.png")
    col2.subheader("VIRAL PNEUMONIA")
    col2.image(img_viral_pneumonia, use_column_width=True, caption='Chest X-ray with Viral Pneumonia')

    img_covid19 = Image.open("./ref_images/xray_covid.png")
    col3.subheader("COVID-19")
    col3.image(img_covid19, use_column_width=True, caption='Chest X-ray with COVID-19')

    image_object = st.file_uploader("Upload the X-ray", type=["png", "jpg", "jpeg"])

    if image_object is not None:
        radiography_img = Image.open(image_object)

        img_temp_file = 'radiography-tmp.' + radiography_img.format
        radiography_img.save(img_temp_file)

        keras_img_object = keras.preprocessing.image.load_img(img_temp_file, target_size=(256, 256))
        img_array = keras.preprocessing.image.img_to_array(keras_img_object)
        img_array = img_array / 255.0
        img_array = img_array.reshape(-1, 256, 256, 1)

        predictions = covid19_model.predict(img_array)
        final_prediction_array = predictions[0]

        class_names = ['COVID-19', 'NORMAL', 'VIRAL PNEUMONIA']

        prediction = class_names[np.argmax(final_prediction_array)]
        probability = 100 * np.max(final_prediction_array)

        st.image(radiography_img, width=250)
        st.write(f'Prediction: {prediction} - Probability: {probability:.4f}')

if __name__ == '__main__':
    main()
