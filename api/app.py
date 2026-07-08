"""
Responsi CPMK 2 - REST API menggunakan Python (Flask)
Mengekspos data tabel pegawai & produk dari YugabyteDB (YSQL, PostgreSQL-compatible)
dalam format JSON.

Cara jalan (Windows PowerShell):
    python -m venv venv
    venv\\Scripts\\activate
    pip install -r requirements.txt
    python app.py

Endpoint:
    GET /                       -> info API
    GET /api/pegawai            -> semua pegawai
    GET /api/pegawai/<id>       -> pegawai berdasarkan id
    GET /api/produk             -> semua produk
    GET /api/produk/<id>        -> produk berdasarkan id
"""

from flask import Flask, jsonify
import pg8000.native

app = Flask(__name__)

# Konfigurasi koneksi ke YugabyteDB YSQL
# Jika API dijalankan di host Windows (bukan di dalam container),
# gunakan host=localhost karena port 5433 sudah di-mapping oleh docker-compose.
DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "responsi_db",
    "user": "yugabyte",
    "password": "yugabyte",
}


def get_connection():
    return pg8000.native.Connection(**DB_CONFIG)


def query_all(sql, params=None):
    conn = get_connection()
    try:
        rows = conn.run(sql, **(params or {}))
        columns = [c["name"] for c in conn.columns]
        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


@app.route("/")
def index():
    return jsonify({
        "message": "REST API Responsi - Sistem Terdistribusi & Terdesentralisasi",
        "endpoints": [
            "/api/pegawai",
            "/api/pegawai/<id>",
            "/api/produk",
            "/api/produk/<id>",
        ]
    })


@app.route("/api/pegawai", methods=["GET"])
def get_pegawai():
    data = query_all("SELECT id, nama, jabatan, departemen, gaji FROM pegawai ORDER BY id;")
    return jsonify({"status": "success", "count": len(data), "data": data})


@app.route("/api/pegawai/<int:pegawai_id>", methods=["GET"])
def get_pegawai_by_id(pegawai_id):
    data = query_all(
        "SELECT id, nama, jabatan, departemen, gaji FROM pegawai WHERE id = :pid;",
        {"pid": pegawai_id}
    )
    if not data:
        return jsonify({"status": "error", "message": "Pegawai tidak ditemukan"}), 404
    return jsonify({"status": "success", "data": data[0]})


@app.route("/api/produk", methods=["GET"])
def get_produk():
    data = query_all("SELECT id, nama_produk, kategori, harga, stok FROM produk ORDER BY id;")
    return jsonify({"status": "success", "count": len(data), "data": data})


@app.route("/api/produk/<int:produk_id>", methods=["GET"])
def get_produk_by_id(produk_id):
    data = query_all(
        "SELECT id, nama_produk, kategori, harga, stok FROM produk WHERE id = :pid;",
        {"pid": produk_id}
    )
    if not data:
        return jsonify({"status": "error", "message": "Produk tidak ditemukan"}), 404
    return jsonify({"status": "success", "data": data[0]})


if __name__ == "__main__":
    # Jalankan di semua interface agar bisa diakses dari browser/curl
    app.run(host="0.0.0.0", port=5000, debug=True)
