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

**Enjoy your Mushroom AI Classification System! 🍄✨**
