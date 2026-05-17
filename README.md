# 🍄 Mushroom AI Classification

Production-ready Machine Learning website untuk klasifikasi jamur menggunakan Random Forest dengan dashboard analytics dan prediksi real-time.

> **🎯 Website ML yang dirancang dengan design yang bagus, mobile friendly, dashboard prediction forms dan Looker Studio integration**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Fitur Utama

- ✅ **Advanced ML Model** - Random Forest dengan 50 trees
- ✅ **Responsive Design** - Sempurna di desktop dan mobile
- ✅ **Real-time Prediction** - Hasil instant dengan confidence score
- ✅ **Interactive Dashboard** - Monitoring real-time dengan Chart.js
- ✅ **Google Looker Studio Integration** - Dashboard analytics profesional
- ✅ **Prediction History** - Simpan riwayat semua prediksi
- ✅ **REST API** - Endpoint siap untuk integrasi
- ✅ **Dark Mode** - Support dark mode (browser preference)
- ✅ **Mobile Optimized** - Touch-friendly interface

## 📋 Requirement

- Python 3.11+
- Node.js 18+ (untuk development)
- pip (Python package manager)

## 🚀 Instalasi Cepat

### 1. Clone Repository
```bash
cd d:\deya\UASDSP
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Persiapkan Model dari Google Colab

Setelah training model di Google Colab, download 2 file penting:
- `model.pkl` - Model Random Forest
- `encoder.pkl` - LabelEncoder untuk semua features

Masukkan kedua file ini ke folder root project (sejajar dengan `app.py`)

### 4. Run Flask Server
```bash
python app.py
```

Server akan berjalan di: **http://localhost:5000**

### 5. Buka di Browser
Kunjungi: [http://localhost:5000](http://localhost:5000)

## 📂 Struktur Folder Project

```
UASDSP/
├── app.py                          # Flask backend utama
├── requirements.txt                # Dependencies
├── Dockerfile                      # Docker configuration
├── README.md                       # Dokumentasi
├── model.pkl                       # Model Random Forest (download dari Colab)
├── encoder.pkl                     # Label encoder (download dari Colab)
├── dashboard_mushroom_final.csv    # Dataset untuk Looker Studio
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Landing page
│   ├── predict.html               # Prediction form
│   └── dashboard.html             # Analytics dashboard
│
└── static/                         # Static files
    ├── css/
    │   └── style.css              # Main stylesheet
    └── js/
        └── script.js              # JavaScript utilities
```

## 🔧 Cara Menggunakan Model dari Google Colab

### Di Google Colab, export model dengan kode ini:

```python
import joblib

# Setelah training selesai
joblib.dump(rf_model, 'model.pkl')
joblib.dump(encoders, 'encoder.pkl')
```

### Download kedua file, kemudian:

1. Letakkan `model.pkl` di folder root
2. Letakkan `encoder.pkl` di folder root
3. Restart Flask server
4. Model siap digunakan!

## 📝 Input Features (21 Attributes)

### Cap Characteristics
- Cap Shape: Bell, Conical, Convex, Flat, Knobbed, Sunken
- Cap Surface: Fibrous, Grooves, Scaly, Smooth
- Cap Color: 10 pilihan warna
- Bruises: Yes/No

### Odor & Gill
- Odor: 9 jenis aroma
- Gill Attachment: Attached, Descending, Free, Notched
- Gill Spacing: Close, Crowded, Distant
- Gill Size: Broad, Narrow
- Gill Color: 11 pilihan warna

### Stalk (Stem)
- Stalk Shape: Enlarging, Tapering
- Stalk Root: Bulbous, Club, Cup, Equal, Rhizomorphs, Rooted, Missing
- Stalk Surface Above Ring: Fibrous, Scaly, Silky, Smooth
- Stalk Surface Below Ring: Fibrous, Scaly, Silky, Smooth
- Stalk Color Above Ring: 9 pilihan warna
- Stalk Color Below Ring: 9 pilihan warna

### Veil & Ring
- Veil Color: Brown, Orange, White, Yellow
- Ring Number: None, One, Two
- Ring Type: 8 pilihan tipe

### Spore & Habitat
- Spore Print Color: 9 pilihan warna
- Population: Abundant, Clustered, Numerous, Scattered, Several, Solitary
- Habitat: Grasses, Leaves, Meadows, Paths, Urban, Waste, Woods

## 🎯 Halaman Utama

### 1. **Landing Page** (`/`)
- Hero section dengan CTA button
- Statistik model (accuracy, dataset size, features, etc)
- Feature cards yang menjelaskan capabilities
- How it works section
- Call-to-action section

### 2. **Prediction Page** (`/predict`)
- Form lengkap untuk semua 21 features
- Organized dalam sections (Cap, Odor, Stalk, Veil, Spore)
- Real-time result display
- Confidence score dengan progress bar
- Risk level indicator
- Probability breakdown

### 3. **Dashboard Page** (`/dashboard`)
- Real-time statistics cards
- Distribution chart (Pie chart - Edible vs Poisonous)
- Confidence score distribution
- Google Looker Studio embed
- Recent predictions table
- Auto-refresh setiap 5 detik

## 🔌 API Endpoints

### Get Stats
```
GET /api/stats
Response:
{
  "total": 10,
  "poisonous": 3,
  "edible": 7,
  "avg_confidence": 94.5
}
```

### Predict
```
POST /api/predict
Body:
{
  "odor": "a",
  "cap-shape": "b",
  "gill-size": "b",
  ...
}
Response:
{
  "success": true,
  "prediction": "EDIBLE",
  "confidence": 95.2,
  "probability_poisonous": 4.8,
  "probability_edible": 95.2,
  "risk_level": "HIGH"
}
```

### Get History
```
GET /api/history
Response: [
  {
    "timestamp": "2024-01-15 10:30:45",
    "prediction": "EDIBLE",
    "confidence": 95.2,
    "input": {...}
  }
]
```

## 🎨 Desain & UI

### Color Scheme
- **Primary**: Green (#28a745) - untuk sukses/safe
- **Secondary**: Gray (#6c757d) - untuk neutral
- **Danger**: Red (#dc3545) - untuk poisonous
- **Info**: Blue (#17a2b8) - untuk informasi

### Responsive Breakpoints
- Mobile: < 576px
- Tablet: 576px - 768px
- Desktop: > 1024px

### Modern Features
- Glassmorphism effects
- Smooth animations
- Loading indicators
- Progress bars
- Badges & alerts
- Interactive charts

## 📊 Integrasi Google Looker Studio

### Langkah-langkah:

1. **Kunjungi**: https://lookerstudio.google.com
2. **Buat Report Baru**
3. **Tambah Data Source**: Upload `dashboard_mushroom_final.csv`
4. **Buat Visualisasi**:
   - Pie chart: Edible vs Poisonous
   - Bar chart: Odor vs Poisonous
   - Table: Recent predictions
   - Scorecard: Accuracy
5. **Share & Embed**:
   - Klik Share → Embed report
   - Copy iframe link
   - Paste ke halaman dashboard HTML

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t mushroom-ai .
```

