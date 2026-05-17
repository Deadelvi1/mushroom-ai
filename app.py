from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import warnings
import json
import logging
warnings.filterwarnings('ignore')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup MLflow tracking
try:
    import mlflow
    MLFLOW_AVAILABLE = True
    
    # Configure MLflow with DagsHub
    dagshub_username = os.getenv('DAGSHUB_USERNAME')
    dagshub_repo = os.getenv('DAGSHUB_REPO')
    dagshub_token = os.getenv('DAGSHUB_TOKEN')
    mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
    
    if mlflow_tracking_uri and dagshub_token:
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        os.environ['MLFLOW_TRACKING_USERNAME'] = dagshub_username or ''
        os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token
        logger_msg = f"✅ MLflow configured for DagsHub: {mlflow_tracking_uri}"
    else:
        logger_msg = "⚠️  DagsHub credentials not found. Using local MLflow."
except ImportError:
    MLFLOW_AVAILABLE = False
    logger_msg = "⚠️  MLflow not installed. Experiment tracking disabled."

# Setup logging for monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info(logger_msg)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Disable caching for development
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Mapping untuk fitur-fitur (HARUS didefinisikan SEBELUM digunakan)
FEATURE_MAPPING = {
    'cap-shape': {
        'b': 'Bell', 'c': 'Conical', 'x': 'Convex', 
        'f': 'Flat', 'k': 'Knobbed', 's': 'Sunken'
    },
    'cap-surface': {
        'f': 'Fibrous', 'g': 'Grooves', 'y': 'Scaly', 's': 'Smooth'
    },
    'cap-color': {
        'n': 'Brown', 'b': 'Buff', 'c': 'Cinnamon', 'g': 'Gray',
        'r': 'Green', 'p': 'Pink', 'u': 'Purple', 'e': 'Red',
        'w': 'White', 'y': 'Yellow'
    },
    'bruises': {'t': 'Yes', 'f': 'No'},
    'odor': {
        'a': 'Almond', 'l': 'Anise', 'c': 'Creosote', 'y': 'Fishy',
        'f': 'Foul', 'm': 'Musty', 'n': 'None', 'p': 'Pungent', 's': 'Spicy'
    },
    'gill-attachment': {
        'a': 'Attached', 'd': 'Descending', 'f': 'Free', 'n': 'Notched'
    },
    'gill-spacing': {
        'c': 'Close', 'w': 'Crowded', 'd': 'Distant'
    },
    'gill-size': {'b': 'Broad', 'n': 'Narrow'},
    'gill-color': {
        'k': 'Black', 'n': 'Brown', 'b': 'Buff', 'h': 'Chocolate',
        'g': 'Gray', 'r': 'Green', 'o': 'Orange', 'p': 'Pink',
        'u': 'Purple', 'e': 'Red', 'w': 'White', 'y': 'Yellow'
    },
    'stalk-shape': {'e': 'Enlarging', 't': 'Tapering'},
    'stalk-root': {
        'b': 'Bulbous', 'c': 'Club', 'u': 'Cup', 'e': 'Equal',
        'z': 'Rhizomorphs', 'r': 'Rooted', '?': 'Missing', 'missing': 'Missing'
    },
    'stalk-surface-above-ring': {
        'f': 'Fibrous', 'y': 'Scaly', 'k': 'Silky', 's': 'Smooth'
    },
    'stalk-surface-below-ring': {
        'f': 'Fibrous', 'y': 'Scaly', 'k': 'Silky', 's': 'Smooth'
    },
    'stalk-color-above-ring': {
        'n': 'Brown', 'b': 'Buff', 'c': 'Cinnamon', 'g': 'Gray',
        'o': 'Orange', 'p': 'Pink', 'e': 'Red', 'w': 'White', 'y': 'Yellow'
    },
    'stalk-color-below-ring': {
        'n': 'Brown', 'b': 'Buff', 'c': 'Cinnamon', 'g': 'Gray',
        'o': 'Orange', 'p': 'Pink', 'e': 'Red', 'w': 'White', 'y': 'Yellow'
    },
    'veil-color': {'n': 'Brown', 'o': 'Orange', 'w': 'White', 'y': 'Yellow'},
    'ring-number': {'n': 'None', 'o': 'One', 't': 'Two'},
    'ring-type': {
        'e': 'Evanescent', 'f': 'Flaring', 'c': 'Cobwebby', 
        'l': 'Large', 'n': 'None', 'p': 'Pendant', 's': 'Sheathing', 'z': 'Zone'
    },
    'spore-print-color': {
        'k': 'Black', 'n': 'Brown', 'b': 'Buff', 'h': 'Chocolate',
        'r': 'Green', 'o': 'Orange', 'u': 'Purple', 'w': 'White', 'y': 'Yellow'
    },
    'population': {
        'a': 'Abundant', 'c': 'Clustered', 'n': 'Numerous',
        's': 'Scattered', 'v': 'Several', 'y': 'Solitary'
    },
    'habitat': {
        'g': 'Grasses', 'l': 'Leaves', 'm': 'Meadows',
        'p': 'Paths', 'u': 'Urban', 'w': 'Waste', 'd': 'Woods'
    }
}

