import numpy as np
import os
from numpy import asarray
from keras.models import load_model
from sklearn.preprocessing import Normalizer
from sklearn.metrics.pairwise import cosine_similarity
import cv2

def loadFacenetModel(modelPath: str = "models/facenet_keras.h5"):
    model = load_model(modelPath)
    print(f"[+] Loaded Facenet model from {modelPath}")
    return model

def preprocessFace(img):
    img = cv2.resize(img, (160, 160))
    img = img.astype('float32')
    mean, std = img.mean(), img.std()
    img = (img - mean) / std
    return asarray(img)

def getEmbedding(model, face):
    face = preprocessFace(face)
    face = np.expand_dims(face, axis=0)
    embedding = model.predict(face)[0]
    return embedding[0]

def matches(knownEmbedding, candidateEmbedding, threshold=0.2):
    score = cosine_similarity([knownEmbedding], [candidateEmbedding])[0][0]
    print(f"[+] Similarity score: {score}")
    return score >= threshold

def loadKnownFaces(model, faceDir: str = "media/faces"):
    knownFaces = {}
    l2_norm = Normalizer(norm='l2')
    
    for person in os.listdir(faceDir):
        personDir = os.path.join(faceDir, person)
        embeddings = []
        for file in os.listdir(personDir):
            if file.endswith('.jpg'):
                facePath = os.path.join(personDir, file)
                face = cv2.imread(facePath)
                if face is not None:
                    embedding = getEmbedding(model, face)
                    embedding = l2_norm.transform([embedding])[0]
                    embeddings.append(embedding)
                    
                if embeddings:
                    meanEmbedding = np.mean(embeddings, axis=0)
                    knownFaces[person] = meanEmbedding
                    print(f"[+] Encoded: {person}")
                    
    return knownFaces