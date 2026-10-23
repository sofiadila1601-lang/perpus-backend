import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Mengambil DATABASE_URL langsung dari Environment Variable Vercel
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# ==================== MODEL DATABASE ====================

class Kategori(db.Model):
    __tablename__ = 'kategori'
    id_kategori = db.Column(db.Integer, primary_key=True)
    nama_kategori = db.Column(db.String(100), nullable=False)

class Buku(db.Model):
    __tablename__ = 'buku'
    id_buku = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(255), nullable=False)
    pengarang = db.Column(db.String(150))
    penerbit = db.Column(db.String(150))
    tahun_terbit = db.Column(db.Integer)
    stok = db.Column(db.Integer, default=0)
    id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id_kategori'))

class Anggota(db.Model):
    __tablename__ = 'anggota'
    id_anggota = db.Column(db.Integer, primary_key=True)
    nama_anggota = db.Column(db.String(150), nullable=False)
    tipe_anggota = db.Column(db.String(50))
    prodi_atau_jabatan = db.Column(db.String(100))
    no_telepon = db.Column(db.String(20))

class Peminjaman(db.Model):
    __tablename__ = 'peminjaman'
    id_peminjaman = db.Column(db.Integer, primary_key=True)
    id_anggota = db.Column(db.Integer, db.ForeignKey('anggota.id_anggota'))
    tanggal_pinjam = db.Column(db.Date)
    tanggal_kembali_rencana = db.Column(db.Date)
    status = db.Column(db.String(20), default='Dipinjam')

class DetailPeminjaman(db.Model):
    __tablename__ = 'detail_peminjaman'
    id_detail = db.Column(db.Integer, primary_key=True)
    id_peminjaman = db.Column(db.Integer, db.ForeignKey('peminjaman.id_peminjaman'))
    id_buku = db.Column(db.Integer, db.ForeignKey('buku.id_buku'))
    jumlah = db.Column(db.Integer, default=1)

# ==================== ROUTE / ENDPOINT ====================

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Selamat datang di API Backend Sistem Informasi Perpustakaan!"
    })

# --- ENDPOINT BUKU (CRUD LENGKAP) ---

# 1. READ ALL (GET)
@app.route('/api/buku', methods=['GET'])
def get_buku():
    list_buku = Buku.query.all()
    results = [{
        "id_buku": b.id_buku,
        "judul": b.judul,
        "pengarang": b.pengarang,
        "penerbit": b.penerbit,
        "tahun_terbit": b.tahun_terbit,
        "stok": b.stok,
        "id_kategori": b.id_kategori
    } for b in list_buku]
    return jsonify({"status": "success", "data": results}), 200

# 2. READ ONE (GET)
@app.route('/api/buku/<int:id>', methods=['GET'])
def get_buku_by_id(id):
    buku = Buku.query.get(id)
    if not buku:
        return jsonify({"error": "Buku tidak ditemukan"}), 404
    
    return jsonify({
        "status": "success",
        "data": {
            "id_buku": buku.id_buku,
            "judul": buku.judul,
            "pengarang": buku.pengarang,
            "penerbit": buku.penerbit,
            "tahun_terbit": buku.tahun_terbit,
            "stok": buku.stok,
            "id_kategori": buku.id_kategori
        }
    }), 200

# 3. CREATE (POST)
@app.route('/api/buku', methods=['POST'])
def add_buku():
    data = request.json
    if not data or not data.get('judul'):
        return jsonify({"error": "Field judul wajib diisi"}), 400

    new_buku = Buku(
        judul=data.get('judul'),
        pengarang=data.get('pengarang'),
        penerbit=data.get('penerbit'),
        tahun_terbit=data.get('tahun_terbit'),
        stok=data.get('stok', 0),
        id_kategori=data.get('id_kategori')
    )
    db.session.add(new_buku)
    db.session.commit()
    return jsonify({"status": "success", "message": "Buku berhasil ditambahkan!"}), 201

# 4. UPDATE (PUT / PATCH)
@app.route('/api/buku/<int:id>', methods=['PUT', 'PATCH'])
def update_buku(id):
    buku = Buku.query.get(id)
    if not buku:
        return jsonify({"error": "Buku tidak ditemukan"}), 404

    data = request.json
    if 'judul' in data: buku.judul = data['judul']
    if 'pengarang' in data: buku.pengarang = data['pengarang']
    if 'penerbit' in data: buku.penerbit = data['penerbit']
    if 'tahun_terbit' in data: buku.tahun_terbit = data['tahun_terbit']
    if 'stok' in data: buku.stok = data['stok']
    if 'id_kategori' in data: buku.id_kategori = data['id_kategori']

    db.session.commit()
    return jsonify({"status": "success", "message": "Data buku berhasil diperbarui!"}), 200

# 5. DELETE
@app.route('/api/buku/<int:id>', methods=['DELETE'])
def delete_buku(id):
    buku = Buku.query.get(id)
    if not buku:
        return jsonify({"error": "Buku tidak ditemukan"}), 404

    db.session.delete(buku)
    db.session.commit()
    return jsonify({"status": "success", "message": "Buku berhasil dihapus!"}), 200

# --- ENDPOINT KATEGORI ---
@app.route('/api/kategori', methods=['GET'])
def get_kategori():
    list_kategori = Kategori.query.all()
    results = [{"id_kategori": k.id_kategori, "nama_kategori": k.nama_kategori} for k in list_kategori]
    return jsonify({"status": "success", "data": results}), 200

@app.route('/api/kategori', methods=['POST'])
def add_kategori():
    data = request.json
    if not data or not data.get('nama_kategori'):
        return jsonify({"error": "Field nama_kategori wajib diisi"}), 400

    new_kat = Kategori(nama_kategori=data.get('nama_kategori'))
    db.session.add(new_kat)
    db.session.commit()
    return jsonify({"status": "success", "message": "Kategori berhasil ditambahkan!"}), 201

# --- ENDPOINT ANGGOTA ---
@app.route('/api/anggota', methods=['GET'])
def get_anggota():
    list_anggota = Anggota.query.all()
    results = [{
        "id_anggota": a.id_anggota,
        "nama_anggota": a.nama_anggota,
        "tipe_anggota": a.tipe_anggota,
        "prodi_atau_jabatan": a.prodi_atau_jabatan,
        "no_telepon": a.no_telepon
    } for a in list_anggota]
    return jsonify({"status": "success", "data": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
