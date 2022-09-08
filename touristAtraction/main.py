from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
from typing import Union
import PIL
import os
import tensorflow as tf
from keras.models import load_model, model_from_json

import pandas as pd
import wikipedia

from pytrends.request import TrendReq

import matplotlib.pyplot as plt
from matplotlib.artist import kwdoc
import seaborn as sns

from matplotlib.image import imread
import matplotlib.pyplot as plt
from PIL import Image
import cv2


def loadModel():
    json_file = open('./model/model_tourist_TF.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("./model/model_tourist_tf_weights.h5")
    return loaded_model

app = FastAPI()

model =loadModel()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    originalImage = cv2.imread(".\\test.jpg")
    print("chega aqui")
    result=cv2.imwrite(".\\test2.jpg", originalImage)
    print("chega aqui")
    image = cv2.imread("\images\\test2.png")
    image_fromarray = Image.fromarray(image, 'RGB')
    #resized_image = image_fromarray.resize((75, 75))
    #im = np.array(resized_image)
    return "done"


