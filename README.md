# 📸 Absensi Face Recognition  

Sistem **Absensi Otomatis Berbasis Pengenalan Wajah (Face Recognition)** menggunakan **Python** dan **Flask**.  
Aplikasi ini dikembangkan untuk mempermudah proses pencatatan kehadiran secara real-time melalui kamera dengan deteksi wajah otomatis.

---

## 💬 Languages & Frameworks  

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7E017?style=for-the-badge&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

#### 🧠 AI / Computer Vision  
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Dlib](https://img.shields.io/badge/Dlib-006400?style=for-the-badge&logo=python&logoColor=white)
![Face_Recognition](https://img.shields.io/badge/Face_Recognition-2E8B57?style=for-the-badge&logo=python&logoColor=white)

---

## 🚀 Fitur Utama

- 🔍 **Pengenalan wajah otomatis** menggunakan kamera real-time.  
- 🧠 **Pelatihan dan deteksi wajah** berbasis library `face_recognition`.  
- 💾 **Database absensi** menggunakan SQLite.  
- 📊 **Ekspor data ke CSV** untuk keperluan laporan.  
- 🌐 **Antarmuka web** dengan Flask + HTML/CSS.  

---

## 🧩 Struktur Folder

```bash
Absensi-FaceRecognition/
│
├── api/                  # Endpoint backend (Flask)
├── face_recognition/     # Modul pengenalan & pelatihan wajah
├── static/               # File CSS, JS, dan aset statis
├── templates/            # Template HTML (Flask Jinja2)
│
├── absensi.db            # Database SQLite
├── absensi_export.csv    # File hasil ekspor absensi
├── requirements.txt      # Daftar dependensi Python
└── README.md             # Dokumentasi proyek
```
---

## ⚙️ Instalasi dan Menjalankan Proyek

### 1️⃣ Clone Repositori

```bash
git clone https://github.com/HibbanRdn/Absensi-FaceRecognition.git
cd Absensi-FaceRecognition
```

### 2️⃣ Buat Virtual Environment (Opsional)

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependensi

```bash
pip install -r requirements.txt
```

### 4️⃣ Jalankan Aplikasi

```bash
python app.py
```

Buka browser dan akses:

```
http://127.0.0.1:5000
```

---

## 🧠 Teknologi yang Digunakan

| Komponen         | Teknologi                      |
| ---------------- | ------------------------------ |
| Backend          | Flask (Python)                 |
| Face Recognition | face_recognition, OpenCV, dlib |
| Database         | SQLite3                        |
| Frontend         | HTML, CSS, JavaScript          |
| Ekspor Data      | CSV                            |

---

## 📸 Cara Penggunaan

1. Jalankan aplikasi Flask.
2. Buka halaman utama melalui browser.
3. Tambahkan data wajah pengguna menggunakan kamera.
4. Saat pengguna datang, sistem mengenali wajah dan mencatat waktu hadir.
5. Admin dapat mengekspor data absensi ke file CSV.

---

## 🗃️ Struktur Database

| Kolom         | Deskripsi        |
| ------------- | ---------------- |
| `id`          | Primary key      |
| `nama`        | Nama pengguna    |
| `waktu_absen` | Waktu absensi    |
| `status`      | Status kehadiran |

---

## 📤 Ekspor Data

File ekspor (`absensi_export.csv`) berisi data absensi lengkap dan dapat dibuka dengan Excel atau Google Sheets.

---

## 🛡️ Keamanan & Privasi

> ⚠️ Sistem ini hanya untuk keperluan pendidikan dan riset.
> Data wajah digunakan secara lokal tanpa dikirim ke server eksternal.
> Pastikan privasi pengguna tetap dijaga.

---

## 🧩 Rencana Pengembangan

* 🔐 Tambah fitur login admin.
* 🗓️ Integrasi absensi harian dan laporan otomatis.
* ☁️ Deployment ke server Ubuntu atau Raspberry Pi.
* 📱 Pengembangan versi mobile berbasis Flutter (opsional).

---

## 👨‍💻 Pengembang

**Nama:** Muhamad Hibban Ramadhan
**Universitas:** Universitas Lampung (Unila)
**Program Studi:** Teknik Informatika
📧 *[hibban.rdn@example.com](mailto:hibbanrdn@gmail.com)* 

---

## 🪪 Lisensi

Proyek ini bersifat **open-source** dan dapat digunakan untuk keperluan pendidikan.
Mohon sertakan atribusi jika digunakan dalam proyek lain.