# ==================== BUILD REVERSE ENCODERS ====================

def build_reverse_encoders(feature_mapping, encoders):
    """Build reverse mapping: numeric index -> human readable value"""
    reverse_map = {}
    
    for col in feature_mapping:
        if col in encoders and isinstance(encoders[col], dict):
            # encoders[col] is code -> index mapping
            # Reverse it to index -> human readable
            code_to_readable = feature_mapping[col]
            index_to_code = {v: k for k, v in encoders[col].items()}
            
            reverse_map[col] = {}
            for idx, code in index_to_code.items():
                if code in code_to_readable:
                    reverse_map[col][idx] = code_to_readable[code]
    
    return reverse_map

# ==================== LOAD MODEL & ENCODER ====================

model = None
encoders = None
required_features_list = None
features_order = None
reverse_encoders = None
model_metrics = None  # Store model evaluation metrics
model_info = {}  # Store model metadata

try:
    model = joblib.load('model/model.pkl')
    encoders = joblib.load('model/encoder.pkl')
    # Pre-cache required features untuk speed
    required_features_list = [f for f in encoders.keys() if f != 'poisonous']
    features_order = required_features_list.copy()
    # Build reverse encoders untuk hasil prediksi
    reverse_encoders = build_reverse_encoders(FEATURE_MAPPING, encoders)
    
    # Try to load model evaluation metrics
    try:
        if os.path.exists('model/metrics.json'):
            with open('model/metrics.json', 'r') as f:
                model_metrics = json.load(f)
                logger.info(f"✓ Model metrics loaded: {model_metrics}")
        else:
            logger.warning("⚠ Model metrics file not found. Run training to generate.")
            model_metrics = {}
    except Exception as e:
        logger.warning(f"⚠ Could not load metrics: {e}")
        model_metrics = {}
    
    # Store model metadata
    model_info = {
        'status': 'loaded',
        'loaded_at': datetime.now().isoformat(),
        'features_count': len(required_features_list),
        'has_metrics': bool(model_metrics)
    }
    
    print("✓ Model berhasil dimuat dari model/ folder")
    print(f"✓ Features cached: {len(required_features_list)} features")
    print(f"✓ Reverse encoders built: {len(reverse_encoders)} mappings")
    if model_metrics:
        print(f"✓ Model Metrics: Accuracy={model_metrics.get('accuracy', 'N/A'):.2%}")
except FileNotFoundError as e:
    logger.error(f"❌ Model tidak ditemukan: {e}")
    print(f"⚠ Model tidak ditemukan: {e}")
    print("  Jalankan: python model/train_model.py")
    model = None
    encoders = None
    reverse_encoders = None
    model_metrics = None
    model_info = {'status': 'not_loaded', 'error': str(e)}

