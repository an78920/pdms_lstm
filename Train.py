from DataManager import *

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import EarlyStopping


def buildManyToOneModel(shape):
    model = Sequential()
    model.add(LSTM(16, input_shape=(shape[1], shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')
    model.summary()

    return model


def trainAndSaveModel(tag):
    train = getPIData(tag, '2019-10-20', '2019-11-13')
    train_arg = addFeature(train)
    train_norm = normalize(train_arg)

    X_train, Y_train = buildTrain(train_norm, 12 * 12, 1)
    X_train, Y_train, X_val, Y_val = splitData(X_train, Y_train, 0.2)

    model = buildManyToOneModel(X_train.shape)
    callback = EarlyStopping(monitor='loss', patience=10, verbose=1, mode='auto')
    model.fit(X_train, Y_train,
              epochs=10,
              batch_size=512,
              validation_data=(X_val, Y_val),
              callbacks=[callback])

    model.save('./Model/%s.h5' % tag)


trainAndSaveModel('USG60_eth0_ifInOctets')
#trainAndSaveModel('USG60_eth0_ifOutOctets')
#trainAndSaveModel('USG60_eth1_ifInOctets')
#trainAndSaveModel('USG60_eth1_ifOutOctets')
#trainAndSaveModel('USG60_eth2_ifInOctets')
#trainAndSaveModel('USG60_eth2_ifOutOctets')