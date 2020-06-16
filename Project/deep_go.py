import h5py

from keras.models import Sequential
from keras.layers import Dense

from dlgo.agent.predict import DeepLearningAgent, load_prediction_agent
from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.httpfrontend import get_web_app
from dlgo.networks import cnn

go_board_rows, go_board_cols = 19, 19
nb_classes = go_board_rows * go_board_cols
encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
processor = GoDataProcessor(encoder=encoder.name())

X, y = processor.load_go_data(num_samples=100)

#opt = SGD(lr=0.005)
model = cnn.Model.build(go_board_rows, go_board_cols,encoder.num_planes,nb_classes)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#model.fit(X, y, batch_size=128, epochs=20, verbose=1)

model.fit(X, y, batch_size=128, epochs=2, verbose=1)

deep_learning_bot = DeepLearningAgent(model, encoder)
with h5py.File('H5PY/deep_bot.h5', 'w') as outf:
    deep_learning_bot.serialize(outf)

model_file = h5py.File('H5PY/deep_bot.h5', 'r')
bot_from_file = load_prediction_agent(model_file)

web_app = get_web_app({ 'predict': bot_from_file })
web_app.run()
