import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import matplotlib.pyplot as plt
import os
import json

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 100  # Increased from 30 to 100
SKIN_TYPE_DIR = 'dataset/skin_type'
CONDITIONS_DIR = 'dataset/conditions'

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# ==================== TRAIN SKIN TYPE MODEL ====================
def train_skin_type_model():
    print("="*60)
    print("🧴 TRAINING SKIN TYPE MODEL")
    print("="*60)
    
    # Data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8,1.2],
        validation_split=0.2
    )
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        SKIN_TYPE_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Load validation data
    validation_generator = train_datagen.flow_from_directory(
        SKIN_TYPE_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=True
    )
    
    # Get class names
    class_names = list(train_generator.class_indices.keys())
    print(f"\n✅ Skin type classes: {class_names}")
    print(f"✅ Training samples: {train_generator.samples}")
    print(f"✅ Validation samples: {validation_generator.samples}")
    
    # Save class names
    with open('skin_type_classes.json', 'w') as f:
        json.dump(class_names, f)
    
    # Build model with transfer learning
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False  # Freeze base model first
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(len(class_names), activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks for better training
    callbacks = [
        EarlyStopping(patience=15, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=7, min_lr=1e-6, verbose=1),
        ModelCheckpoint('models/skin_type_best.h5', save_best_only=True, verbose=1)
    ]
    
    # Train model
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save('models/skin_type_model.h5')
    print("✅ Skin type model saved to models/skin_type_model.h5")
    
    return history

# ==================== TRAIN CONDITIONS MODEL ====================
def train_conditions_model():
    print("\n" + "="*60)
    print("🔬 TRAINING CONDITIONS MODEL")
    print("="*60)
    
    # Data augmentation with more variety
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        brightness_range=[0.7,1.3],
        validation_split=0.2
    )
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        CONDITIONS_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Load validation data
    validation_generator = train_datagen.flow_from_directory(
        CONDITIONS_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=True
    )
    
    # Get class names
    class_names = list(train_generator.class_indices.keys())
    print(f"\n✅ Condition classes: {class_names}")
    print(f"✅ Training samples: {train_generator.samples}")
    print(f"✅ Validation samples: {validation_generator.samples}")
    
    # Save class names
    with open('condition_classes.json', 'w') as f:
        json.dump(class_names, f)
    
    # Build model with transfer learning
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.4),  # More dropout to prevent overfitting
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(len(class_names), activation='softmax')
    ])
    
    # Compile with lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks for better training
    callbacks = [
        EarlyStopping(patience=20, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(factor=0.5, patience=8, min_lr=1e-6, verbose=1),
        ModelCheckpoint('models/skin_condition_best.h5', save_best_only=True, verbose=1)
    ]
    
    # Train model
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save('models/skin_condition_model.h5')
    print("✅ Conditions model saved to models/skin_condition_model.h5")
    
    return history

# ==================== MAIN ====================
if __name__ == "__main__":
    print("="*60)
    print("🚀 TRAINING BOTH MODELS WITH 100 EPOCHS")
    print("="*60)
    
    # Train skin type model
    skin_history = train_skin_type_model()
    
    # Train conditions model
    cond_history = train_conditions_model()
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("✅ Models saved in 'models' folder")
    print("="*60)