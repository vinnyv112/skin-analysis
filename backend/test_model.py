import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import mediapipe as mp
import random

# ==================== CONFIGURATION ====================
IMG_SIZE = 224
SKIN_TYPE_CLASSES = ['dry', 'normal', 'oily']
SKIN_CONDITION_CLASSES = ['acne', 'open_pores', 'pigmentation']

# Initialize mediapipe correctly for version 0.10.32
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Load trained models
def load_trained_models():
    models = {}
    
    # Load skin type model
    skin_type_path = 'models/skin_type_model.h5'
    if os.path.exists(skin_type_path):
        try:
            models['skin_type'] = load_model(skin_type_path)
            print(f"✅ Loaded skin type model from: {skin_type_path}")
        except Exception as e:
            print(f"⚠ Error loading skin type model: {e}")
            models['skin_type'] = None
    else:
        print(f"⚠ Skin type model not found at: {skin_type_path}")
        models['skin_type'] = None
    
    # Load skin condition model
    skin_condition_path = 'models/skin_condition_model.h5'
    if os.path.exists(skin_condition_path):
        try:
            models['skin_condition'] = load_model(skin_condition_path)
            print(f"✅ Loaded skin condition model from: {skin_condition_path}")
        except Exception as e:
            print(f"⚠ Error loading skin condition model: {e}")
            models['skin_condition'] = None
    else:
        print(f"⚠ Skin condition model not found at: {skin_condition_path}")
        models['skin_condition'] = None
    
    return models