### Run Container
```bash
docker run -p 5000:5000 mushroom-ai
```

### Docker Compose (Optional)
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
```

## 🚀 Deploy Online

### Option 1: Render
1. Push project ke GitHub
2. Connect Render ke repo
3. Set start command: `gunicorn app:app`
4. Set port: 5000
5. Deploy!

### Option 2: Railway
1. Push project ke GitHub
2. Connect Railway ke repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Deploy!

### Option 3: Heroku
```bash
heroku create mushroom-ai
git push heroku main
```

## 📊 Model Performance

```
Accuracy: 95.2%
Precision: 96.1%
Recall: 94.5%
F1-Score: 95.3%

Features: 21 attributes
Algorithm: Random Forest (50 trees)
Test Size: 30%
Random State: 42
```

## ⚠️ Disclaimer

Hasil prediksi ini **HANYA untuk referensi**. Jangan pernah memakan jamur hanya berdasarkan prediksi model ini. **Selalu konsultasikan dengan ahli mikologi atau expert lainnya** sebelum mengkonsumsi jamur apapun.

## 🔐 Security

- Input validation di frontend dan backend
- CORS configuration untuk API
- Environment variables untuk sensitive data
- Rate limiting ready (implementasi optional)

## 🐛 Troubleshooting

### Model tidak ditemukan
```
⚠ Model tidak ditemukan, model akan dimuat saat tersedia
```
**Solusi**: Download `model.pkl` dan `encoder.pkl` dari Colab, letakkan di folder root

### Port 5000 sudah terpakai
```bash
# Ganti port di app.py line terakhir
app.run(debug=True, host='0.0.0.0', port=5001)
```

### CORS Error
```bash
# Sudah dihandle dengan flask-cors
# Jika masih error, pastikan Flask-CORS terinstall
pip install flask-cors
```

### Static files tidak loading
```bash
# Pastikan folder structure benar:
# static/
#   ├── css/
#   │   └── style.css
#   └── js/
#       └── script.js
```

## 📚 Libraries Digunakan

- **Flask** - Web framework
- **Flask-CORS** - Cross-origin support
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **Joblib** - Model serialization
- **Bootstrap 5** - CSS framework
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

## 📝 Lisensi

MIT License - Bebas digunakan untuk project apapun

## 👤 Author

- **Project**: Mushroom AI Classification
- **Purpose**: Skripsi, Sidang, Portfolio
- **Status**: Production Ready

## 📞 Support

Jika ada masalah atau pertanyaan:
1. Cek troubleshooting section
2. Baca error message dengan teliti
3. Pastikan semua dependencies terinstall
4. Check Flask server logs

## 🎓 Educational Value

Project ini cocok untuk:
- ✅ Skripsi/Tesis
- ✅ Tugas Akhir
- ✅ Portfolio Data Science
- ✅ Portfolio ML Engineer
- ✅ Learning Flask & ML Integration
- ✅ Understanding ML Workflow

## 🚦 Development Status

- [x] Backend API
- [x] Frontend UI
- [x] Prediction Form
- [x] Dashboard
- [x] Mobile Responsive
- [x] Docker Support
- [x] Documentation
- [ ] User Authentication (Optional)
- [ ] Database Integration (Optional)
- [ ] File Upload ML (Optional)

---

**Enjoy your Mushroom AI Classification System! 🍄✨**
