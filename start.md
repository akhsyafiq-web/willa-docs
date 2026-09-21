# Tugas: Buat skeleton repo dokumentasi Willa PMS (struktur saja, semua file kosong/draft)

## Konteks

Repo ini akan berisi dokumentasi "cara menggunakan" Willa PMS, yaitu HRIS mobile-first (PWA) untuk operasional hotel di Indonesia. Format: markdown polos (CommonMark/GFM) supaya bisa dibaca GitBook (Git Sync) maupun framework docs lain (Docusaurus, VitePress, MkDocs). Nanti akan di-host di subdomain docs.

Tugasmu HANYA membuat struktur folder dan file. JANGAN menulis konten dokumentasi apa pun.

## Aturan umum

1. Gunakan folder workspace saat ini sebagai root repo. Jangan membuat folder pembungkus.
2. Nama file dan folder: lowercase, kebab-case, tanpa spasi.
3. Semua file konten memakai TEMPLATE di bawah, persis, tanpa tambahan heading, paragraf, atau contoh apa pun.
4. Setiap folder `assets/` hanya berisi satu file kosong bernama `.gitkeep` (supaya folder kosong ikut ter-commit di Git).
5. Jangan menjalankan `git init`, `git commit`, atau install dependency apa pun.
6. Jangan membuat file atau folder selain yang tercantum di bagian STRUKTUR.

## Struktur

Tanda `→ "..."` adalah nilai `title` di front matter file tersebut.

```
.
├── README.md                          → "Dokumentasi Willa PMS"
├── SUMMARY.md                         → (isi khusus, lihat bagian SUMMARY.md)
├── .gitbook.yaml                      → (isi khusus, lihat bagian .gitbook.yaml)
│
├── assets/
│   └── .gitkeep
│
├── getting-started/
│   ├── README.md                      → "Getting Started"
│   ├── login-dan-aktivasi-akun.md     → "Login dan Aktivasi Akun"
│   ├── install-pwa.md                 → "Install PWA"
│   ├── peran-dan-hak-akses.md         → "Peran dan Hak Akses"
│   └── assets/.gitkeep
│
├── features/
│   ├── README.md                      → "Fitur"
│   │
│   ├── attendance/
│   │   ├── README.md                  → "Presensi"
│   │   ├── face-verification.md       → "Face Verification"
│   │   ├── geofencing.md              → "Geofencing"
│   │   ├── catatan-fitur.md
│   │   └── assets/.gitkeep
│   │
│   ├── shift-management/
│   │   ├── README.md                  → "Shift Management"
│   │   ├── shift-type.md              → "Shift Type"
│   │   ├── scheduling.md              → "Scheduling"
│   │   ├── log-history.md             → "Log History"
│   │   ├── catatan-fitur.md
│   │   └── assets/.gitkeep
│   │
│   ├── employee-management/
│   │   ├── README.md                  → "Employee Management"
│   │   ├── employee-list.md           → "Employee List"
│   │   ├── employee-detail.md         → "Employee Detail"
│   │   ├── face-registration.md       → "Face Registration"
│   │   ├── edit-employee.md           → "Edit Employee"
│   │   ├── catatan-fitur.md
│   │   └── assets/.gitkeep
│   │
│   ├── exit-permit/
│   │   ├── README.md                  → "Izin Keluar"
│   │   ├── catatan-fitur.md
│   │   └── assets/.gitkeep
│   │
│   ├── sick-leave/
│   │   ├── README.md                  → "Izin Sakit"
│   │   ├── catatan-fitur.md
│   │   └── assets/.gitkeep
│   │
│   ├── holiday-management/
│   │   ├── README.md                  → "Holiday Management"
│   │   ├── catatan-fitur.md
│   │   └── assets/.gitkeep
│   │
│   └── leave-management/
│       ├── README.md                  → "Leave Management"
│       ├── catatan-fitur.md
│       └── assets/.gitkeep
│
├── account-settings/
│   ├── README.md                      → "Akun & Pengaturan"
│   └── assets/.gitkeep
│
└── troubleshooting/
    ├── README.md                      → "Troubleshooting"
    └── assets/.gitkeep
```

