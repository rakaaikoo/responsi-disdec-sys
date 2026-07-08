-- ============================================================
-- Responsi CPMK 1 - Praktikum Sistem Terdistribusi & Terdesentralisasi
-- Skema database sederhana: pegawai & produk
-- Jalankan via: docker exec -it yugabytedb-node1 ysqlsh -h yugabytedb-node1 -f /path/init.sql
-- atau copy-paste isi file ini ke ysqlsh interaktif
-- ============================================================

CREATE DATABASE responsi_db;
\c responsi_db

-- Tabel 1: pegawai
CREATE TABLE pegawai (
    id          SERIAL PRIMARY KEY,
    nama        VARCHAR(100) NOT NULL,
    jabatan     VARCHAR(50)  NOT NULL,
    departemen  VARCHAR(50)  NOT NULL,
    gaji        NUMERIC(12,2) NOT NULL
);

INSERT INTO pegawai (nama, jabatan, departemen, gaji) VALUES
('Andi Saputra',    'Backend Engineer',  'IT',         9500000),
('Budi Santoso',    'Data Analyst',      'IT',         8700000),
('Citra Ayu',       'UI/UX Designer',    'Product',    8200000),
('Dewi Lestari',    'Project Manager',   'Operasional',12500000),
('Eka Prasetyo',    'DevOps Engineer',   'IT',         10500000);

-- Tabel 2: produk
CREATE TABLE produk (
    id          SERIAL PRIMARY KEY,
    nama_produk VARCHAR(100) NOT NULL,
    kategori    VARCHAR(50)  NOT NULL,
    harga       NUMERIC(12,2) NOT NULL,
    stok        INTEGER      NOT NULL
);

INSERT INTO produk (nama_produk, kategori, harga, stok) VALUES
('Laptop ProBook 14',   'Elektronik', 8500000, 15),
('Mouse Wireless X1',   'Aksesoris',   150000, 120),
('Keyboard Mekanik K2', 'Aksesoris',   650000, 60),
('Monitor 24 inch',     'Elektronik', 1750000, 30),
('SSD NVMe 512GB',      'Komponen',    850000, 75);

-- ============================================================
-- Verifikasi (bukti) - jalankan setelah insert:
-- ============================================================
\dt
SELECT * FROM pegawai;
SELECT * FROM produk;
SELECT COUNT(*) AS total_pegawai FROM pegawai;
SELECT COUNT(*) AS total_produk FROM produk;