# Riwayat prediksi
prediction_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    return render_template('predict.html', features=FEATURE_MAPPING)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if model is None or encoders is None:
        error_msg = 'Model belum dimuat. Jalankan: python model/train_model.py'
        logger.error(f"❌ {error_msg}")
        return jsonify({'error': error_msg, 'code': 'MODEL_NOT_LOADED'}), 503
    
    try:
        data = request.json
        
        if not data:
            logger.warning("⚠ Prediction request received with no data")
            return jsonify({'error': 'Data tidak diterima', 'code': 'NO_DATA'}), 400
        
        # Fast validation - gunakan pre-cached list
        missing_features = [f for f in required_features_list if f not in data]
        
        if missing_features:
            logger.warning(f"⚠ Missing features: {missing_features}")
            return jsonify({
                'error': f'Fitur yang hilang: {", ".join(missing_features)}',
                'code': 'MISSING_FEATURES',
                'missing': missing_features
            }), 400
        
        # Buat numpy array langsung (lebih cepat dari DataFrame)
        encoded_values = []
        
        for col in features_order:
            try:
                raw_value = data[col]
                
                # Handle encoder - it's now a dict mapping codes to numeric indices
                if isinstance(encoders[col], dict):
                    # encoders[col] maps codes to numeric indices
                    if raw_value not in encoders[col]:
                        logger.warning(f"⚠ Invalid value for {col}: {raw_value}")
                        return jsonify({
                            'error': f'Nilai tidak valid untuk {col}: {raw_value}',
                            'code': 'INVALID_VALUE',
                            'field': col,
                            'received': raw_value,
                            'valid_options': list(encoders[col].keys())
                        }), 400
                    encoded_value = encoders[col][raw_value]
                else:
                    # Legacy support for sklearn LabelEncoder
                    encoded_value = encoders[col].transform([raw_value])[0]
                
                encoded_values.append(encoded_value)
            except (ValueError, KeyError) as e:
                logger.error(f"❌ Encoding error for {col}: {str(e)}")
                return jsonify({
                    'error': f'Nilai tidak valid untuk {col}: {str(e)}',
                    'code': 'ENCODING_ERROR',
                    'field': col
                }), 400
        
        # Convert ke numpy array untuk prediksi
        input_array = np.array([encoded_values])
        
        # Prediksi langsung dari numpy array (lebih cepat)
        try:
            prediction = model.predict(input_array)[0]
            probability = model.predict_proba(input_array)[0]
        except Exception as e:
            logger.error(f"❌ Model prediction failed: {str(e)}")
            return jsonify({
                'error': f'Error dalam prediksi model: {str(e)}',
                'code': 'PREDICTION_FAILED'
            }), 500
        
        result = 'POISONOUS' if prediction == 1 else 'EDIBLE'
        confidence = float(max(probability)) * 100
        
        # Build mapped input data untuk response (konversi dari code ke human-readable)
        mapped_input = {}
        for col in required_features_list:
            raw_value = data[col]
            if col in FEATURE_MAPPING and raw_value in FEATURE_MAPPING[col]:
                mapped_input[col] = FEATURE_MAPPING[col][raw_value]
            else:
                mapped_input[col] = raw_value
        
        # Simpan ke history
        history_item = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'prediction': result,
            'confidence': confidence,
            'input': data,
            'input_mapped': mapped_input,
            'status': 'success'
        }
        prediction_history.append(history_item)
        
        # Batas history 100 item
        if len(prediction_history) > 100:
            prediction_history.pop(0)
        
        logger.info(f"✓ Prediction: {result} (confidence: {confidence:.2f}%)")
        
        return jsonify({
            'success': True,
            'prediction': result,
            'confidence': round(confidence, 2),
            'probability_poisonous': round(float(probability[1]) * 100, 2),
            'probability_edible': round(float(probability[0]) * 100, 2),
            'risk_level': 'HIGH' if confidence > 85 else 'MEDIUM' if confidence > 70 else 'LOW',
            'input_mapped': mapped_input,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"❌ Prediction error: {str(e)}", exc_info=True)
        return jsonify({
            'error': f'Error prediksi: {str(e)}',
            'code': 'INTERNAL_ERROR'
        }), 500

@app.route('/api/history')
def get_history():
    return jsonify(prediction_history[-10:])

@app.route('/api/stats')
def get_stats():
    if not prediction_history:
        return jsonify({
            'total': 0,
            'poisonous': 0,
            'edible': 0,
            'avg_confidence': 0
        })
    
    total = len(prediction_history)
    poisonous = sum(1 for item in prediction_history if item['prediction'] == 'POISONOUS')
    edible = total - poisonous
    avg_confidence = sum(item['confidence'] for item in prediction_history) / total
    
    return jsonify({
        'total': total,
        'poisonous': poisonous,
        'edible': edible,
        'avg_confidence': round(avg_confidence, 2)
    })

@app.route('/api/model-metrics')
def get_model_metrics():
    """Get model evaluation metrics from training"""
    if not model_metrics:
        return jsonify({
            'status': 'no_metrics',
            'message': 'Model metrics not available. Run training script to generate.'
        }), 404
    
    return jsonify({
        'status': 'success',
        'metrics': model_metrics,
        'loaded_at': datetime.now().isoformat()
    })

@app.route('/api/model-info')
def get_model_info():
    """Get model information and status"""
    info = {
        'model_status': model_info.get('status', 'unknown'),
        'model_loaded': model is not None,
        'encoders_loaded': encoders is not None,
        'features_count': len(required_features_list) if required_features_list else 0,
        'has_evaluation_metrics': bool(model_metrics),
        'loaded_at': model_info.get('loaded_at'),
        'total_predictions': len(prediction_history),
        'evaluation_metrics': model_metrics if model_metrics else None
    }
    
    logger.info(f"Model info requested: {info}")
    return jsonify(info)

if __name__ == '__main__':
    # Production mode - no debug, faster performance
    app.run(debug=False, host='0.0.0.0', port=8000, threaded=True)