## Template file konten (semua `.md` kecuali SUMMARY.md)

Ganti `{judul}` dengan nilai title dari struktur di atas.

```
---
title: {judul}
description: Panduan penggunaan {judul}.
roles: []
status: draft
last_updated: 2026-09-21
---

# {judul}

> 🚧 **Dokumentasi ini sedang dalam tahap pengembangan.**
> Konten halaman ini akan segera ditambahkan.
```

Pengecualian:

- File `README.md` di root: title "Dokumentasi Willa PMS", description "Panduan penggunaan Willa PMS, HRIS untuk operasional hotel."
- File `catatan-fitur.md`: title "Catatan Fitur: {Nama Fitur}" (Nama Fitur = title README di folder yang sama), description "Catatan Do & Don't untuk fitur {Nama Fitur}."
- `roles: []` sengaja dibiarkan kosong, akan diisi saat dokumentasi ditulis.

## SUMMARY.md

Buat dengan isi persis berikut:

```
# Summary

* [Beranda](README.md)

## Getting Started

* [Getting Started](getting-started/README.md)
  * [Login dan Aktivasi Akun](getting-started/login-dan-aktivasi-akun.md)
  * [Install PWA](getting-started/install-pwa.md)
  * [Peran dan Hak Akses](getting-started/peran-dan-hak-akses.md)

## Fitur

* [Fitur](features/README.md)
  * [Presensi](features/attendance/README.md)
    * [Face Verification](features/attendance/face-verification.md)
    * [Geofencing](features/attendance/geofencing.md)
    * [Catatan Fitur](features/attendance/catatan-fitur.md)
  * [Shift Management](features/shift-management/README.md)
    * [Shift Type](features/shift-management/shift-type.md)
    * [Scheduling](features/shift-management/scheduling.md)
    * [Log History](features/shift-management/log-history.md)
    * [Catatan Fitur](features/shift-management/catatan-fitur.md)
  * [Employee Management](features/employee-management/README.md)
    * [Employee List](features/employee-management/employee-list.md)
    * [Employee Detail](features/employee-management/employee-detail.md)
    * [Face Registration](features/employee-management/face-registration.md)
    * [Edit Employee](features/employee-management/edit-employee.md)
    * [Catatan Fitur](features/employee-management/catatan-fitur.md)
  * [Izin Keluar](features/exit-permit/README.md)
    * [Catatan Fitur](features/exit-permit/catatan-fitur.md)
  * [Izin Sakit](features/sick-leave/README.md)
    * [Catatan Fitur](features/sick-leave/catatan-fitur.md)
  * [Holiday Management](features/holiday-management/README.md)
    * [Catatan Fitur](features/holiday-management/catatan-fitur.md)
  * [Leave Management](features/leave-management/README.md)
    * [Catatan Fitur](features/leave-management/catatan-fitur.md)

## Akun & Pengaturan

* [Akun & Pengaturan](account-settings/README.md)

## Troubleshooting

* [Troubleshooting](troubleshooting/README.md)
```

## .gitbook.yaml

Buat dengan isi persis:

```
root: ./
structure:
  readme: README.md
  summary: SUMMARY.md
```

## Verifikasi setelah selesai

1. Tampilkan tree final folder (tanpa node_modules atau folder tersembunyi selain `.gitkeep` dan `.gitbook.yaml`).
2. Pastikan setiap link di SUMMARY.md menunjuk ke file yang benar-benar ada.
3. Pastikan tidak ada file konten yang isinya lebih dari template (front matter + H1 + notice).
4. Laporkan jumlah total file yang dibuat, dan sebutkan jika ada yang menyimpang dari instruksi ini.
