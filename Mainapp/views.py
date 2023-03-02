import pickle
import uuid
import tensorflow as tf

# ==== Machine Learning function ====
import math
import numpy as np
from django.shortcuts import render, redirect
from .preprocessor import preprocess
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load tokenization
tokenizer_path = "./Mainapp/model/tokenizer_1.pickle"
with open(tokenizer_path, 'rb') as handle:
    tokenizer: Tokenizer = pickle.load(handle)

# Load model
model_1 = tf.keras.models.load_model("./Mainapp/model/model1_fold_batch32_epoch20_lr0.0001.h5", compile=False)
model_2 = tf.keras.models.load_model("./Mainapp/model/model2_fold_batch32_epoch20_lr0.0001.h5", compile=False)
model_3 = tf.keras.models.load_model("./Mainapp/model/model3_fold_batch64_epoch20_lr0.001.h5", compile=False)
model_4 = tf.keras.models.load_model("./Mainapp/model/model4_fold_batch32_epoch10_lr0.001.h5", compile=False)

def predict_hate_speech(txt: 'str') -> 'int':
    """
    Returning int
    for 0 -> non hate speech
        1 -> hate speech
    """

    clean_text = preprocess(txt)
    clean_texts = [clean_text]
    seq = tokenizer.texts_to_sequences(clean_texts)
    seq = pad_sequences(seq)
    logits = model_1.predict(seq)
    prediction = logits[0][0]
    prediction = round(prediction)
    return prediction

class FullHateSpeechPrediction:
    def __init__(self, pred2, pred3, pred4) -> None:
        self.prediction_model_2_individual = pred2[0]
        self.prediction_model_2_group = pred2[1]
        self.prediction_model_3_religion = pred3[0]
        self.prediction_model_3_ras = pred3[1]
        self.prediction_model_3_physical = pred3[2]
        self.prediction_model_3_gender = pred3[3]
        self.prediction_model_4_weak = pred4[0]
        self.prediction_model_4_moderate = pred4[1]
        self.prediction_model_4_string = pred4[2]

def predict_full_hate_speech(txt: 'str') -> 'FullHateSpeechPrediction' :
    """
    Generating FullHateSpeechPrediction
    """
    clean_text = preprocess(txt)
    clean_texts = [clean_text]
    seq = tokenizer.texts_to_sequences(clean_texts)
    seq = pad_sequences(seq)
    prediction2 = model_2.predict(seq)[0]
    prediction3 = model_3.predict(seq)[0]
    prediction4 = model_4.predict(seq)[0]
    return FullHateSpeechPrediction(prediction2, prediction3, prediction4)

# ======================================

def get_predict_by_id(id: 'str') -> ...:
    pass

# Create your views here.
def index(request):
    dummy_text = """jangan asal ngomong ndasmu. congor lu yg seka."""
    
    prediction_hs = predict_hate_speech(dummy_text)
    print(prediction_hs)
    
    prediction_full = predict_full_hate_speech(dummy_text)
    print(
        prediction_full.prediction_model_2_individual,
        prediction_full.prediction_model_2_group,
        prediction_full.prediction_model_3_religion,
        prediction_full.prediction_model_3_ras,
        prediction_full.prediction_model_3_physical,
        prediction_full.prediction_model_3_gender,
        prediction_full.prediction_model_4_weak,
        prediction_full.prediction_model_4_moderate,
        prediction_full.prediction_model_4_string,
    )
    return render(request, 'index.html')

def predict(request):
    predict_id = str(uuid.uuid4())
    if request.method == "GET":
        return render(request, 'predict.html')
    if request.method == "POST":
        text = request.POST['text']
        
        # Predict
        hate_speech_predict = 0 # Label of hate speech or not a hate speech (default non hate speech)
        if (text.strip() != ""): # if text is not empty after preprocessing, predict to model
            hate_speech_predict = predict_hate_speech(text)
            full_prediction = predict_full_hate_speech(text)
            
        # TODO: Save to database
        
        if hate_speech_predict == 1: # Hate speech
            return redirect(f"/hate_speech_detail/{predict_id}")
        else:
            return redirect("/no_hate_speech")
            

def no_hate_speech(request):
    return render(request, 'no_hate_speech.html')

def hate_speech(request, id):
    # TODO: Check to database if prediction of certain id is hate speech
    
    return render(request, 'hate_speech.html')

def hate_speech_detail(request, id):
    # TODO: Check to databse if already predicted and a hate speech if not, then predict
    
    return render(request, 'hate_speech_detail.html')