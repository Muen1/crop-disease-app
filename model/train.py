# Train.py

import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models, Model
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam

# --- Config ---
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 15
TRAIN_DIR = "/content/plantvillage/dataset/train"
VAL_DIR = "/content/plantvillage/dataset/validation"
TEST_DIR = "/content/plantvillage/dataset/test"
MODEL_OUT = "model/plant_disease_model.h5"
CLASS_MAP_OUT = "model/class_indices.json"

def build_generators():
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True
    )
    eval_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
        class_mode="categorical", shuffle=True
    )
    val_gen = eval_datagen.flow_from_directory(
        VAL_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
        class_mode="categorical", shuffle=False
    )
    test_gen = eval_datagen.flow_from_directory(
        TEST_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
        class_mode="categorical", shuffle=False
    )
    return train_gen, val_gen, test_gen

def build_model(num_classes):
    base_model = EfficientNetB0(
        weights="imagenet", include_top=False,
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
    )
    base_model.trainable = True

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.4)(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

def main():
    train_gen, val_gen, test_gen = build_generators()
    num_classes = train_gen.num_classes
    print("Number of classes:", num_classes)
    print("Class indices:", train_gen.class_indices)

    model = build_model(num_classes)
    model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

    test_gen.reset()
    loss, acc = model.evaluate(test_gen)
    print(f"Test Accuracy: {acc:.4f}")

    os.makedirs("model", exist_ok=True)
    model.save(MODEL_OUT)

    with open(CLASS_MAP_OUT, "w") as f:
        json.dump(train_gen.class_indices, f, indent=2)

    print(f"Saved model to {MODEL_OUT}")
    print(f"Saved class mapping to {CLASS_MAP_OUT}")

main()
