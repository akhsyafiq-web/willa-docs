# Panduan Penulisan Dokumentasi Willa PMS

Dokumen internal untuk penulis. File ini **tidak** dimasukkan ke `SUMMARY.md`, jadi tidak tampil di navigasi docs.

Tujuan panduan ini: semua halaman punya struktur dan gaya yang sama, dan tetap terbaca di GitBook maupun framework docs lain (Docusaurus, VitePress, MkDocs).

## Prinsip dasar

1. Gunakan Markdown standar (CommonMark/GFM). HTML hanya dipakai untuk hal yang tidak bisa dicapai Markdown, dan terbatas pada `<figure>`, `<figcaption>`, `<small>`, dan `<details>`.
2. Jangan memakai sintaks khusus platform, misalnya `{% hint %}`, `{% tabs %}`, `{% embed %}`, komponen MDX/JSX, atau atribut `style="..."`.
3. Markdown hanya menentukan **struktur**. Ukuran huruf, warna abu-abu, dan tampilan kotak diatur oleh CSS/theme di hosting, bukan di file `.md`.

---

## 1. Bahasa

- Bahasa Indonesia formal, sapaan "Anda".
- Istilah teknis tetap dalam bahasa Inggris (contoh: shift, check-in, geofencing).
- Nama tombol, menu, tab, dan field ditulis persis seperti di aplikasi, termasuk huruf besar-kecilnya.
- Kalimat aktif, satu ide per paragraf, idealnya tidak lebih dari 25 kata per kalimat.
- Langkah selalu diawali kata kerja: "Ketuk", "Pilih", "Isi", "Simpan".

## 2. Front matter (wajib di setiap halaman)

```yaml
---
title: Face Verification
description: Cara melakukan presensi dengan verifikasi wajah.
roles: [employee]
status: draft
last_updated: 2026-09-21
---
```

| Field          | Aturan                                                 |
| -------------- | ------------------------------------------------------ |
| `title`        | Sama dengan H1 halaman.                                |
| `description`  | Satu kalimat, diawali "Cara ..." atau "Panduan ...".   |
| `roles`        | Salah satu atau lebih dari `employee`, `hod`, `hrd`.   |
| `status`       | `draft` atau `published`.                              |
| `last_updated` | Format `YYYY-MM-DD`. Perbarui setiap kali isi berubah. |

---

## 3. Heading

| Level | Markdown         | Fungsi                                           |
| ----- | ---------------- | ------------------------------------------------ |
| H1    | `# Judul`        | Judul halaman. **Tepat satu** per halaman.       |
| H2    | `## Bagian`      | Bagian utama (section).                          |
| H3    | `### Sub-bagian` | Rincian dalam satu section.                      |
| H4    | `#### Rincian`   | Hanya jika terpaksa. Jangan lebih dalam dari H4. |

Aturan:

- Jangan melompati level (H2 langsung ke H4).
- Huruf kapital hanya di awal kalimat, kecuali nama fitur atau nama elemen UI.
- Tanpa titik di akhir, tanpa emoji, tanpa huruf tebal, dan tanpa link di dalam heading.
- Beri jarak satu baris kosong sebelum dan sesudah heading.

## 4. Teks isi

### Body 1: paragraf utama

Paragraf biasa. Dipakai untuk penjelasan utama. Panjang 1 sampai 3 kalimat.

```md
Halaman ini menjelaskan cara Employee melakukan presensi dengan verifikasi wajah.
```

### Body 2: teks pendukung

Teks sekunder yang ukurannya lebih kecil dari Body 1. Dipakai untuk keterangan tambahan singkat, misalnya pengecualian atau syarat khusus. Maksimal 2 kalimat. Ditulis dengan tag `<small>` di dalam paragraf sendiri.

```md
<small>Fitur ini hanya tersedia untuk peran HRD.</small>
```

Ukuran huruf sebenarnya diatur oleh theme hosting.

### Content text: isi konten

| Kebutuhan                              | Format                                       |
| -------------------------------------- | -------------------------------------------- |
| Langkah berurutan                      | List bernomor (`1.`), satu aksi per langkah. |
| Daftar tidak berurutan                 | List bertanda (`-`).                         |
| Perbandingan atau referensi            | Tabel dengan baris header, maksimal 5 kolom. |
| Nilai yang diketik atau tampil literal | Inline code (`` `08:00` ``).                 |

Aturan tambahan:

- List bersarang maksimal 1 level.
- Jangan menaruh gambar di tengah kalimat. Gambar selalu berdiri sendiri (lihat bagian 7).
- Setelah langkah terakhir, tulis hasilnya dalam satu kalimat, misalnya "Data karyawan berhasil disimpan."

