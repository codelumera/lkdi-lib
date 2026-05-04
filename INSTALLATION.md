# 🚀 Panduan Instalasi dan Penggunaan L-KDI

Panduan lengkap untuk menginstal, mengonfigurasi, dan menggunakan **L-KDI (Latent Knowledge Diffusion Index)** di localhost untuk pengembangan dan pengujian.

---

## 📋 Prasyarat

Sebelum memulai, pastikan Anda telah menginstal:

- **Python 3.9 atau lebih baru** ([Download Python](https://www.python.org/downloads/))
- **pip** (Package installer for Python) - biasanya sudah termasuk dengan Python
- **Git** ([Download Git](https://git-scm.com/downloads))

### Verifikasi Instalasi Prasyarat

```bash
# Cek versi Python (harus 3.9+)
python --version
# atau
python3 --version

# Cek versi pip
pip --version
# atau
pip3 --version

# Cek versi Git
git --version
```

---

## 📥 Instalasi di Localhost

### Langkah 1: Clone Repository

```bash
# Clone repository dari GitHub
git clone https://github.com/stipwunaraha/latent-knowledge-diffusion-index.git

# Masuk ke direktori proyek
cd latent-knowledge-diffusion-index
```

### Langkah 2: Buat Virtual Environment (Direkomendasikan)

Menggunakan virtual environment sangat direkomendasikan untuk mengisolasi dependensi proyek:

#### **Opsi A: Menggunakan `venv` (Bawaan Python)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### **Opsi B: Menggunakan `conda` (Jika menggunakan Anaconda/Miniconda)**

```bash
# Buat environment baru
conda create -n lkdi python=3.9

# Aktifkan environment
conda activate lkdi
```

### Langkah 3: Instal Dependensi

Setelah virtual environment aktif, instal semua dependensi:

```bash
# Upgrade pip terlebih dahulu (opsional tapi direkomendasikan)
pip install --upgrade pip

# Instal semua dependensi dari requirements.txt
pip install -r requirements.txt
```

Proses ini akan menginstal:
- **Core libraries**: networkx, numpy, scipy, pandas
- **ML/Embedding**: scikit-learn, gensim
- **API Client**: requests
- **Visualisasi**: matplotlib, streamlit
- **Testing**: pytest, pytest-cov
- **Development tools**: black, flake8

### Langkah 4: Verifikasi Instalasi

Jalankan test suite untuk memastikan semua berfungsi dengan baik:

```bash
# Jalankan semua test
python -m pytest tests/ -v

# Jalankan test dengan coverage report
python -m pytest tests/ -v --cov=lkdi --cov-report=html

# Buka laporan coverage (jika menggunakan browser GUI)
# Coverage report akan tersimpan di folder htmlcov/
```

Jika semua test lulus (32 tests), instalasi berhasil! ✅

---

## 🎯 Cara Penggunaan

### 1. Penggunaan Dasar dalam Python Script

Buat file Python baru (misalnya `analyze_paper.py`):

```python
from lkdi import RevivalDetector, CitationGraphBuilder
from lkdi.metrics import calculate_rif, detect_dormancy

# Inisialisasi detector
detector = RevivalDetector(data_source="openalex")

# Analisis paper berdasarkan DOI
result = detector.analyze(doi="10.1038/323533a0")

# Tampilkan hasil
print(f"📊 Revival Impact Factor (RIF): {result.rif_score:.2f}")
print(f"⏰ Periode Dormansi: {result.dormant_period}")
print(f"🔑 Konsep Kunci: {', '.join(result.key_concepts)}")
print(f"📈 Total Sitasi: {result.total_citations}")
```

Jalankan script:

```bash
python analyze_paper.py
```

### 2. Membangun Graf Sitasi

```python
from lkdi import CitationGraphBuilder

# Inisialisasi builder
builder = CitationGraphBuilder()

# Tambahkan paper ke graf
builder.add_paper(
    paper_id="paper_1",
    year=1986,
    title="Learning representations by back-propagating errors",
    field="neural_networks"
)

builder.add_paper(
    paper_id="paper_2",
    year=2012,
    title="ImageNet Classification with Deep Convolutional Neural Networks",
    field="computer_vision"
)

# Tambahkan edge sitasi
builder.add_edge("paper_2", "paper_1", weight=0.8)

# Bangun graf
graph = builder.build()

# Hitung metrik centrality
centralities = builder.calculate_centrality_metrics()
print(f"PageRank scores: {centralities['pagerank']}")
```

### 3. Analisis Kustom dengan Data Sendiri

```python
from lkdi.detector import RevivalDetector

# Gunakan data custom (tidak fetch dari API)
detector = RevivalDetector(data_source="custom")

# Siapkan data timeline sitasi
citation_data = {
    1986: 150,
    1987: 45,
    # ... tahun dengan sedikit sitasi (dormansi)
    2000: 2,
    2005: 1,
    # ... lonjakan tiba-tiba
    2012: 500,
    2013: 1200,
    2014: 2500
}

result = detector.analyze_custom(citation_data)
print(f"RIF Score: {result.rif_score}")
```

---

## 🧪 Pengujian (Testing)

### Menjalankan Test Suite

```bash
# Jalankan semua test
python -m pytest tests/ -v

# Jalankan test spesifik
python -m pytest tests/test_metrics.py -v
python -m pytest tests/test_graph_builder.py -v
python -m pytest tests/test_detector.py -v

# Jalankan test dengan filter nama
python -m pytest tests/ -v -k "test_calculate_rif"

# Jalankan test dengan coverage
python -m pytest tests/ -v --cov=lkdi --cov-report=term-missing
```

### Menulis Test Baru

Tambahkan test baru di folder `tests/`:

```python
# tests/test_custom.py
from lkdi.metrics import your_new_function

def test_your_new_feature():
    result = your_new_function(input_data)
    assert result == expected_value
```

---

## 🛠️ Development Tools

### Code Formatting dengan Black

```bash
# Format semua file Python
black lkdi/ tests/

# Format dengan line length khusus
black lkdi/ --line-length 88
```

### Code Linting dengan Flake8

```bash
# Periksa style issues
flake8 lkdi/ tests/

# Periksa dengan ignore rules tertentu
flake8 lkdi/ --ignore=E203,W503
```

### Menjalankan Streamlit Dashboard (Jika tersedia)

```bash
# Jalankan dashboard visualisasi
streamlit run app.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

---

## 📁 Struktur Direktori

```
latent-knowledge-diffusion-index/
├── lkdi/                      # Package utama
│   ├── __init__.py           # Export modul publik
│   ├── metrics.py            # Fungsi metrik inti
│   ├── graph_builder.py      # Pembangunan graf sitasi
│   └── detector.py           # Detektor revival
├── tests/                     # Test suite
│   ├── conftest.py           # Konfigurasi pytest
│   ├── test_metrics.py       # Test metrik
│   ├── test_graph_builder.py # Test graph builder
│   └── test_detector.py      # Test detector
├── requirements.txt          # Daftar dependensi
├── README.md                 # Dokumentasi utama
├── INSTALLATION.md          # Panduan ini
└── .gitignore               # File yang diabaikan Git
```

---

## 🔧 Troubleshooting

### Masalah Umum dan Solusi

#### 1. **Error: `ModuleNotFoundError: No module named 'lkdi'`**

**Solusi**: Pastikan Anda berada di direktori root proyek atau tambahkan ke PYTHONPATH:

```bash
# Opsi A: Jalankan dari direktori root
cd /path/to/latent-knowledge-diffusion-index
python your_script.py

# Opsi B: Tambahkan ke PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/latent-knowledge-diffusion-index"

# Windows (PowerShell)
$env:PYTHONPATH = "${env:PYTHONPATH};C:\path\to\latent-knowledge-diffusion-index"
```

#### 2. **Error: `pip install` gagal**

**Solusi**:
```bash
# Upgrade pip
pip install --upgrade pip

# Clear cache dan install ulang
pip cache purge
pip install -r requirements.txt --no-cache-dir

# Install satu per satu jika masih gagal
pip install networkx
pip install numpy
# ... dst
```

#### 3. **Test gagal karena timeout API**

**Solusi**: Beberapa test mungkin memerlukan koneksi ke OpenAlex API. Jika offline:

```bash
# Skip test yang memerlukan API
python -m pytest tests/ -v -m "not api"

# Atau gunakan mock data
pytest tests/ --mock-api
```

#### 4. **Virtual environment tidak aktif**

**Solusi**:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Verifikasi aktif
which python  # Harus menunjuk ke venv/bin/python
```

---

## 🌐 API Keys (Opsional)

Beberapa fitur mungkin memerlukan API key untuk akses penuh:

### OpenAlex API
- **Status**: Gratis, tidak memerlukan API key untuk penggunaan dasar
- **Rate Limit**: 100 requests/menit
- **Dokumentasi**: https://docs.openalex.org/

### Semantic Scholar API (Alternatif)
- **Status**: Gratis dengan registrasi
- **Dapatkan API Key**: https://www.semanticscholar.org/product/api
- **Setup**:
  ```python
  import os
  os.environ['S2_API_KEY'] = 'your_api_key_here'
  ```

---

## 📊 Contoh Output

Ketika menjalankan analisis, Anda akan mendapatkan output seperti:

```
📊 Revival Impact Factor (RIF): 8.45
⏰ Periode Dormansi: (1990, 2010) - 20 tahun
🔑 Konsep Kunci: ['backpropagation', 'gradient descent', 'neural networks']
📈 Total Sitasi: 15420
📉 Sitasi selama dormansi: 45
📈 Sitasi setelah revival: 12300

Analisis: Paper ini mengalami periode dormansi selama 20 tahun 
sebelum mengalami kebangkitan signifikan pada tahun 2010-an, 
kemungkinan disebabkan oleh kemajuan dalam komputasi GPU 
dan ketersediaan dataset besar.
```

---

## 🤝 Kontribusi

Untuk berkontribusi pada pengembangan L-KDI:

1. **Fork repository**
2. **Buat branch fitur**: `git checkout -b fitur-baru`
3. **Commit perubahan**: `git commit -m 'Tambah fitur baru'`
4. **Push ke branch**: `git push origin fitur-baru`
5. **Buat Pull Request**

Pastikan semua test lulus sebelum submit PR:

```bash
python -m pytest tests/ -v
black lkdi/ tests/
flake8 lkdi/ tests/
```

---

## 📚 Referensi & Sumber Daya

- **Dokumentasi NetworkX**: https://networkx.org/documentation/
- **OpenAlex API Docs**: https://docs.openalex.org/
- **Scikit-learn User Guide**: https://scikit-learn.org/stable/user_guide.html
- **Pandas Documentation**: https://pandas.pydata.org/docs/

---

## 📄 Lisensi

MIT License - Lihat file [LICENSE](LICENSE) untuk detail lengkap.

---

## 📞 Dukungan

Jika mengalami masalah atau memiliki pertanyaan:

- 🐛 **Bug Reports**: Buat issue di [GitHub Issues](https://github.com/stipwunaraha/latent-knowledge-diffusion-index/issues)
- 💬 **Diskusi**: Gunakan [GitHub Discussions](https://github.com/stipwunaraha/latent-knowledge-diffusion-index/discussions)
- 📧 **Email**: Lihat profil kontributor utama

---

**Selamat mengembangkan L-KDI!** 🎉

*\"Melacak hantu ide: Ketika pemikiran dari masa lalu tiba-tiba menjadi solusi masa depan.\"*
