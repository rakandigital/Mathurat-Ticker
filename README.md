# Mathurat Ticker  
**Baca tanpa lupa.**

Mathurat Ticker ialah aplikasi web open source yang dibina untuk membantu pembacaan **Al Mathurat** secara tertib, fokus, dan tenang.  
Setiap bacaan dipaparkan satu persatu dengan sistem tick (gundal) bagi memastikan tiada ayat yang tertinggal, tanpa tekanan prestasi atau gamifikasi.

Aplikasi ini dibina untuk kegunaan peribadi dan komuniti, tanpa iklan, tanpa tracking, dan tanpa paksaan.

---

## ✨ Ciri Utama

- One ayat one screen
- Sistem gundal untuk tracking ulangan bacaan
- Auto kesan waktu pagi atau petang
- Pilihan Mathurat Sugra dan Kubra
- Butang Start untuk menetapkan niat dan mula sesi
- Paparan tempoh masa selepas selesai bacaan
- Ayat Quran dipaparkan terus dari API Quran
- Doa dan zikir bukan Quran diselenggara melalui fail CSV
- Transliteration dan terjemahan (BM & English)
- Ringan, minimal, dan sesuai untuk mobile

---

## 🧭 Aliran Penggunaan Ringkas

1. Buka aplikasi
2. Pilih Mathurat Sugra atau Kubra
3. Tekan butang Start
4. Baca ayat satu persatu
5. Tekan gundal mengikut bilangan bacaan
6. Selesai dan lihat tempoh masa bacaan

---

## 📁 Struktur Kandungan

Kandungan bacaan disimpan dalam fail CSV sebagai sumber utama.

Contoh medan CSV:

- id
- order
- title
- type (quran / dua)
- surah
- ayah
- arabic
- transliteration
- translation_ms
- translation_en
- repeat
- session (pagi / petang)
- set (sughra / kubra)

Pendekatan ini membolehkan:
- Kandungan disemak dan diaudit dengan mudah
- Penyelenggaraan tanpa ubah kod
- Sumbangan komuniti yang lebih selamat

---

## 🛠️ Teknologi Digunakan

- Python
- Streamlit
- AlQuran Cloud API (untuk paparan ayat Quran)

---

## 🤝 Sumbangan

Projek ini terbuka untuk sumbangan.

Anda boleh menyumbang melalui:
- Penambahbaikan kod
- Semakan kandungan
- Pembetulan terjemahan
- Cadangan UI dan UX
- Dokumentasi

Sila buat pull request atau buka issue dengan adab dan niat yang baik.

---

## 🕌 Nota Kandungan

- Al Mathurat adalah himpunan zikir dan doa ma’thur yang dinisbahkan kepada Imam Hasan Al Banna
- Susunan dan kandungan dirujuk kepada versi yang masyhur digunakan di Nusantara
- Terjemahan dan transliterasi adalah untuk kefahaman, bukan tafsiran mendalam

Sekiranya terdapat kesilapan atau cadangan pembetulan, sumbangan amat dialu alukan.

---

## ❤️ Support Us

Jika aplikasi ini memberi manfaat dan anda ingin menyokong pembangunan berterusan:

Support Us  
(Sumbangan adalah sukarela dan tiada sebarang unlock feature)

👉 https://www.bizappay.my/qIKzmsvfiX
---

## 📜 Lesen

MIT License

---

## 🌱 Penutup

Mathurat Ticker dibina dengan niat untuk memudahkan ibadah harian  
tanpa gangguan, tanpa paksaan, dan tanpa lupa.

Semoga ia memberi manfaat, walaupun kecil.

Baca tanpa lupa.
