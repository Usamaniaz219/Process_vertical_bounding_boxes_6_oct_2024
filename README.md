

---

# **Text Extraction and OCR Processing with EasyOCR and OpenCV**

This repository contains scripts for processing images, detecting text regions, and applying OCR using **EasyOCR** and **OpenCV**. It includes two main scripts:

1. **Tile Processing and OCR Extraction** - Splits images into tiles, detects text, and identifies tilted bounding boxes.
2. **Rotated Bounding Box Extraction and OCR** - Extracts, rotates, and processes tilted text regions before applying OCR.

---

## **📌 Features**
- **Image tiling** with overlapping regions.
- **EasyOCR-based text detection** for better recognition.
- **Mask-based bounding box extraction** for tilted text.
- **Rotation of detected text** for improved readability.
- **Final annotation and storage** of extracted text.

---

## **📂 Repository Structure**
```
📦 text-extraction-ocr
│-- 📂 data/                         # Sample images and masks
│-- 📜 tile_processing.py             # Script for tiling and OCR extraction
│-- 📜 rotated_bbox_extraction.py     # Script for extracting and rotating text regions
│-- 📜 requirements.txt               # Dependencies
│-- 📜 README.md                      # Documentation
```

---

## **🚀 Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/text-extraction-ocr.git
   cd text-extraction-ocr
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **🛠️ Usage**

### **1️⃣ Tile Processing and OCR Extraction**
- Detects text in image tiles and saves masks for tilted text.

Run:
```bash
python tile_processing.py
```

### **2️⃣ Rotated Bounding Box Extraction and OCR**
- Extracts and rotates text regions from the mask before OCR.

Run:
```bash
python rotated_bbox_extraction.py
```

---

## **📌 Outputs**
- **rotated_bboxes_on_blank.png** → Image with rotated text regions.
- **ocr_rotated_bboxes_annotated.png** → OCR-annotated image.
- **Amberley-Ohio.txt** → Extracted text saved to a file.

---

## **📜 License**
This project is open-source under the MIT License.

---

## **📩 Contact**
For any issues or improvements, feel free to open an **Issue** or contribute via a **Pull Request**.

---

Let me know if you need modifications! 🚀
