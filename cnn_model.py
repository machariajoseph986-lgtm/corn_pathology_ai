import tensorflow as tf


# ============================================================
# MAIZE DISEASE CNN MODEL
# ============================================================

IMAGE_SIZE = 256
NUM_CHANNELS = 3
NUM_CLASSES = 4


def build_cnn_model():

    model = tf.keras.Sequential([

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------
        tf.keras.layers.Input(
            shape=(IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS)
        ),

        # ----------------------------------------------------
        # CONVOLUTIONAL BLOCK 1
        # 32 filters
        # ----------------------------------------------------
        tf.keras.layers.Conv2D(
            filters=32,
            kernel_size=(3, 3),
            activation="relu",
            padding="same"
        ),

        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.MaxPooling2D(
            pool_size=(2, 2)
        ),


        # ----------------------------------------------------
        # CONVOLUTIONAL BLOCK 2
        # 64 filters
        # ----------------------------------------------------
        tf.keras.layers.Conv2D(
            filters=64,
            kernel_size=(3, 3),
            activation="relu",
            padding="same"
        ),

        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.MaxPooling2D(
            pool_size=(2, 2)
        ),


        # ----------------------------------------------------
        # CONVOLUTIONAL BLOCK 3
        # 128 filters
        # ----------------------------------------------------
        tf.keras.layers.Conv2D(
            filters=128,
            kernel_size=(3, 3),
            activation="relu",
            padding="same"
        ),

        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.MaxPooling2D(
            pool_size=(2, 2)
        ),


        # ----------------------------------------------------
        # CONVOLUTIONAL BLOCK 4
        # 256 filters
        # ----------------------------------------------------
        tf.keras.layers.Conv2D(
            filters=256,
            kernel_size=(3, 3),
            activation="relu",
            padding="same"
        ),

        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.MaxPooling2D(
            pool_size=(2, 2)
        ),


        # ----------------------------------------------------
        # FEATURE AGGREGATION
        # ----------------------------------------------------
        tf.keras.layers.GlobalAveragePooling2D(),


        # ----------------------------------------------------
        # CLASSIFICATION HEAD
        # ----------------------------------------------------
        tf.keras.layers.Dense(
            128,
            activation="relu"
        ),

        tf.keras.layers.Dropout(
            0.4
        ),

        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------
        tf.keras.layers.Dense(
            NUM_CLASSES,
            activation="softmax"
        )

    ], name="maize_disease_cnn")


    return model


# ============================================================
# BUILD MODEL
# ============================================================

model = build_cnn_model()


# ============================================================
# DISPLAY ARCHITECTURE
# ============================================================

model.summary()