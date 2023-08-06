import tensorflow as tf

def create_model(LOSS,OPTIMIZER,METRICS,OUTPUT_CLASSES):
    LAYERS = [
          tf.keras.layers.Flatten(input_shape=[28,28], name="inputlayer"),
          tf.keras.layers.Dense(300,activation="relu", name="hiddenlayer1"),
          tf.keras.layers.Dense(100,activation="relu", name="hiddenlayer2"),
          tf.keras.layers.Dense(OUTPUT_CLASSES,activation="relu", name="outputlayer")] 

    model_tf = tf.keras.models.Sequential(LAYERS)

    model_tf.compile(loss=LOSS,optimizer=OPTIMIZER,metrics=METRICS)
    return model_tf