## 5. Penekanan teks

| Gaya      | Penulisan    | Dipakai untuk                                                                           |
| --------- | ------------ | --------------------------------------------------------------------------------------- |
| **Tebal** | `**teks**`   | Nama elemen UI (tombol, menu, tab, field) dan istilah kunci saat pertama didefinisikan. |
| _Miring_  | `_teks_`     | Istilah asing yang belum umum, hanya saat pertama muncul di halaman.                    |
| `Kode`    | `` `teks` `` | Nilai literal yang diketik atau tampil di layar. Bukan untuk nama tombol.               |

Aturan:

- Gunakan underscore (`_teks_`) untuk miring, bukan tanda bintang.
- Jangan menebalkan satu kalimat penuh.
- Jangan menggabungkan tebal dan miring.
- Jangan memakai garis bawah, huruf kapital semua, atau tanda seru.

Contoh:

```md
Ketuk tombol **Simpan**, lalu pilih jam masuk `08:00`.
```

## 6. Link

```md
[Scheduling](../shift-management/scheduling.md)
[Situs GitBook](https://gitbook.com)
```

- Teks link harus deskriptif. Jangan menulis "klik di sini".
- Link antar halaman memakai **path relatif ke file `.md`**, bukan URL absolut.
- Link ke bagian dalam halaman memakai anchor: `[Langkah 2](#langkah-langkah)`.
- Link eksternal memakai URL lengkap `https://`.
- Jangan menaruh link di dalam heading. Jangan menulis URL mentah di tengah kalimat.
- Kumpulkan halaman terkait di akhir halaman dalam bagian `## Lihat juga`.

---

## 7. Gambar, GIF, dan file

### Gambar dan GIF

```md
![Layar presensi dengan kamera aktif](./assets/01-layar-presensi.png)
```

- Alt text wajib dan harus menjelaskan isi gambar. Jangan menulis "gambar" atau "screenshot".
- Letakkan gambar di folder `assets/` yang sama dengan halamannya. Aset yang dipakai banyak halaman ditaruh di `/assets/` di root.
- Penamaan: `NN-deskripsi-kebab.ext`, dengan `NN` adalah urutan di halaman (`01`, `02`, ...).
- Screenshot memakai PNG. GIF hanya untuk alur singkat: maksimal 10 detik, 3 MB, dan lebar 1000 px.
- Satu gambar untuk satu langkah atau satu ide.
- Gambar berdiri sendiri di paragrafnya, dengan baris kosong di atas dan bawah.
- **Samarkan data pribadi** karyawan (nama, NIK, foto wajah, nomor telepon) sebelum mengambil screenshot. Gunakan data contoh.

### Gambar dengan caption

Pakai `<figure>` hanya jika gambar memerlukan keterangan.

```html
<figure>
  <img
    src="./assets/01-layar-presensi.png"
    alt="Layar presensi dengan kamera aktif"
  />
  <figcaption>Gambar 1. Layar presensi saat kamera aktif.</figcaption>
</figure>
```

- Caption satu kalimat, diawali "Gambar N." bila ada lebih dari satu gambar.
- Jangan memakai sintaks Markdown di dalam `<figcaption>` (tebal, link, dll.).
- Beri baris kosong sebelum `<figure>` dan setelah `</figure>`.

### File unduhan

```md
[Unduh template import karyawan (XLSX, 45 KB)](./assets/template-import-karyawan.xlsx)
```

Tulis selalu nama file, format, dan ukurannya di teks link.

### Video

Jangan meng-embed video. Gunakan GIF untuk alur pendek, atau link biasa ke video untuk yang panjang.

## 8. Caption dan teks abu-abu

Warna abu-abu **tidak** ditulis di Markdown. Gunakan elemen semantik, lalu theme yang mewarnai:

| Kebutuhan               | Elemen                             |
| ----------------------- | ---------------------------------- |
| Caption gambar atau GIF | `<figcaption>` di dalam `<figure>` |
| Keterangan singkat lain | `<small>` (Body 2)                 |

Jangan memakai `style="color:gray"`, `<font>`, atau `<span style>`. Atribut itu dibuang oleh banyak platform.

## 9. Border dan pemisah

Markdown tidak punya border bawaan. Gunakan cara berikut:

| Kebutuhan                       | Cara                                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| Pemisah antar kelompok bagian   | Garis horizontal `---`, dengan baris kosong di atas dan bawah. Pakai hemat, tidak di setiap H2. |
| Kotak dengan border penuh       | Tabel satu kolom (lihat contoh). Pakai hemat.                                                   |
| Kotak dengan garis di sisi kiri | Blockquote atau callout (lihat bagian 11).                                                      |
| Border pada screenshot          | Sudah ada di dalam file gambar (lihat catatan).                                                 |

