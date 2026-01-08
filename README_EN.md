# Mathurat Ticker  
**Read without forgetting.**

Mathurat Ticker is a calm, open source web application designed to help users read **Al Mathurat** in a structured and focused flow.

Each verse or supplication is presented one at a time, supported by a simple tick (gundal) system to ensure nothing is missed.  
There is no gamification, no performance pressure, and no user tracking.

This project is built for personal practice and for the benefit of the wider community.

---

## ✨ Key Features

- One verse per screen
- Tick based repetition tracking (gundal)
- Automatic morning and evening detection
- Mathurat Sugra and Kubra selection
- Start button to mark session intention
- Session duration shown after completion
- Quran verses rendered directly from a Quran API
- Non Quran supplications managed via CSV
- Transliteration and translations (Malay and English)
- Lightweight and mobile friendly
- No ads and no analytics

---

## 🧭 Simple User Flow

1. Open the application
2. Select Mathurat Sugra or Kubra
3. Press Start
4. Read one verse at a time
5. Tap the gundal according to repetition count
6. Complete the session and view reading duration

---

## 📁 Content Structure

All recitations are maintained in a CSV file as the single source of truth.

CSV fields include:

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
- session (morning / evening)
- set (sughra / kubra)

This approach allows:
- Easy content auditing
- Manual updates without touching code
- Safe community contributions

---

## 🛠️ Technology Stack

- Python
- Streamlit
- AlQuran Cloud API for Quran verse rendering

---

## 🤝 Contributions

This is an open source project and contributions are welcome.

You may contribute through:
- Code improvements
- Content review and corrections
- Translation enhancements
- UI and UX suggestions
- Documentation updates

Please open an issue or submit a pull request with good adab and intention.

---

## 🕌 Content Note

- Al Mathurat is a collection of authentic supplications compiled by Imam Hasan Al Banna
- The arrangement follows commonly accepted versions used in Southeast Asia
- Translations and transliterations are provided for understanding, not deep tafsir

If you notice any issues or have suggestions, please reach out.

---

## 📮 Contact

For issues, feedback, or collaboration:

📧 **hawadirect@gmail.com**

---

## ❤️ Support Us

If you find this project beneficial and would like to support its continued development:

👉 https://www.bizappay.my/qIKzmsvfiX

Donations are entirely optional and do not unlock any features.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🌱 Closing

Mathurat Ticker was built to support daily remembrance  
with calm, structure, and intention.

Read without forgetting.
