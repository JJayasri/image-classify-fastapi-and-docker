from fastapi import FastAPI, File, UploadFile

import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()
MODEL = tf.keras.models.load_model("./models/1")

CLASS_NAMES = [0,1,2,3]

@app.get("/ping")
async def ping():
    return "Image Classification API"
input_shape=(224,224)
def read_image(data):
    x=Image.open(BytesIO(data)).convert("RGB")
    x=x.resize((input_shape))
    image = np.array(x)
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image=read_image(await file.read())
    image=image/225.0
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }
    


