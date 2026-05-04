# 🚀 Panduan Setup Localhost untuk L-KDI

Panduan lengkap untuk menyiapkan environment pengembangan L-KDI di localhost.

---

## 📋 Daftar Isi

1. [Prasyarat](#prasyarat)
2. [Instalasi Cepat](#instalasi-cepat)
3. [Instalasi Detail](#instalasi-detail)
4. [Verifikasi Instalasi](#verifikasi-instalasi)
5. [Cara Penggunaan](#cara-penggunaan)
6. [Struktur Project](#struktur-project)
7. [Development Workflow](#development-workflow)
8. [Troubleshooting](#troubleshooting)

---

## Prasyarat

Sebelum memulai, pastikan Anda memiliki:

- ✅ **Python 3.9 atau lebih tinggi** (disarankan Python 3.10+)
- ✅ **pip** (Python package manager)
- ✅ **Git** (untuk clone repository)
- ✅ **Virtual environment** (direkomendasikan)

### Cek Versi Python

```bash
python --version
# atau
python3 --version
```

---

## Instalasi Cepat

Jalankan perintah berikut untuk setup otomatis:

```bash
# 1. Clone repository
git clone <repository-url>
cd lkdi

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install semua dependensi
pip install -r requirements.txt

# 5. Verifikasi instalasi
python -m pytest tests/ -v
```

---

## Instalasi Detail

### Langkah 1: Clone Repository

```bash
git clone https://github.com/username/lkdi.git
cd lkdi
```

### Langkah 2: Setup Virtual Environment

**Mengapa virtual environment?**
Virtual environment mengisolasi dependensi project ini dari system Python, menghindari konflik versi library.

#### Linux/MacOS:
```bash
python -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt):
```bash
python -m venv venv
venv\Scripts\activate.bat
```

✅ Anda akan melihat `(venv)` di awal prompt terminal jika berhasil.

### Langkah 3: Install Dependensi

```bash
pip install -r requirements.txt
```

**Daftar Library yang Diinstall:**

| Kategori | Library | Fungsi |
|----------|---------|--------|
| **Core** | `networkx>=3.0` | Analisis graf sitasi |
| | `numpy>=1.21.0` | Komputasi numerik |
| | `scipy>=1.7.0` | Algoritma ilmiah |
| | `pandas>=1.3.0` | Manipulasi data |
| **ML/NLP** | `scikit-learn>=1.0.0` | Machine learning |
| | `gensim>=4.0.0` | Word embeddings & topic modeling |
| **API** | `requests>=2.26.0` | HTTP requests ke OpenAlex/Semantic Scholar |
| **Viz** | `matplotlib>=3.4.0` | Visualisasi data |
| | `streamlit>=1.10.0` | Dashboard interaktif |
| **Testing** | `pytest>=7.0.0` | Framework testing |
| | `pytest-cov>=3.0.0` | Coverage reporting |
| **Dev Tools** | `black>=22.0.0` | Code formatter |
| | `flake8>=4.0.0` | Code linter |

### Langkah 4: Verifikasi Instalasi

Jalankan test suite untuk memastikan semua berfungsi:

```bash
python -m pytest tests/ -v
```

**Output yang diharapkan:**
```
============================= test session starts ==============================
collected 32 items

tests/test_detector.py ..........                                        [ 31%]
tests/test_graph_builder.py .........                                    [ 59%]
tests/test_metrics.py .............                                      [100%]

============================== 32 passed in 1.82s ==============================
```

---

## Verifikasi Instalasi

### 1. Cek Import Package

```bash
python -c "import lkdi; print('L-KDI version:', lkdi.__version__)"
```

### 2. Jalankan Test dengan Coverage

```bash
python -m pytest tests/ --cov=lkdi --cov-report=html
```

Buka laporan coverage di browser:
```bash
# Linux/Mac
open htmlcov/index.html
# Windows
start htmlcov\index.html
```

### 3. Test Import Semua Modul

```python
from lkdi import RevivalDetector, CitationGraphBuilder
from lkdi.metrics import detect_dormancy, calculate_rif, diffusion_distance, breakthrough_score

print("✅ Semua modul berhasil diimport!")
```

---

## Cara Penggunaan

### Contoh 1: Analisis Paper dengan DOI

```python
from lkdi import RevivalDetector

# Inisialisasi detector
detector = RevivalDetector(data_source="openalex")

# Analisis paper
result = detector.analyze(doi="10.1038/323533a0")

# Tampilkan hasil
print(f"Paper: {result.title}")
print(f"RIF Score: {result.rif_score:.2f}")
print(f"Periode Dormansi: {result.dormant_period}")
print(f"Konsep Kunci: {result.key_concepts}")
```

### Contoh 2: Bangun Graf Sitasi Custom

```python
from lkdi import CitationGraphBuilder

# Inisialisasi builder
builder = CitationGraphBuilder()

# Tambahkan paper
builder.add_paper("paper1", year=1990, citations=[])
builder.add_paper("paper2", year=1995, citations=["paper1"])
builder.add_paper("paper3", year=2005, citations=["paper1", "paper2"])

# Bangun graf
graph = builder.build()

# Hitung metrik
centrality = builder.calculate_centrality_metrics()
print(centrality)
```

### Contoh 3: Gunakan Fungsi Metrik Langsung

```python
from lkdi.metrics import detect_dormancy, calculate_rif

# Timeline sitasi: [(year, citation_count), ...]
timeline = [(1990, 2), (1991, 1), (1992, 0), (1993, 0), (1994, 0), 
            (1995, 0), (1996, 0), (1997, 0), (1998, 0), (1999, 0),
            (2000, 15), (2001, 25), (2002, 40)]

# Deteksi dormansi
dormant_period = detect_dormancy(timeline, dormancy_threshold=5)
print(f"Periode dormansi: {dormant_period}")

# Hitung RIF
rif = calculate_rif(timeline, dormant_period)
print(f"RIF Score: {rif}")
```

### Contoh 4: Jalankan Streamlit Dashboard

```bash
streamlit run app.py
```

Dashboard akan terbuka di `http://localhost:8501`

---

## Struktur Project

```
lkdi/
├── lkdi/                      # Package utama
│   ├── __init__.py           # Export modul publik
│   ├── metrics.py            # Fungsi metrik inti
│   ├── graph_builder.py      # Pembangunan graf sitasi
│   └── detector.py           # Detektor revival
├── tests/                     # Test suite
│   ├── conftest.py           # Konfigurasi pytest
│   ├── test_metrics.py       # Test fungsi metrik
│   ├── test_graph_builder.py # Test graph builder
│   └── test_detector.py      # Test detector
├── requirements.txt          # Daftar dependensi
├── SETUP_LOCALHOST.md        # Panduan ini
├── INSTALLATION.md           # Panduan instalasi umum
└── README.md                 # Dokumentasi utama
```

---

## Development Workflow

### 1. Format Kode dengan Black

```bash
black lkdi/ tests/
```

### 2. Lint Kode dengan Flake8

```bash
flake8 lkdi/ tests/
```

### 3. Jalankan Semua Test

```bash
python -m pytest tests/ -v
```

### 4. Jalankan Test dengan Coverage

```bash
python -m pytest tests/ --cov=lkdi --cov-report=term-missing
```

### 5. Tambah Test Baru

Buat file test baru di folder `tests/` dengan prefix `test_`:

```python
# tests/test_new_feature.py
def test_new_feature():
    assert True
```

### 6. Commit & Push

```bash
git add .
git commit -m "feat: tambah fitur baru"
git push origin main
```

---

## Troubleshooting

### ❌ ModuleNotFoundError: No module named 'lkdi'

**Solusi:**
```bash
# Pastikan berada di direktori project
cd /workspace/lkdi

# Install package dalam mode development
pip install -e .

# Atau tambahkan path ke PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/workspace/lkdi"
```

### ❌ Gagal Install Library

**Solusi 1: Upgrade pip**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Solusi 2: Install per library**
```bash
pip install networkx numpy scipy pandas
pip install scikit-learn gensim
pip install requests matplotlib streamlit
pip install pytest pytest-cov black flake8
```

**Solusi 3: Gunakan conda (jika tersedia)**
```bash
conda create -n lkdi python=3.10
conda activate lkdi
conda install networkx numpy scipy pandas scikit-learn
pip install gensim requests matplotlib streamlit pytest pytest-cov black flake8
```

### ❌ Timeout saat Fetch Data dari API

**Solusi:**
- Periksa koneksi internet
- Tambahkan timeout parameter
- Gunakan cache lokal

```python
detector = RevivalDetector(data_source="openalex", timeout=30)
```

### ❌ Virtual Environment Tidak Aktif

**Solusi:**
```bash
# Cek apakah venv aktif
which python
# Harus menunjuk ke venv/bin/python

# Re-activate
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
```

### ❌ Test Gagal

**Solusi:**
```bash
# Jalankan test dengan detail error
python -m pytest tests/ -v --tb=long

# Jalankan satu test spesifik
python -m pytest tests/test_metrics.py::TestDetectDormancy::test_dormancy_detected -v

# Jalankan test dengan capture output
python -m pytest tests/ -s
```

---

## API Keys (Opsional)

Untuk akses penuh ke API eksternal:

### OpenAlex API
- Gratis, tidak memerlukan API key
- Rate limit: ~100 requests/menit

### Semantic Scholar API
- Gratis untuk penggunaan dasar
- Dapatkan API key di: https://www.semanticscholar.org/product/api

Simpan API key di environment variable:

```bash
export SEMANTIC_SCHOLAR_API_KEY="your-api-key-here"
```

Atau buat file `.env`:

```bash
SEMANTIC_SCHOLAR_API_KEY=your-api-key-here
```

---

## Quick Reference Commands

```bash
# Aktivasi virtual environment
source venv/bin/activate

# Install dependensi
pip install -r requirements.txt

# Jalankan semua test
python -m pytest tests/ -v

# Jalankan test dengan coverage
python -m pytest tests/ --cov=lkdi

# Format kode
black lkdi/ tests/

# Lint kode
flake8 lkdi/ tests/

# Jalankan dashboard
streamlit run app.py

# Deaktivasi virtual environment
deactivate
```

---

## 📚 Referensi Tambahan

- [Dokumentasi NetworkX](https://networkx.org/documentation/)
- [Dokumentasi Scikit-learn](https://scikit-learn.org/stable/)
- [OpenAlex API Docs](https://docs.openalex.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## 🤝 Kontribusi

Untuk berkontribusi pada project ini:

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/amazing-feature`)
3. Commit perubahan (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buka Pull Request

---

## 📄 Lisensi

Project ini dilisensikan di bawah lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail.

---

**Happy Coding! 🎉**

Jika ada pertanyaan atau masalah, silakan buka issue di repository GitHub.
