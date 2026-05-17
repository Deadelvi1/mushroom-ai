# 🍄 Mushroom AI - Monitoring & Deployment Guide

## 📊 Monitoring Model Evaluation Metrics

### Generate Metrics (Required First Step)

Before metrics are available, you must train the model:

```bash
python model/train_model.py
```

This generates `model/metrics.json` containing evaluation metrics.

### Access Metrics via API

**Get Model Metrics:**
```bash
curl http://localhost:8000/api/model-metrics
```

**Response:**
```json
{
  "status": "success",
  "metrics": {
    "accuracy": 0.952,
    "train_accuracy": 0.953,
    "test_accuracy": 0.952,
    "precision": 0.945,
    "recall": 0.951,
    "f1_score": 0.9483,
    "confusion_matrix": {
      "true_negatives": 741,
      "false_positives": 18,
      "false_negatives": 16,
      "true_positives": 769
    }
  },
  "loaded_at": "2026-05-14T18:06:31.123456"
}
```

### Get Model Information

```bash
curl http://localhost:8000/api/model-info
```

**Response:**
```json
{
  "model_status": "loaded",
  "model_loaded": true,
  "encoders_loaded": true,
  "features_count": 21,
  "has_evaluation_metrics": true,
  "loaded_at": "2026-05-14T18:06:31.123456",
  "total_predictions": 15,
  "evaluation_metrics": { ... }
}
```

### Monitor Real-time Statistics

```bash
curl http://localhost:8000/api/stats
```

**Response:**
```json
{
  "total": 45,
  "poisonous": 12,
  "edible": 33,
  "avg_confidence": 91.23
}
```

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Build image
docker build -t mushroom-ai:latest .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/model:/app/model \
  mushroom-ai:latest

# Access application
# http://localhost:8000
```

### Docker Compose (Development)

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web
```

## 🔗 DagsHub Integration

### Setup Steps

1. **Create Account**: https://dagshub.com

2. **Setup Environment Variables**:
   ```bash
   export MLFLOW_TRACKING_URI=https://dagshub.com/YOUR_USERNAME/mushroom-ai.mlflow
   export MLFLOW_TRACKING_USERNAME=YOUR_USERNAME
   export MLFLOW_TRACKING_PASSWORD=YOUR_DAGSHUB_TOKEN
   ```

3. **Run Training with MLflow**:
   ```bash
   python model/train_model.py
   ```

4. **View Experiments**:
   - https://dagshub.com/YOUR_USERNAME/mushroom-ai/experiments

## 🚀 Railway Deployment

### Deploy in 3 Steps

1. **Login to Railway**: https://railway.app

2. **Connect GitHub Repository**:
   - New Project → Deploy from GitHub
   - Select mushroom-ai repository
   - Railway auto-detects Python

3. **Set Environment Variables**:
   - FLASK_ENV=production
   - PYTHONUNBUFFERED=1

### Access Deployed App

After deployment, Railway provides a public URL:
```
https://mushroom-ai-production.railway.app
```

### Monitor Deployment

```bash
# View logs
railway logs

# Check status
railway status
```

## ✅ Error Handling

All API errors include error codes for debugging:

| Error Code | HTTP | Meaning | Solution |
|-----------|------|---------|----------|
| `MODEL_NOT_LOADED` | 503 | Model file missing | Run `python model/train_model.py` |
| `MISSING_FEATURES` | 400 | Input features incomplete | Check all 21 features present |
| `INVALID_VALUE` | 400 | Invalid categorical value | Use valid option from dropdown |
| `ENCODING_ERROR` | 400 | Feature encoding failed | Check feature values |
| `PREDICTION_FAILED` | 500 | Model prediction error | Check model files |
| `INTERNAL_ERROR` | 500 | Unexpected error | Check logs |

## 📋 Feature Checklist

- [x] Model training with evaluation metrics
- [x] Metrics saved to JSON file
- [x] API endpoints for model metrics
- [x] Error handling with error codes
- [x] Logging for all operations
- [x] Docker containerization (port 8000)
- [x] Docker Compose setup
- [x] DagsHub/MLflow integration
- [x] Railway deployment guide
- [x] Real-time prediction monitoring

## 📁 File Structure

```
mushroom-ai/
├── app.py                    # Flask with enhanced monitoring
├── model/
│   ├── train_model.py       # Training with metrics export
│   ├── model.pkl            # Trained model
│   ├── encoder.pkl          # Feature encoders
│   └── metrics.json         # Evaluation metrics (generated)
├── Dockerfile               # Updated for port 8000
├── docker-compose.yml       # MLflow integration
├── COMPLETE_GUIDE.md        # Full documentation
├── MONITORING_GUIDE.md      # This file
└── .env.example             # Configuration template
```

## 🎯 Production Deployment Checklist

- [ ] Run `python model/train_model.py` locally
- [ ] Verify `model/metrics.json` created
- [ ] Test all API endpoints locally
- [ ] Build Docker image: `docker build -t mushroom-ai .`
- [ ] Test Docker image locally
- [ ] Create DagsHub account & repository
- [ ] Setup MLflow tracking environment variables
- [ ] Create Railway account
- [ ] Deploy to Railway
- [ ] Test production endpoints
- [ ] Setup custom domain (optional)
- [ ] Monitor logs & metrics

## 🆘 Troubleshooting

### Metrics endpoint returns 404

**Cause**: `model/metrics.json` doesn't exist

**Solution**:
```bash
python model/train_model.py
```

### Model not loading at startup

**Cause**: Model files missing or corrupted

**Solution**:
```bash
# Check files exist
ls model/model.pkl
ls model/encoder.pkl

# Retrain if needed
python model/train_model.py
```

### Docker port conflict

**Cause**: Port 8000 already in use

**Solution**:
```bash
# Use different port
docker run -p 9000:8000 mushroom-ai:latest

# Or find and kill existing process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Railway deployment fails

**Cause**: Model files too large or missing

**Solutions**:
1. Use Git LFS: `git lfs track "*.pkl"`
2. Pre-train on Railway: Update build command
3. Download from cloud: Add download script to app.py

---

For detailed setup instructions, see `COMPLETE_GUIDE.md`
