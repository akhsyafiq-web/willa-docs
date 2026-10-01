---
title: Presensi
description: Cara melakukan check-in presensi harian di Willa PMS.
roles: [employee, hod, hrd]
status: draft
last_updated: 2026-10-01
---

# Presensi

Presensi adalah halaman utama bagi Anda untuk melakukan check-in setiap hari kerja, menampilkan info shift hari ini dan riwayat kehadiran.

## Ringkasan

Halaman **Home** menampilkan status shift hari ini dan tombol untuk check-in. Setelah check-in, Anda melalui proses verifikasi lewat kamera (selfie) dan lokasi (geofence) sebelum presensi tercatat.

## Siapa yang menggunakan

Semua peran — Employee, HOD, dan HRD — melakukan presensi lewat halaman ini.

## Prasyarat

- Perangkat Anda punya kamera dan akses lokasi (GPS) yang aktif.
- Anda berada di dalam area geofence lokasi kerja.
- Wajah Anda sudah terdaftar di sistem oleh HRD. Lihat [Face Registration](../employee-management/face-registration.md).

## Langkah-langkah

### Buka halaman Home

1. Buka Willa PMS. Halaman **Home** terbuka.

![Halaman Home menampilkan kartu shift hari ini dengan tombol Check-in Sekarang, kartu ringkasan Hadir/Terlambat/Absen, dan Riwayat Terakhir](./assets/01-halaman-home.png)

Halaman Home terdiri dari beberapa bagian.

| Bagian | Isi |
| ---------------- | --- |
| Kartu shift | Status shift hari ini (misalnya belum ditentukan), status keterlambatan, dan tombol **Check-in Sekarang**. |
| Kartu ringkasan | Jumlah **Hadir**, **Terlambat**, dan **Absen** Anda. |
| Riwayat Terakhir | Daftar presensi terakhir, dengan jam **Check In** dan **Check Out** per tanggal. Ketuk **Lihat Semua** untuk melihat riwayat lengkap. |

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

Verifikasi presensi terdiri dari tiga tahap: **Selfie**, **Geofence**, dan **Result**.

![Tahap Selfie meminta Anda memposisikan wajah dalam area, dengan tombol Ambil Foto](./assets/04-tahap-selfie.png)

1. Posisikan wajah Anda dalam area sesuai instruksi di layar.
2. Ketuk **Ambil Foto**.

<small>Detail tahap Geofence dan Result akan ditambahkan di pembaruan berikutnya.</small>

## Hasil

Setelah seluruh tahap verifikasi selesai, presensi Anda tercatat dan muncul di **Riwayat Terakhir** pada halaman Home.

## Sub-fitur

- [Face Verification](face-verification.md): penjelasan lebih lanjut tentang verifikasi wajah saat presensi.
- [Geofencing](geofencing.md): penjelasan lebih lanjut tentang validasi lokasi saat presensi.

## Lihat juga

- [Fitur](../README.md)
- [Peran dan Hak Akses](../../getting-started/peran-dan-hak-akses.md)
