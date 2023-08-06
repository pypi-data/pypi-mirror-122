import numpy as np
from keras.preprocessing import image
from keras.applications.resnet import ResNet50 
import matplotlib.pyplot as plt
from pathlib import Path

def prediction(path):
    path = Path(path)
    img = image.load_img(path, target_size=(224,224))
    image_array = image.img_to_array(img)
    x_train = np.expand_dims(image_array, axis=0)
    x_train = ResNet50.preprocess_input(x_train)
    plt.imread(path)
    plt.imshow(img)
    plt.show()
    model = ResNet50(weights="imagenet")
    predict = model.predict(x_train)
    pred = ResNet50.decode_predictions(predict)
    return pred