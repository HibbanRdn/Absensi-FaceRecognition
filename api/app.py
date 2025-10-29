from flask import Flask, jsonify, request, render_template, redirect, url_for, session, send_file
import sqlite3
import os, json, base64, re
from datetime import datetime
import numpy as np
from scipy.spatial.distance import cosine
from deepface import DeepFace
import traceback
import tempfile

# ============================================================
# KONFIGURASI APLIKASI
# ============================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "absensi.db")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = "absensi_secret_key"

# ============================================================
# DATABASE HELPERS
# ============================================================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Buat tabel jika belum ada (users, absensi).
    Memudahkan bila database baru / belum diinisialisasi.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      embedding TEXT NOT NULL,
      npm TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS absensi (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      waktu TEXT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

# panggil inisialisasi DB saat start
init_db()

# ============================================================
# ROUTES UTAMA
# ============================================================
@app.route("/")
def index():
    return redirect(url_for("absen"))

# ============================================================
# ABSEN MAHASISWA
# ============================================================
@app.route("/absen")
def absen():
    return render_template("absen.html")

@app.route("/absensi", methods=["GET", "POST"])
def absensi():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        # coba terima JSON body (biasanya dipakai untuk webcam base64)
        try:
            data = request.get_json(silent=True) or {}
        except Exception:
            data = {}

        # Mode 1: user_id langsung
        if "user_id" in data:
            try:
                user_id = int(data["user_id"])
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("INSERT INTO absensi (user_id, waktu) VALUES (?, ?)", (user_id, waktu))
                conn.commit()
                cur.execute("SELECT name, npm FROM users WHERE id = ?", (user_id,))
                user = cur.fetchone()
                conn.close()
                if user:
                    return jsonify({
                        "recognized": True,
                        "name": user["name"],
                        "npm": user["npm"],
                        "waktu": waktu
                    })
                else:
                    return jsonify({"recognized": False, "message": "User tidak ditemukan"}), 404
            except Exception as e:
                conn.close()
                return jsonify({"recognized": False, "message": f"Error penyimpanan absensi: {str(e)}"}), 500

        # Mode 2: image base64 (mis. dari canvas.toDataURL)
        if "image" in data:
            try:
                img_str = re.sub("^data:image/.+;base64,", "", data["image"])
                img_bytes = base64.b64decode(img_str)
                temp_fd, temp_path = tempfile.mkstemp(suffix=".jpg", dir=BASE_DIR)
                os.close(temp_fd)
                with open(temp_path, "wb") as f:
                    f.write(img_bytes)

                embedding = DeepFace.represent(img_path=temp_path, model_name="Facenet")[0]["embedding"]

                cur.execute("SELECT id, name, npm, embedding FROM users")
                users = cur.fetchall()

                best_match = None
                min_distance = 1.0
                for user in users:
                    try:
                        stored_embedding = np.array(json.loads(user["embedding"]))
                        distance = cosine(embedding, stored_embedding)
                        if distance < min_distance and distance < 0.4:
                            min_distance = distance
                            best_match = user
                    except Exception:
                        # skip user jika embedding corrupt
                        continue

                os.remove(temp_path)

                if best_match:
                    user_id, name, npm = best_match["id"], best_match["name"], best_match["npm"]
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cur.execute("INSERT INTO absensi (user_id, waktu) VALUES (?, ?)", (user_id, waktu))
                    conn.commit()
                    conn.close()
                    return jsonify({
                        "recognized": True,
                        "name": name,
                        "npm": npm,
                        "waktu": waktu
                    })
                else:
                    conn.close()
                    return jsonify({"recognized": False, "message": "Wajah tidak dikenali"}), 200

            except Exception as e:
                try:
                    if 'temp_path' in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)
                except Exception:
                    pass
                conn.close()
                tb = traceback.format_exc()
                return jsonify({"recognized": False, "message": f"Gagal absensi: {str(e)}", "trace": tb}), 500

        # Jika request bukan JSON image/user_id, kembalikan error
        return jsonify({"recognized": False, "message": "Format data tidak dikenali"}), 400

    # GET semua absensi (return JSON)
    try:
        cur.execute("""
            SELECT a.id, u.name, u.npm, a.waktu
            FROM absensi a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.waktu DESC
        """)
        rows = [dict(row) for row in cur.fetchall()]
        conn.close()
        return jsonify(rows)
    except Exception as e:
        conn.close()
        return jsonify({"success": False, "message": f"Gagal ambil data absensi: {e}"}), 500

# ============================================================
# REGISTER (menerima multipart/form-data via AJAX / FormData)
# Mengembalikan JSON agar frontend AJAX mudah menanganinya
# ============================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Terima form-data (AJAX FormData atau form biasa)
        name = request.form.get("name")
        npm = request.form.get("npm")
        image = request.files.get("image")

        if not (name and npm and image):
            # kembalikan JSON supaya frontend AJAX dapat menangani
            return jsonify({"success": False, "message": "Data tidak lengkap! (name, npm, image diperlukan)"}), 400

        # simpan ke temporary file yang aman
        temp_fd, temp_path = tempfile.mkstemp(suffix=".jpg", dir=BASE_DIR)
        os.close(temp_fd)
        try:
            image.save(temp_path)

            # buat embedding
            new_embedding = DeepFace.represent(img_path=temp_path, model_name="Facenet")[0]["embedding"]

            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT id, name, npm, embedding FROM users")
            existing_users = cur.fetchall()

            THRESHOLD = 8.0
            for user in existing_users:
                try:
                    stored_embedding = np.array(json.loads(user["embedding"]))
                    distance = np.linalg.norm(np.array(new_embedding) - stored_embedding)
                    if distance < THRESHOLD:
                        conn.close()
                        # hapus file temp lalu kembalikan pesan
                        try:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                        except Exception:
                            pass
                        return jsonify({
                            "success": False,
                            "message": f"Wajah sudah terdaftar sebagai {user['name']} (NPM: {user['npm']})!"
                        }), 400
                except Exception:
                    # jika parsing embedding gagal, skip user itu
                    continue

            # simpan user baru
            cur.execute("INSERT INTO users (name, npm, embedding) VALUES (?, ?, ?)",
                        (name, npm, json.dumps(new_embedding)))
            conn.commit()
            conn.close()

            # bersihkan temporary file
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass

            return jsonify({"success": True, "message": "Registrasi berhasil!"})

        except Exception as e:
            # bersihkan file jika ada
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass

            tb = traceback.format_exc()
            return jsonify({"success": False, "message": f"Gagal registrasi: {str(e)}", "trace": tb}), 500

    # GET -> render halaman register (HTML)
    return render_template("register.html")

# ============================================================
# LOGIN & LOGOUT ADMIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Username atau password salah")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

# ============================================================
# DASHBOARD
# ============================================================
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ============================================================
# EXPORT CSV
# ============================================================
@app.route("/export/csv")
def export_absensi():
    if not session.get("admin"):
        return redirect(url_for("login"))

    filepath = os.path.join(BASE_DIR, "absensi_export.csv")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, u.name, u.npm, a.waktu
        FROM absensi a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.waktu DESC
    """)
    rows = cur.fetchall()
    conn.close()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("ID,Name,NPM,Waktu\n")
        for row in rows:
            f.write(f"{row['id']},{row['name']},{row['npm']},{row['waktu']}\n")

    return send_file(filepath, as_attachment=True, download_name="absensi.csv")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
