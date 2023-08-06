import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras.callbacks import LambdaCallback
import plotly.offline as pyo
import plotly.graph_objs as go
# Set notebook mode to work in offline
pyo.init_notebook_mode()
import keras


class OptimizedLR():
    def __init__(self, mod, lr_end):
        self.model = mod
        self.lrs = []
        self.val_loss = []
        self.end_lr = lr_end

    def on_epoch_end(self, batch, logs):
        lr = keras.backend.get_value(self.model.optimizer.lr)
        self.lrs.append(lr)
        self.val_loss.append(logs['val_loss'])
        if len(self.val_loss) == 1:
            return
        if self.val_loss[-1] >= self.val_loss[-2]: #maybe change the decay of lr to an exp function
            lr = lr * 0.0002 ** (1 / 100)
            if lr <= self.end_lr:
                self.model.stop_training = True
            keras.backend.set_value(self.model.optimizer.lr, lr)
        elif self.val_loss[-1] >= 1.03 * self.val_loss[-2]:
            self.model.stop_training = True

    def search(self, X_train, y_train, validation=None, epochs=5, batch=32):
        if validation == None:
            raise Exception("Validation set should be included") # the validation should be Initialized at the call of this method
            
        cyclical_lr = tf.keras.callbacks.LambdaCallback(
            on_epoch_end=lambda batch, logs: self.on_epoch_end(batch, logs))
        self.model.fit(X_train, y_train, validation_data=validation, epochs=epochs, batch_size=batch,
                       callbacks=[cyclical_lr])

    def plot_loss(self):
        fig = go.Figure()

        sorted_lrs, sorted_val_loss = zip(*sorted(zip(self.lrs, self.val_loss)))

        fig.add_trace(
            go.Scatter(
                x=sorted_lrs,
                y=sorted_val_loss,
                mode='lines',
                line=dict(width=3)
            )
        )

        fig.update_layout(
            title='Validation Loss vs Learning Rate',
            xaxis=dict(
                title='Learning Rate',
                tickformat='.4e'
            ),
            yaxis=dict(
                title='Validation Loss',
                tickformat='.4e'

            ),
            width=800,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(size=14),
            # set the color of the title and axis labels
            title_font=dict(size=20),
            xaxis_title_font=dict(size=18),
            yaxis_title_font=dict(size=18)
        )

        # set the color of the gridlines

        # add a horizontal line to indicate the minimum validation loss
        fig.add_shape(
            type='line',
            x0=min(self.lrs), y0=min(self.val_loss),
            x1=max(self.lrs), y1=min(self.val_loss),
            line=dict(color='red', width=3, dash='dash')
        )
        fig.update_layout(template='plotly_dark')

        fig.show()
