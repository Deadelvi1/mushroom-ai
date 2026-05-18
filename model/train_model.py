import pandas as pd
import numpy as np
import joblib
import os
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# DagsHub & MLflow Integration
try:
    import mlflow
    import dagshub
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("⚠️  MLflow/DagsHub not installed. Skipping experiment tracking.")

# ==================== DATASET LOADING ====================

def load_dataset():
    """Load mushroom dataset dari UCI ML Repository"""
    
    print("\n📥 Loading Mushroom Dataset from UCI ML Repository...")
    
    try:
        from ucimlrepo import fetch_ucirepo
        
        # Fetch dataset
        mushroom = fetch_ucirepo(id=73)
        
        X = mushroom.data.features
        y = mushroom.data.targets
        
        df = pd.concat([X, y], axis=1)
        
        print(f"✅ Dataset loaded successfully!")
        print(f"   Shape: {df.shape}")
        print(f"   Features: {len(X.columns)}")
        
        return df
    
    except ImportError:
        print("⚠️  ucimlrepo not installed. Please run: pip install ucimlrepo")
        return None
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

# ==================== DATA MAPPING ====================

def get_feature_mapping():
    """Return feature mapping dictionary"""
    
    return {
        'poisonous': {
            'e': 'Edible',
            'p': 'Poisonous'
        },
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
        'bruises': {'t': 'Bruises', 'f': 'No'},
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
        'veil-type': {'p': 'Partial', 'u': 'Universal'},
        'veil-color': {'n': 'Brown', 'o': 'Orange', 'w': 'White', 'y': 'Yellow'},
        'ring-number': {'n': 'None', 'o': 'One', 't': 'Two'},
        'ring-type': {
            'c': 'Cobwebby', 'e': 'Evanescent', 'f': 'Flaring',
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

# ==================== PREPROCESSING ====================

def preprocess_data(df):
    """Preprocess dataset - SAME AS GOOGLE COLAB"""
    
    print("\n🔧 Preprocessing data...")
    
    df_ml = df.copy()
    
    # Handle missing values
    df_ml['stalk-root'] = df_ml['stalk-root'].replace('?', 'missing')
    
    # Drop veil-type (karena hanya punya 1 nilai unik)
    if 'veil-type' in df_ml.columns:
        df_ml.drop('veil-type', axis=1, inplace=True)
    
    encoders = {}
    
    for col in df_ml.columns:
        le = LabelEncoder()
        df_ml[col] = le.fit_transform(df_ml[col].astype(str))
        encoders[col] = le
    
    print(f"✅ Preprocessing complete!")
    print(f"   Columns: {list(df_ml.columns)}")
    print(f"   ℹ️  Using LabelEncoder (same as Google Colab) for consistency")
    
    return df_ml, encoders

# ==================== MODEL TRAINING ====================

def train_model(X_train, y_train):
    """Train Random Forest model"""
    
    print("\n🤖 Training Random Forest model...")
    
    model = RandomForestClassifier(
        n_estimators=50,
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    model.fit(X_train, y_train)
    
    print("✅ Model training complete!")
    
    return model

# ==================== MODEL EVALUATION ====================

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """Evaluate model performance"""
    
    print("\n📊 Evaluating model...")
  
    # Training accuracy
    train_accuracy = model.score(X_train, y_train)
    
    # Testing accuracy
    test_accuracy = model.score(X_test, y_test)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Comprehensive metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\n✅ Model Evaluation Results:")
    print(f"   Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"   Testing Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"   Accuracy Score:    {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Precision:         {precision:.4f} ({precision*100:.2f}%)")
    print(f"   Recall:            {recall:.4f} ({recall*100:.2f}%)")
    print(f"   F1-Score:          {f1:.4f}")
    
    print(f"\n📋 Classification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Edible', 'Poisonous']
    ))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n🎯 Confusion Matrix:")
    print(f"   True Negatives:  {cm[0,0]}")
    print(f"   False Positives: {cm[0,1]}")
    print(f"   False Negatives: {cm[1,0]}")
    print(f"   True Positives:  {cm[1,1]}")
    
    return {
        'accuracy': float(accuracy),
        'train_accuracy': float(train_accuracy),
        'test_accuracy': float(test_accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'confusion_matrix': {
            'true_negatives': int(cm[0,0]),
            'false_positives': int(cm[0,1]),
            'false_negatives': int(cm[1,0]),
            'true_positives': int(cm[1,1])
        },
        'y_pred': y_pred
    }

# ==================== FEATURE IMPORTANCE ====================

def get_feature_importance(model, X_columns):
    """Get feature importance"""
    
    print("\n🔝 Top 10 Feature Importance:")
    
    importance = model.feature_importances_
    
    feature_df = pd.DataFrame({
        'Feature': X_columns,
        'Importance': importance
    }).sort_values('Importance', ascending=False)
    
    print(feature_df.head(10).to_string(index=False))
    
    return feature_df

# ==================== EXPORT MODEL ====================

def export_model(model, encoders, output_dir='model'):
    """Export model dan encoders ke file"""
    
    print(f"\n💾 Exporting model to {output_dir}/ folder...")
    
    # Create directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, 'model.pkl')
    joblib.dump(model, model_path)
    print(f"   ✅ Model saved: {model_path}")
    
    # Save encoders
    encoder_path = os.path.join(output_dir, 'encoder.pkl')
    joblib.dump(encoders, encoder_path)
    print(f"   ✅ Encoders saved: {encoder_path}")
    
    return model_path, encoder_path

# ==================== EXPORT METRICS ====================

def export_metrics(metrics, output_dir='model'):
    """Export evaluation metrics to JSON file"""
    
    print(f"\n📊 Exporting evaluation metrics...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    metrics_path = os.path.join(output_dir, 'metrics.json')
    
    metrics_json = {
        'accuracy': metrics['accuracy'],
        'train_accuracy': metrics['train_accuracy'],
        'test_accuracy': metrics['test_accuracy'],
        'precision': metrics['precision'],
        'recall': metrics['recall'],
        'f1_score': metrics['f1_score'],
        'confusion_matrix': metrics['confusion_matrix'],
        'timestamp': pd.Timestamp.now().isoformat()
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics_json, f, indent=2)
    
    print(f"   ✅ Metrics saved: {metrics_path}")
    return metrics_path

# ==================== EXPORT PREDICTIONS ====================

def export_dashboard_csv(df_original, model, X, encoders, output_dir='model'):
    """Export predictions untuk Looker Studio dashboard"""
    
    print(f"\n📊 Exporting dashboard CSV...")
    
    # Mapping untuk display
    mapping = get_feature_mapping()
    df_display = df_original.copy()
    
    for col, trans in mapping.items():
        if col in df_display.columns:
            df_display[col] = df_display[col].map(trans)
    
    # Predictions
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    # Create result dataframe
    hasil_final = df_display.copy()
    hasil_final['Prediction'] = pd.Series(predictions).map({
        0: 'Edible',
        1: 'Poisonous'
    })
    hasil_final['Confidence'] = probabilities.max(axis=1)
    hasil_final['Accuracy'] = np.where(
        hasil_final['poisonous'] == hasil_final['Prediction'],
        'Correct',
        'Wrong'
    )
    
    # Save CSV
    csv_path = os.path.join(output_dir, 'dashboard_mushroom_final.csv')
    hasil_final.to_csv(csv_path, index=False)
    print(f"   ✅ CSV saved: {csv_path}")
    print(f"   Records: {len(hasil_final)}")
    
    return csv_path

# ==================== MLFLOW INTEGRATION WITH DAGSHUB ====================

def setup_mlflow_tracking(df, model, metrics):
    """Setup MLflow with DagsHub remote tracking"""
    
    if not MLFLOW_AVAILABLE:
        print("⚠️  MLflow not available. Skipping tracking.")
        return
    
    print("\n📈 Setting up MLflow + DagsHub tracking...")
    
    try:
        dagshub_username = os.getenv('DAGSHUB_USERNAME')
        dagshub_repo = os.getenv('DAGSHUB_REPO')
        dagshub_token = os.getenv('DAGSHUB_TOKEN')
        
        print(f"   🔗 Connecting to DagsHub ({dagshub_username}/{dagshub_repo})...")
        dagshub.init(
            repo_owner=dagshub_username,
            repo_name=dagshub_repo,
            mlflow=True
        )
        
        print(f"   ⚙️  Enabling MLflow autologging...")
        mlflow.autolog()
        
        tracking_uri = mlflow.get_tracking_uri()
        print(f"   📡 MLflow Tracking URI: {tracking_uri}")
        
        experiment_name = os.getenv('MLFLOW_EXPERIMENT_NAME', 'mushroom-classification')
        try:
            mlflow.set_experiment(experiment_name)
        except:
            mlflow.create_experiment(experiment_name)
            mlflow.set_experiment(experiment_name)
        print(f"   📊 Experiment: {experiment_name}")
        
        with mlflow.start_run(run_name="mushroom-random-forest"):
            
            print("   📝 Logging parameters...")
            mlflow.log_param("model_type", "RandomForestClassifier")
            mlflow.log_param("n_estimators", 50)
            mlflow.log_param("max_depth", 5)
            mlflow.log_param("min_samples_split", 5)
            mlflow.log_param("min_samples_leaf", 2)
            mlflow.log_param("dataset_size", len(df))
            mlflow.log_param("test_size", 0.3)
            mlflow.log_param("random_state", 42)
            
            print("   📊 Logging metrics...")
            mlflow.log_metric("accuracy", metrics['accuracy'])
            mlflow.log_metric("train_accuracy", metrics['train_accuracy'])
            mlflow.log_metric("test_accuracy", metrics['test_accuracy'])
            mlflow.log_metric("precision", metrics['precision'])
            mlflow.log_metric("recall", metrics['recall'])
            mlflow.log_metric("f1_score", metrics['f1_score'])
            
            cm = metrics['confusion_matrix']
            mlflow.log_metric("true_negatives", cm['true_negatives'])
            mlflow.log_metric("false_positives", cm['false_positives'])
            mlflow.log_metric("false_negatives", cm['false_negatives'])
            mlflow.log_metric("true_positives", cm['true_positives'])
            
            print("   🤖 Logging model...")

            mlflow.sklearn.log_model(
                model,
                artifact_path="mushroom_classifier"
            )
            
            print("   ✅ All data logged to MLflow + DagsHub!")
            print(f"   📊 View experiments: mlflow ui")
            print(f"   🌐 View on DagsHub: https://dagshub.com/{dagshub_username}/{dagshub_repo}")
            
    except Exception as e:
        print(f"   ⚠️  MLflow tracking error (continuing): {e}")

# ==================== MAIN TRAINING PIPELINE ====================

def main():
    """Main training pipeline"""
    
    print("=" * 60)
    print("🍄 MUSHROOM CLASSIFICATION - RANDOM FOREST TRAINING")
    print("=" * 60)
    
    df = load_dataset()
    if df is None:
        print("❌ Failed to load dataset. Exiting.")
        return
    
    # 2. Preprocess data
    df_ml, encoders = preprocess_data(df)
    
    # 3. Split data
    print("\n📊 Splitting data...")
    X = df_ml.drop('poisonous', axis=1)
    y = df_ml['poisonous']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.3,
        random_state=42,
        stratify=y
    )
    
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Testing set:  {X_test.shape[0]} samples")
    
    # 4. Train model
    model = train_model(X_train, y_train)
    
    # 5. Evaluate model
    metrics = evaluate_model(model, X_train, y_train, X_test, y_test)
    
    # 6. Feature importance
    feature_df = get_feature_importance(model, X.columns)
    
    # 7. Export model
    export_model(model, encoders, output_dir='model')
    
    # 8. Export metrics
    export_metrics(metrics, output_dir='model')
    
    # 9. Export predictions CSV
    export_dashboard_csv(df, model, df_ml.drop('poisonous', axis=1), encoders, output_dir='model')
    
    # 10. MLflow tracking (optional)
    setup_mlflow_tracking(df, model, metrics)
    
    # 10. Summary
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print("\n📁 Output files:")
    print("   • model/model.pkl")
    print("   • model/encoder.pkl")
    print("   • model/metrics.json (evaluation metrics)")
    print("   • model/dashboard_mushroom_final.csv")
    print("\n📊 Model Metrics:")
    print(f"   • Accuracy: {metrics['accuracy']:.2%}")
    print(f"   • Precision: {metrics['precision']:.2%}")
    print(f"   • Recall: {metrics['recall']:.2%}")
    print(f"   • F1-Score: {metrics['f1_score']:.4f}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
