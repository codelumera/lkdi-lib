<!-- latent-knowledge-diffusion-index/README.md -->

# 👻 L-KDI: Latent Knowledge Diffusion Index

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-green.svg)](https://networkx.org/)
[![Tests](https://img.shields.io/badge/tests-32%20passed-brightgreen.svg)](https://github.com/stipwunaraha/latent-knowledge-diffusion-index)

> *"Melacak hantu ide: Ketika pemikiran dari masa lalu tiba-tiba menjadi solusi masa depan."*

**L-KDI** adalah pustaka Python open-source untuk mendeteksi fenomena **"Sleeping Beauties"** dalam literatur ilmiah—makalah yang awalnya terabaikan lalu menjadi sangat berpengaruh setelah masa dormansi panjang. Library ini menghitung **Revival Impact Factor (RIF)** dan menganalisis pola difusi pengetahuan melalui graf sitasi temporal.

## 🎯 Fitur Utama

- 🔍 **Deteksi Otomatis Kebangkitan Ide**: Identifikasi makalah dengan periode dormansi diikuti lonjakan sitasi
- 📊 **Metrik L-KDI & RIF**: Kuantifikasi dampak tertunda (delayed impact) dalam sains
- 🕸️ **Analisis Graf Sitasi Temporal**: Bangun dan analisis jaringan sitasi dengan bobot waktu
- 🌐 **Integrasi Data Multi-Sumber**: Fetch data dari OpenAlex API dan Semantic Scholar
- 🧠 **Ekstraksi Konsep Kunci**: NLP-powered extraction untuk identifikasi ide yang di-revive
- 📈 **Visualisasi Timeline**: Dashboard Streamlit untuk eksplorasi interaktif

## 💡 Mengapa L-KDI?

Banyak terobosan ilmiah sebenarnya merupakan *rediscovery* dari konsep lama:
- **Backpropagation** (1974 → 1986 → 2010s)
- **Convolutional Neural Networks** (1980s → 2012)
- **Attention Mechanism** (2014 → 2017)

Metrik tradisional tidak menangkap *delayed impact* ini. L-KDI mengisi celah tersebut dengan mengukur:
1. **Diffusion Distance**: Seberapa jauh konsep bergerak melintasi ruang ilmu
2. **Latency Time**: Durasi periode dormansi sebelum kebangkitan
3. **Breakthrough Score**: Sejauh mana karya mendobrak batasan bidang

## 📦 Instalasi Cepat

### Prasyarat
- Python 3.9 atau lebih tinggi
- pip (Python package manager)
- Git

### Langkah Instalasi (5 Menit)

```bash
# 1. Clone repository
git clone https://github.com/stipwunaraha/latent-knowledge-diffusion-index.git
cd latent-knowledge-diffusion-index

# 2. Buat virtual environment (direkomendasikan)
python -m venv venv

# 3. Aktifkan virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 4. Install semua dependensi
pip install -r requirements.txt

# 5. Verifikasi instalasi dengan menjalankan test suite
python -m pytest tests/ -v
```

✅ Jika semua 32 test lulus, library siap digunakan!

## 🚀 Cara Penggunaan

### Contoh 1: Analisis Paper dengan DOI

```python
from lkdi import RevivalDetector

# Inisialisasi detector dengan sumber data OpenAlex
detector = RevivalDetector(data_source="openalex")

# Analisis makalah seminal Backpropagation (Rumelhart et al., 1986)
result = detector.analyze(doi="10.1038/323533a0")

print(f"📊 Revival Impact Factor (RIF): {result.rif_score:.2f}")
print(f"⏳ Periode Dormansi: {result.dormant_period}")
print(f"💡 Konsep yang di-revive: {result.key_concepts}")
print(f"📈 Total Sitasi: {result.total_citations}")
```

### Contoh 2: Bangun Graf Sitasi Custom

```python
from lkdi import CitationGraphBuilder

# Inisialisasi builder
builder = CitationGraphBuilder()

# Tambahkan paper ke graf
builder.add_paper("paper_1", year=1980, title="Early Neural Nets")
builder.add_paper("paper_2", year=1986, title="Learning Representations")
builder.add_paper("paper_3", year=2012, title="Deep Learning Revolution")

# Tambahkan edge sitasi
builder.add_edge("paper_2", "paper_1", weight=0.8)  # paper_2 sitasi paper_1
builder.add_edge("paper_3", "paper_2", weight=0.9)

# Bangun graf
graph = builder.build()

# Hitung centrality metrics
centralities = builder.compute_centrality(graph)
print(f"PageRank scores: {centralities['pagerank']}")
```

### Contoh 3: Gunakan Fungsi Metrik Langsung

```python
from lkdi.metrics import detect_dormancy, calculate_rif, diffusion_distance

# Timeline sitasi per tahun
citations = [2, 1, 0, 1, 0, 0, 1, 2, 15, 45, 120, 300]

# Deteksi periode dormansi
dormant = detect_dormancy(citations, min_years=5)
print(f"Dormant period: {dormant}")

# Hitung RIF score
rif = calculate_rif(citations)
print(f"RIF Score: {rif}")
```

## 📁 Struktur Repository

```
latent-knowledge-diffusion-index/
├── lkdi/                      # Package utama
│   ├── __init__.py           # Export modul publik
│   ├── metrics.py            # Fungsi metrik inti (RIF, dormancy, dll)
│   ├── graph_builder.py      # Class CitationGraphBuilder
│   └── detector.py           # Class RevivalDetector
├── tests/                     # Test suite
│   ├── conftest.py           # Konfigurasi pytest
│   ├── test_metrics.py       # Test fungsi metrik
│   ├── test_graph_builder.py # Test graph builder
│   └── test_detector.py      # Test detector
├── requirements.txt          # Daftar dependensi
├── INSTALLATION.md           # Panduan instalasi detail
├── SETUP_LOCALHOST.md        # Setup localhost cepat
└── README.md                 # Dokumentasi ini
```

## 🧪 Pengujian

Jalankan seluruh test suite:

```bash
# Semua test dengan verbose output
python -m pytest tests/ -v

# Dengan coverage report
python -m pytest tests/ --cov=lkdi --cov-report=html

# Test spesifik
python -m pytest tests/test_metrics.py -v
```

## 🛠️ Development Tools

Repository ini menyertakan tools untuk development:

- **Black**: Code formatting (`black lkdi/ tests/`)
- **Flake8**: Linting (`flake8 lkdi/ tests/`)
- **Pytest**: Testing framework dengan coverage
- **Streamlit**: Dashboard visualisasi (opsional)

## 📚 Dokumentasi Lengkap

- **[INSTALLATION.md](INSTALLATION.md)**: Panduan instalasi detail dengan troubleshooting
- **[SETUP_LOCALHOST.md](SETUP_LOCALHOST.md)**: Setup cepat untuk pengembangan localhost
- **Docstrings**: Setiap fungsi dan class memiliki docstring lengkap

## 🔧 Troubleshooting Umum

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError` | Pastikan virtual environment aktif dan `pip install -r requirements.txt` sudah dijalankan |
| Gagal install dependency | Coba upgrade pip: `pip install --upgrade pip` |
| Timeout API OpenAlex | Periksa koneksi internet atau gunakan mode offline dengan data lokal |
| Test gagal | Pastikan versi Python ≥ 3.9 |

Untuk panduan troubleshooting lengkap, lihat [INSTALLATION.md](INSTALLATION.md#troubleshooting).

## 🗺️ Roadmap

- [x] ✅ Implementasi core metrics (RIF, dormancy detection)
- [x] ✅ Graph builder dengan NetworkX
- [x] ✅ RevivalDetector dengan OpenAlex integration
- [x] ✅ Test suite lengkap (32 tests)
- [ ] Visualisasi timeline interaktif dengan Streamlit
- [ ] Support multiple data sources (Crossref, PubMed)
- [ ] CLI interface untuk analisis batch
- [ ] Pre-trained models untuk ekstraksi konsep
- [ ] Dashboard web untuk eksplorasi data

## 🤝 Kontribusi

Kami menyambut kontribusi! Cara berkontribusi:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/amazing-feature`)
3. Commit perubahan (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buka Pull Request

Lihat [Issues](https://github.com/stipwunaraha/latent-knowledge-diffusion-index/issues) untuk task yang bisa dikerjakan.

### Standar Kode
- Gunakan Black untuk formatting
- Jalankan Flake8 untuk linting
- Pastikan semua test lulus sebelum submit PR
- Tambahkan test untuk fitur baru

## 📄 Lisensi

Distributed under the **MIT License**. Lihat [LICENSE](LICENSE) untuk detail.

## 🙏 Acknowledgements

- [OpenAlex](https://openalex.org/) - Sumber data bibliografik terbuka
- [Semantic Scholar](https://www.semanticscholar.org/) - API pencarian akademik
- [NetworkX](https://networkx.org/) - Library graf Python
- Konsep "Sleeping Beauties" dari ilmuometri

## 📬 Kontak

- Repository: [GitHub](https://github.com/stipwunaraha/latent-knowledge-diffusion-index)
- Issues: [Laporkan bug atau request fitur](https://github.com/stipwunaraha/latent-knowledge-diffusion-index/issues)

---

<p align="center">
  <strong>Dibuat dengan ❤️ untuk komunitas riset terbuka</strong>
</p>