def preprocess_image(image_path):
    """Load and preprocess image for model input"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"❌ Cannot load image: {image_path}")
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
    img_norm = img_resized / 255.0
    return np.expand_dims(img_norm, axis=0), img_rgb, img

def predict_skin_type(model, img_tensor):
    """Predict skin type using trained model"""
    if model is None:
        # Fallback random prediction
        skin_type = random.choice(SKIN_TYPE_CLASSES)
        confidence = random.uniform(0.6, 0.9)
        print(f"⚠ Using random fallback: {skin_type}")
        return skin_type, confidence
    
    try:
        predictions = model.predict(img_tensor, verbose=0)[0]
        class_index = np.argmax(predictions)
        confidence = float(predictions[class_index])
        
        if class_index < len(SKIN_TYPE_CLASSES):
            skin_type = SKIN_TYPE_CLASSES[class_index]
        else:
            skin_type = "normal"
        
        return skin_type, confidence
    except Exception as e:
        print(f"⚠ Prediction error: {e}")
        return "normal", 0.5

def predict_skin_conditions(model, img_tensor, img_rgb):
    """Predict skin conditions using trained model + mediapipe"""
    conditions = []
    
    # Model prediction
    if model is not None:
        try:
            predictions = model.predict(img_tensor, verbose=0)[0]
            threshold = 0.3
            
            for i, confidence in enumerate(predictions):
                if confidence > threshold and i < len(SKIN_CONDITION_CLASSES):
                    severity = "Mild"
                    if confidence > 0.7:
                        severity = "Severe"
                    elif confidence > 0.5:
                        severity = "Moderate"
                    
                    conditions.append({
                        "issue": SKIN_CONDITION_CLASSES[i].replace('_', ' ').title(),
                        "severity": severity,
                        "confidence": float(confidence)
                    })
            print(f"✅ Model detected {len(conditions)} conditions")
        except Exception as e:
            print(f"⚠ Model prediction error: {e}")
    
    # MediaPipe enhancement
    try:
        mp_conditions = detect_with_mediapipe(img_rgb)
        
        # Merge results
        if mp_conditions:
            existing = [c['issue'] for c in conditions]
            for mp_c in mp_conditions:
                if mp_c['issue'] not in existing:
                    conditions.append(mp_c)
    except Exception as e:
        print(f"⚠ MediaPipe error (non-critical): {e}")
    
    return conditions

def detect_with_mediapipe(img_rgb):
    """Use MediaPipe for additional condition detection"""
    conditions = []
    
    # Process the image
    results = face_mesh.process(img_rgb)
    
    if not results.multi_face_landmarks:
        return conditions
    
    h, w, _ = img_rgb.shape
    
    for face_landmarks in results.multi_face_landmarks:
        # 1. Acne detection (redness in cheeks)
        for cheek_idx in [234, 454]:  # Left and right cheek
            x = int(face_landmarks.landmark[cheek_idx].x * w)
            y = int(face_landmarks.landmark[cheek_idx].y * h)
            
            # Ensure coordinates are within image bounds
            x = max(0, min(x, w-1))
            y = max(0, min(y, h-1))
            
            roi = img_rgb[max(0, y-30):min(h, y+30), max(0, x-30):min(w, x+30)]
            if roi.size > 0:
                hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
                red_mask = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255)) | cv2.inRange(hsv, (160, 50, 50), (180, 255, 255))
                red_ratio = np.sum(red_mask > 0) / (roi.shape[0] * roi.shape[1] + 1e-5)
                
                if red_ratio > 0.08 and not any(c['issue'] == 'Acne' for c in conditions):
                    conditions.append({"issue": "Acne", "severity": "Moderate" if red_ratio > 0.12 else "Mild"})
        
        # 2. Open pores detection (T-zone)
        nose_y = int(face_landmarks.landmark[1].y * h)
        nose_x = int(face_landmarks.landmark[1].x * w)
        
        nose_y = max(0, min(nose_y, h-1))
        nose_x = max(0, min(nose_x, w-1))
        
        roi = img_rgb[max(0, nose_y-40):min(h, nose_y+40), max(0, nose_x-40):min(w, nose_x+40)]
        
        if roi.size > 0:
            gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
            variance = np.var(gray)
            if variance > 800 and not any(c['issue'] == 'Open Pores' for c in conditions):
                conditions.append({"issue": "Open Pores", "severity": "Moderate" if variance > 1000 else "Mild"})
        
        # 3. Pigmentation detection
        sample_points = [234, 454, 10]  # cheeks and forehead
        l_values = []
        for point in sample_points:
            x = int(face_landmarks.landmark[point].x * w)
            y = int(face_landmarks.landmark[point].y * h)
            
            x = max(0, min(x, w-1))
            y = max(0, min(y, h-1))
            
            roi = img_rgb[max(0, y-15):min(h, y+15), max(0, x-15):min(w, x+15)]
            if roi.size > 0:
                lab = cv2.cvtColor(roi, cv2.COLOR_RGB2LAB)
                l_values.append(np.mean(lab[:, :, 0]))
        
        if l_values and np.var(l_values) > 80 and not any(c['issue'] == 'Pigmentation' for c in conditions):
            conditions.append({"issue": "Pigmentation", "severity": "Moderate" if np.var(l_values) > 120 else "Mild"})
    
    return conditions

def display_result(image, skin_type, confidence, conditions):
    """Display the analysis results on image"""
    # Create a copy for display
    display_img = image.copy()
    
    # Add text overlay
    cv2.putText(display_img, f"Skin Type: {skin_type.upper()} ({confidence:.2f})", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    y_offset = 60
    for i, condition in enumerate(conditions[:5]):  # Show max 5 conditions
        text = f"{condition['issue']}: {condition['severity']}"
        if 'confidence' in condition:
            text += f" ({condition['confidence']:.2f})"
        cv2.putText(display_img, text, (10, y_offset + i*25), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    return display_img

def test_single_image(image_path, models):
    """Test analysis on a single image"""
    print(f"\n{'='*60}")
    print(f"🔍 Testing image: {image_path}")
    print(f"{'='*60}")
    
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            return None
        
        # Preprocess
        img_tensor, img_rgb, original_img = preprocess_image(image_path)
        print(f"✅ Image loaded: {original_img.shape}")
        
        # Skin type prediction
        skin_type, confidence = predict_skin_type(models['skin_type'], img_tensor)
        print(f"\n📊 Skin Type: {skin_type.upper()} (Confidence: {confidence:.2f})")
        
        # Skin conditions prediction
        conditions = predict_skin_conditions(models['skin_condition'], img_tensor, img_rgb)
        
        print(f"\n🔍 Detected Conditions:")
        if conditions:
            for condition in conditions:
                conf_text = f" (conf: {condition.get('confidence', 0):.2f})" if 'confidence' in condition else ""
                print(f"   • {condition['issue']}: {condition['severity']}{conf_text}")
        else:
            print("   • No specific conditions detected")
            conditions = [{"issue": "Normal Skin", "severity": "None"}]
        
        # Display result
        result_img = display_result(original_img, skin_type, confidence, conditions)
        
        # Show image
        cv2.imshow('Skin Analysis Result', result_img)
        print("\n⏎ Press any key in the image window to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Save result
        output_path = f"result_{os.path.basename(image_path)}"
        cv2.imwrite(output_path, result_img)
        print(f"\n✅ Result saved as: {output_path}")
        
        return {
            'skin_type': skin_type,
            'confidence': confidence,
            'conditions': conditions
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_multiple_images(image_folder, models):
    """Test all images in a folder"""
    print(f"\n{'='*60}")
    print(f"🔍 Testing all images in folder: {image_folder}")
    print(f"{'='*60}")
    
    if not os.path.exists(image_folder):
        print(f"❌ Folder not found: {image_folder}")
        return
    
    image_files = [f for f in os.listdir(image_folder) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("❌ No images found in folder")
        return
    
    print(f"Found {len(image_files)} images\n")
    
    results = []
    for i, img_file in enumerate(image_files):
        print(f"\n[{i+1}/{len(image_files)}] Processing...")
        img_path = os.path.join(image_folder, img_file)
        result = test_single_image(img_path, models)
        if result:
            results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}")
    
    if results:
        skin_types = [r['skin_type'] for r in results]
        print(f"Skin Type Distribution:")
        for st in set(skin_types):
            print(f"   • {st}: {skin_types.count(st)} images")
    else:
        print("No results to summarize")

# ==================== MAIN TEST ====================
if __name__ == "__main__":
    print("="*60)
    print("🧪 SKIN ANALYSIS MODEL TESTER")
    print("="*60)
    print(f"MediaPipe version: {mp.__version__}")
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    print(f"Models folder exists: {os.path.exists('models')}")
    
    # Load models
    models = load_trained_models()
    
    while True:
        print("\n" + "="*60)
        print("Choose test option:")
        print("1. Test a single image")
        print("2. Test all images in a folder")
        print("3. Test with sample (if you have a test image)")
        print("4. Check model info")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            img_path = input("Enter image path: ").strip()
            if os.path.exists(img_path):
                test_single_image(img_path, models)
            else:
                print("❌ File not found!")
        
        elif choice == '2':
            folder_path = input("Enter folder path: ").strip()
            test_multiple_images(folder_path, models)
        
        elif choice == '3':
            # Check for common test images
            test_images = ['test.jpg', 'test.png', 'sample.jpg', 'face.jpg']
            found = False
            for test_img in test_images:
                if os.path.exists(test_img):
                    test_single_image(test_img, models)
                    found = True
                    break
            if not found:
                print("❌ No test image found. Please place a test image in the current folder.")
        
        elif choice == '4':
            print("\n📊 Model Information:")
            print(f"   Skin Type Model: {'✅ Loaded' if models['skin_type'] else '❌ Not loaded'}")
            print(f"   Skin Condition Model: {'✅ Loaded' if models['skin_condition'] else '❌ Not loaded'}")
            
            if os.path.exists('models'):
                print(f"\n   Files in models folder:")
                for f in os.listdir('models'):
                    file_path = os.path.join('models', f)
                    size = os.path.getsize(file_path) / (1024*1024)  # Size in MB
                    print(f"   • {f} ({size:.2f} MB)")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice!")