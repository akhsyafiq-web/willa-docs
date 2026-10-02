---
title: Presensi
description: Cara melakukan check-in presensi harian di Willa PMS.
roles: [employee, hod, hrd]
status: published
last_updated: 2026-10-02
---

# Presensi

Presensi adalah fitur utama bagi Anda untuk melakukan check-in setiap hari kerja. Halaman ini menampilkan status shift hari ini dan riwayat kehadiran Anda.

## Ringkasan

Check-in presensi dimulai dari tombol pada halaman **Home**. Setelah menekan tombol tersebut, Anda melewati tiga tahap: **Selfie** untuk verifikasi wajah, **Geofence** untuk validasi lokasi, dan **Result** yang menampilkan hasil presensi. Presensi baru tercatat setelah seluruh tahap selesai.

## Siapa yang menggunakan

Semua peran — Employee, HOD, dan HRD — melakukan presensi lewat fitur ini.

## Prasyarat

- Perangkat Anda memiliki kamera dan akses lokasi (GPS) yang aktif.
- Anda berada di dalam area geofence lokasi kerja.
- Wajah Anda sudah terdaftar di sistem oleh HRD. Lihat [Face Registration](../employee-management/face-registration.md).
- Anda sudah memiliki jadwal shift untuk hari tersebut. Lihat [Scheduling](../shift-management/scheduling.md).

## Langkah-langkah

### Buka halaman Home

1. Buka Willa PMS. Halaman **Home** terbuka.

![Halaman Home menampilkan kartu sambutan, status shift hari ini, tombol Check-in Sekarang, kartu ringkasan Hadir Terlambat Absen, dan Riwayat Terakhir](./assets/01-halaman-home.png)

Halaman Home terdiri dari beberapa bagian.

| Bagian | Isi |
| ---------------- | --- |
| Kartu sambutan | Sapaan beserta tanggal hari ini. |
| Kartu shift | Status shift hari ini, misalnya **Tidak ada shift hari ini**, dan tombol **Check-in Sekarang**. |
| Kartu ringkasan | Jumlah **Hadir**, **Terlambat**, dan **Absen** Anda. |
| Riwayat Terakhir | Daftar presensi terakhir, dengan jam **Check In** dan **Check Out** per tanggal. Ketuk **Lihat Semua** untuk melihat riwayat lengkap. |

<small>Jika Anda sudah check-in tetapi belum check-out, tombol pada kartu shift berubah menjadi **Check-out Sekarang**. Panduan check-out dibahas terpisah.</small>

### Mulai check-in

1. Ketuk **Check-in Sekarang** pada kartu shift.
2. Halaman **Check In Presensi** terbuka.

![Halaman Check In Presensi dengan tombol Mulai Verifikasi dan Batal](./assets/02-mulai-verifikasi.png)

3. Ketuk **Mulai Verifikasi** untuk melanjutkan, atau **Batal** untuk kembali ke halaman Home.

### Berikan izin kamera dan lokasi

Jika izin belum pernah diberikan, dialog **Izin Diperlukan** muncul.

![Dialog Izin Diperlukan meminta akses Kamera dan Lokasi](./assets/03-dialog-izin.png)

| Izin | Kegunaan |
| ------ | --- |
| Kamera | Untuk verifikasi wajah. |
| Lokasi | Untuk memvalidasi geofence. |

> ℹ️ **Info:** Data kamera dan lokasi hanya dipakai untuk keperluan validasi presensi.

1. Ketuk **Izinkan dan Lanjutkan** untuk memberikan izin, atau **Kembali** untuk membatalkan.

### Ikuti tahap verifikasi

Verifikasi presensi terdiri dari tiga tahap yang ditampilkan pada indikator di bagian atas: **Selfie**, **Geofence**, dan **Result**.

#### Selfie

1. Posisikan wajah Anda dalam area sesuai instruksi di layar. Pastikan pencahayaan cukup dan wajah terlihat jelas.

![Tahap Selfie meminta Anda memposisikan wajah dalam area, dengan tombol Ambil Foto](./assets/04-tahap-selfie.png)

2. Ketuk **Ambil Foto**.
3. Pratinjau foto tampil. Ketuk **Ambil Lagi** untuk memotret ulang, atau **Lanjutkan** untuk memakai foto tersebut.

![Pratinjau foto presensi dengan tombol Ambil Lagi dan Lanjutkan](./assets/05-konfirmasi-foto.png)

Penjelasan lebih lanjut ada di halaman [Face Verification](face-verification.md).

#### Geofence

Setelah foto dikonfirmasi, sistem memvalidasi wajah dan lokasi Anda secara bersamaan.

![Layar Memvalidasi Wajah dan Lokasi](./assets/06-validasi.png)

Penjelasan lebih lanjut ada di halaman [Geofencing](geofencing.md).

#### Result

Layar hasil menampilkan status presensi Anda beserta ringkasan **Kecocokan Wajah** dan **Lokasi**.

![Layar hasil presensi menampilkan status, kecocokan wajah, lokasi, dan tombol Ulangi check in](./assets/07-hasil.png)

Jika presensi berhasil, layar menampilkan status keberhasilan dan presensi Anda tercatat.

![Layar hasil presensi berhasil](./assets/08-berhasil.png)

Jika presensi gagal, penyebabnya ditampilkan pada layar ini. Ketuk **Ulangi check in** untuk mencoba lagi dari tahap Selfie.

## Hasil

Setelah seluruh tahap verifikasi berhasil, presensi Anda tercatat dan muncul di **Riwayat Terakhir** pada halaman Home.

## Sub-fitur

- [Face Verification](face-verification.md): penjelasan lebih lanjut tentang verifikasi wajah saat presensi.
- [Geofencing](geofencing.md): penjelasan lebih lanjut tentang validasi lokasi saat presensi.

## Lihat juga

- [Fitur](../README.md)
- [Face Registration](../employee-management/face-registration.md)
- [Scheduling](../shift-management/scheduling.md)
- [Peran dan Hak Akses](../../getting-started/peran-dan-hak-akses.md)
