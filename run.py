import streamlit as st
from keras.models import load_model
from DataManager import *
from glob import glob
from datetime import date, timedelta, datetime
from scipy.stats import multivariate_normal
import plotly.graph_objects as go

models = glob('Model/*.h5')
models_name = [i[6:] for i in models]
models_name.sort()

model_name = st.sidebar.selectbox(
    'Which model do you choice?',
    models_name
)

start = st.sidebar.date_input('Start Date:',
                              date.today() - timedelta(days=1))
# end = st.sidebar.date_input('End Date:')


model = load_model('./Model/%s' % model_name)

test = getPIData(model_name[:-3], start.strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d %H:00:00"))
test_arg = addFeature(test)
test_norm = normalize(test_arg)

X_test, Y_test = buildTrain(test_norm, 12 * 12, 1)
shape = Y_test.shape[0]
dt = pd.DataFrame({
    'true_y': np.reshape(Y_test, shape),
    'pred_y': np.reshape(model.predict(X_test), shape)
})

dt.index = test.tail(Y_test.shape[0]).index

dt['error'] = dt.pred_y - dt.true_y
dt['mulTest'] = multivariate_normal.pdf(dt.error, mean=dt.error.mean(), cov=dt.error.std())
dt['LogLikehood'] = dt.mulTest.rolling(12, min_periods=1).aggregate(multi).shift(-11).fillna(0)

s = st.sidebar.slider('敏感度', 40, 80, 60)
dt['IsAlarm'] = [1 if i > s else 0 for i in dt.LogLikehood]

fig = go.Figure()
fig.update_layout(
    xaxis_title='Date Time',
    yaxis_title='log(Y)',
    title='GateWay Discharge Monitor <br>Time : %s ~ %s'
          % (start.strftime("%Y-%m-%d 00:00:00"), datetime.now().strftime("%Y-%m-%d %H:00:00")),
    yaxis=dict(
        range=[10, 25]
    )
)

fig.add_trace(go.Scatter(x=dt.index, y=dt.true_y,
                         mode='lines',
                         name='Total Discharge')
              )

fig.add_trace(go.Scatter(x=dt.index, y=dt.true_y.where(dt.IsAlarm == 1),
                         mode='lines',
                         name='Anomaly Detection'))

st.plotly_chart(fig)