import cv2
import numpy as np
import os
import time

# Lazy loading - models will load only when needed
_skin_type_model = None
_condition_model = None
_MODELS_LOADED = False

def load_models():
    """Load models only when first analysis is requested"""
    global _skin_type_model, _condition_model, _MODELS_LOADED
    
    if _MODELS_LOADED:
        return True
    
    print("🔄 Loading AI models...")
    start_time = time.time()
    
    try:
        from tensorflow.keras.models import load_model
        
        MODELS_DIR = 'models'
        
        # Load skin type model
        skin_type_path = os.path.join(MODELS_DIR, 'skin_type_model.h5')
        if os.path.exists(skin_type_path):
            _skin_type_model = load_model(skin_type_path)
            print(f"✅ Skin type model loaded in {time.time()-start_time:.1f}s")
        else:
            print(f"⚠ Skin type model not found at {skin_type_path}")
        
        # Load condition model
        condition_path = os.path.join(MODELS_DIR, 'skin_condition_model.h5')
        if os.path.exists(condition_path):
            _condition_model = load_model(condition_path)
            print(f"✅ Condition model loaded in {time.time()-start_time:.1f}s")
        else:
            print(f"⚠ Condition model not found at {condition_path}")
        
        _MODELS_LOADED = True
        return True
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False

# Class names
SKIN_TYPE_CLASSES = ['dry', 'normal', 'oily']
CONDITION_CLASSES = ['Acne', 'Open_pores', 'Pigmentation', 'clear']

def preprocess_image(image_path, target_size=(224, 224)):
    """Load and preprocess image for model input"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, target_size)
        img_norm = img_resized / 255.0
        img_batch = np.expand_dims(img_norm, axis=0)
        
        return img_batch, img_rgb
    
    except Exception as e:
        print(f"❌ Error preprocessing image: {e}")
        return None, None

def analyze_skin(image_path):
    """Analyze skin image using trained models"""
    try:
        # Load models if not already loaded
        load_models()
        
        # Preprocess image
        img_tensor, original_img = preprocess_image(image_path)
        if img_tensor is None:
            return {
                "skin_type": "Unknown",
                "confidence": 0.0,
                "issues": []
            }
        
        results = {
            "skin_type": "Unknown",
            "confidence": 0.0,
            "issues": []
        }
        
        # ==================== SKIN TYPE PREDICTION ====================
        if _skin_type_model is not None:
            try:
                skin_pred = _skin_type_model.predict(img_tensor, verbose=0)[0]
                skin_class_idx = np.argmax(skin_pred)
                skin_confidence = float(skin_pred[skin_class_idx])
                
                if skin_class_idx < len(SKIN_TYPE_CLASSES):
                    skin_type = SKIN_TYPE_CLASSES[skin_class_idx]
                    results["skin_type"] = skin_type
                    results["confidence"] = skin_confidence
                    print(f"✅ Skin type: {skin_type} (confidence: {skin_confidence:.2f})")
            except Exception as e:
                print(f"❌ Skin type prediction error: {e}")
        
        # ==================== CONDITION PREDICTION ====================
        if _condition_model is not None:
            try:
                condition_pred = _condition_model.predict(img_tensor, verbose=0)[0]
                
                # Get values
                acne_conf = float(condition_pred[0])
                pores_conf = float(condition_pred[1])
                pigment_conf = float(condition_pred[2])
                clear_conf = float(condition_pred[3])
                
                print(f"\n📊 Model Values:")
                print(f"   Acne: {acne_conf:.3f}")
                print(f"   Open Pores: {pores_conf:.3f}")
                print(f"   Pigmentation: {pigment_conf:.3f}")
                print(f"   Clear: {clear_conf:.3f}")
                
                issues_detected = []
                
                # ===== SIMPLE APPROACH: Just use model with low thresholds =====
                
                # PIGMENTATION - Very low threshold to catch anything
                if pigment_conf > 0.25:  # Very low threshold
                    if pigment_conf > 0.7:
                        severity = "Severe"
                    elif pigment_conf > 0.5:
                        severity = "Moderate"
                    else:
                        severity = "Mild"
                    
                    issues_detected.append({
                        "issue": "Pigmentation",
                        "severity": severity
                    })
                    print(f"   ✓ Pigmentation detected: {severity} ({pigment_conf:.2f})")
                
                # ACNE
                if acne_conf > 0.35:
                    if acne_conf > 0.7:
                        severity = "Severe"
                    elif acne_conf > 0.5:
                        severity = "Moderate"
                    else:
                        severity = "Mild"
                    
                    issues_detected.append({
                        "issue": "Acne",
                        "severity": severity
                    })
                    print(f"   ✓ Acne detected: {severity} ({acne_conf:.2f})")
                
                # OPEN PORES
                if pores_conf > 0.50:
                    if pores_conf > 0.8:
                        severity = "Severe"
                    elif pores_conf > 0.65:
                        severity = "Moderate"
                    else:
                        severity = "Mild"
                    
                    issues_detected.append({
                        "issue": "Open Pores",
                        "severity": severity
                    })
                    print(f"   ✓ Open Pores detected: {severity} ({pores_conf:.2f})")
                
                # If we have too many issues, keep the highest ones
                if len(issues_detected) > 2:
                    # Sort by confidence
                    issues_detected.sort(key=lambda x: 
                        pigment_conf if x["issue"] == "Pigmentation" else
                        acne_conf if x["issue"] == "Acne" else pores_conf, 
                        reverse=True)
                    issues_detected = issues_detected[:2]
                
                results["issues"] = issues_detected
                
                if len(issues_detected) == 0:
                    print(f"✅ No issues detected")
                
            except Exception as e:
                print(f"❌ Condition error: {e}")
        
        return results
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return {
            "skin_type": "Unknown",
            "confidence": 0.0,
            "issues": []
        }