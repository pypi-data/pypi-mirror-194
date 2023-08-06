import joblib
import utils

def segmenter(text):
    model = joblib.load('models/segmenter.sav')
    text = text.split()
    X_test = []
    for index, word in enumerate(text):
        f = utils.features(text, index)
        X_test.append(f)

    y_pred = model.predict_single(X_test)

    text_ = ''
    for c, t in zip(text, y_pred):
        text_ = text_ + c + t 
    text_ = text_.strip(' SB')
    text_ = text_.replace('S', ' ').split('B')

    return text_