Contoh kotak border penuh:

```md
| Contoh                     |
| -------------------------- |
| Isi kotak ditulis di sini. |
```

**Catatan border screenshot:** ekspor screenshot berlatar putih dengan border 1 px berwarna `#e5e5e5` (warna border design system Willa). Border menjadi bagian dari file gambar, jadi tampil sama di hosting mana pun. Developer tidak menambahkan border lagi lewat CSS.

---

## 10. Section text

Setiap H2 adalah satu section dan diawali paragraf pengantar Body 1 (1 sampai 3 kalimat) sebelum list, tabel, atau gambar.

### Rangka halaman

| Jenis halaman      | Urutan H2                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------ |
| `README.md` fitur  | Ringkasan, Siapa yang menggunakan, Prasyarat, Sub-fitur, Lihat juga                        |
| Sub-fitur          | Ringkasan, Sebelum memulai, Langkah-langkah, Hasil, Pertanyaan umum (opsional), Lihat juga |
| `catatan-fitur.md` | Lakukan, Jangan, Catatan tambahan (opsional)                                               |

Di `catatan-fitur.md`, setiap butir di bagian Lakukan diawali ✅ dan setiap butir di bagian Jangan diawali ❌.

### Section lipat

Untuk FAQ atau detail opsional, gunakan `<details>`. Jangan dipakai untuk langkah utama. Baris kosong setelah `<summary>` wajib ada supaya Markdown di dalamnya tetap ter-render.

```html
<details>
  <summary>Apa yang terjadi jika wajah tidak terdeteksi?</summary>

  Sistem meminta Anda mengulangi verifikasi. Pastikan pencahayaan cukup.
</details>
```

## 11. Hint dan callout

Ditulis sebagai blockquote satu paragraf, diawali emoji dan label tebal:

```md
> ℹ️ **Info:** Presensi hanya bisa dilakukan di dalam area geofence.
```

| Jenis     | Awalan                | Dipakai untuk                                                          |
| --------- | --------------------- | ---------------------------------------------------------------------- |
| Info      | `> ℹ️ **Info:**`      | Tips atau konteks tambahan.                                            |
| Perhatian | `> ⚠️ **Perhatian:**` | Risiko atau konsekuensi, misalnya tindakan yang tidak bisa dibatalkan. |
| Lakukan   | `> ✅ **Lakukan:**`   | Praktik yang dianjurkan.                                               |
| Jangan    | `> ❌ **Jangan:**`    | Praktik yang harus dihindari.                                          |

Aturan:

- Maksimal 3 kalimat per callout, dan maksimal 2 callout per section.
- Jangan menaruh dua callout berurutan tanpa teks di antaranya.
- Jangan menaruh langkah utama di dalam callout.
- Emoji hanya boleh dipakai untuk callout, butir di `catatan-fitur.md`, dan notice 🚧 pada halaman draft. Jangan memakai emoji lain di heading atau isi.

---

## 12. Sebelum halaman diubah menjadi `published`

- [ ] Front matter lengkap dan `roles` sudah diisi.
- [ ] Hanya ada satu H1 dan tidak ada heading yang dilompati.
- [ ] Semua gambar punya alt text dan berada di folder `assets/`.
- [ ] Semua link relatif menuju file yang ada.
- [ ] Tidak ada sintaks khusus platform atau atribut `style`.
- [ ] Data pribadi di screenshot sudah disamarkan.
- [ ] Notice 🚧 pada halaman draft sudah dihapus.
- [ ] `status` diubah menjadi `published` dan `last_updated` diperbarui.
- [ ] Halaman sudah terdaftar di `SUMMARY.md`.

## Catatan untuk developer

- Repo ini berisi beberapa file yang bukan halaman docs: `STYLE-GUIDE.md` dan `.gitbook.yaml`. Jika hosting memindai semua file `.md` (misalnya Docusaurus), kecualikan `STYLE-GUIDE.md`.
- Elemen HTML berikut perlu diuji di hosting final: `<small>`, `<figure>`/`<figcaption>`, dan `<details>`. Jika `<small>` tidak dirender, Body 2 cukup ditampilkan sebagai paragraf biasa.
- Styling yang perlu ditambahkan di theme (jika tidak sudah bawaan):

```css
figcaption {
  color: #737373;
  font-size: 0.875rem;
  text-align: center;
}
small {
  color: #525252;
  font-size: 0.875rem;
}
blockquote {
  border-left: 3px solid #e5e5e5;
  padding-left: 1rem;
}
```
