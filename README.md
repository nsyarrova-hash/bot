# GForm Automation — Ekonomi + Sejarah

Project berisi 60 data mahasiswa:
- 30 Pendidikan Ekonomi
- 30 Pendidikan Sejarah

Script akan:
1. Membuka Google Form.
2. Mengisi Nama Lengkap.
3. Mengisi NIM.
4. Memilih Program Studi.
5. Memilih Angkatan dari 2 digit pertama NIM.
6. Klik Submit/Kirim otomatis.
7. Menunggu acak 2–5 menit.
8. Mengulang sampai semua data selesai.

## GitHub Actions

Workflow berada di:

`.github/workflows/gform.yml`

Jalankan dari GitHub melalui:

**Actions → GForm Automation → Run workflow**

### Penting
Form harus dapat diakses dan disubmit oleh browser tanpa login Google pada runner GitHub.
Jangan menyimpan password Google di repository atau GitHub Secrets untuk mencoba
mengotomatisasi login.

Jika form mewajibkan login akun tertentu, jalankan script secara lokal dengan
browser yang sudah login atau gunakan mekanisme autentikasi yang memang disediakan
dan diizinkan oleh akun/form tersebut.

## Instalasi lokal

```bash
pip install -r requirements.txt
playwright install chromium
python main.py
```
