from keras.models import load_model
from DataManager import *


def loadModel(name):
    model = load_model('./Model/%s.h5' % name)
    return model


def predict(tag):
    test = getPIData(tag, '2019-11-05', '2019-11-06')
    test_arg = addFeature(test)
    test_norm = normalize(test_arg)

    X_test, Y_test = buildTrain(test_norm, 12 * 12, 1)

    model = loadModel(tag)

    return model.predict(X_test)


print(predict('USG60_eth0_ifInOctets'))
