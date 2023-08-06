import tensorflow as tf
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns

def create_model(LOSS,OPTIMIZER,METRICS,OUTPUT_CLASSES):
    LAYERS = [
          tf.keras.layers.Flatten(input_shape=[28,28], name="inputlayer"),
          tf.keras.layers.Dense(300,activation="relu", name="hiddenlayer1"),
          tf.keras.layers.Dense(100,activation="relu", name="hiddenlayer2"),
          tf.keras.layers.Dense(OUTPUT_CLASSES,activation="softmax", name="outputlayer")] 

    model_tf = tf.keras.models.Sequential(LAYERS)

    model_tf.compile(loss=LOSS,optimizer=OPTIMIZER,metrics=METRICS)
    return model_tf

def get_unique_filename(filename):
    unique_filename = time.strftime(f"%Y%m%d_%H%M%S_{filename}")
    return unique_filename

def save_model(model, model_name, model_dir):
    unique_filename = get_unique_filename(model_name)
    path_to_model = os.path.join(model_dir, unique_filename)
    model.save(path_to_model)

def save_plots(df, plots_name, plots_dir):
    unique_filename = get_unique_filename(plots_name)
    path_to_plot = os.path.join(plots_dir, unique_filename)
    df.plot(figsize=(10, 10))
    plt.grid(True)
    plt.savefig(path_to_plot)


