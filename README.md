<p align="center">
  <img src="assets/your_project_logo_or_banner.png" alt="AI Challenge 2024 Project Banner" width="700"/>
  <!-- **THAY THẾ 'assets/your_project_logo_or_banner.png' BẰNG LOGO HOẶC BANNER DỰ ÁN CỦA BẠN (NẾU CÓ)** -->
</p>

<h1 align="center">AI Challenge 2024 - Multi-Modal Video Event Retrieval</h1>

<p align="center">
  <em>A sophisticated system for querying and retrieving specific events from videos using text, image, and audio inputs.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI_Challenge_2024-Top_10_Finalist-brightgreen?style=for-the-badge" alt="Top 10 Finalist Badge"/>
  <!-- You can add more badges like build status, license, etc. -->
</p>

<p align="center">
  <b>Team:</b> Tứ Đại Thạch Hầu
  <br>
  <b>Members:</b> Khanh Duy Ho, Minh Duy Nguyen, Van Diep Tran, Hong Son Nguyen
</p>

<p align="center">
  <img src="assets/members.jpg" alt="Team Tứ Đại Thạch Hầu" width="80%" style="border-radius: 10px;"/>
  <!-- Consider adjusting width and adding a border-radius for a polished look -->
</p>

---

## 🌟 Project Overview

This project introduces an advanced **video retrieval system** designed to accurately and efficiently locate specific events within video content based on diverse query types: **text, image, and audio**. By harnessing the power of cutting-edge deep learning models and robust vector databases, our system significantly accelerates the query process while maintaining high precision in identifying relevant video segments.

---

## 🚀 System Architecture

Our solution is architected with a user-centric frontend and a powerful backend, ensuring a seamless and effective user experience:

- 🎨 **Frontend (ReactJS):**

  - Delivers an intuitive and interactive user interface.
  - Allows users to effortlessly submit queries through text input, image uploads, or audio recordings.
  - Presents search results in a clear, organized, and visually engaging manner.

- ⚙️ **Backend (FastAPI):**
  - Serves as the core processing engine, intelligently handling multi-modal queries.
  - Orchestrates communication with sophisticated deep learning models for feature extraction and understanding.
  - Manages high-performance interactions with **Milvus** (for vector similarity search) and **Elasticsearch** (for textual data indexing and search), ensuring rapid and accurate data retrieval.

---

## 🖼️ System Snapshots

A glimpse into our system's interface and capabilities:

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="assets/capture-1.png" alt="System Interface - Query Input" width="300"/><br><sub>Query Input Interface</sub></td>
      <td align="center"><img src="assets/capture-2.jpeg" alt="System Interface - Image Query Results" width="300"/><br><sub>Image Query Results</sub></td>
      <td align="center"><img src="assets/capture-3.jpeg" alt="System Interface - Text Query Results" width="300"/><br><sub>Text Query Results</sub></td>
    </tr>
    <tr>
      <td align="center"><img src="assets/capture-4.jpeg" alt="System Interface - Frame Details" width="300"/><br><sub>Detailed Frame View</sub></td>
      <td align="center"><img src="assets/capture-5.jpeg" alt="System Interface - Audio Query" width="300"/><br><sub>Audio Query Processing</sub></td>
      <td align="center"><img src="assets/capture-6.png" alt="System Interface - Results Ranking" width="300"/><br><sub>Ranked Search Results</sub></td>
    </tr>
     <tr>
      <td align="center"><img src="assets/capture-8.jpeg" alt="System Interface - Another View 1" width="300"/><br><sub>Additional View 1</sub></td>
      <td align="center"><img src="assets/capture-9.jpeg" alt="System Interface - Another View 2" width="300"/><br><sub>Additional View 2</sub></td>
      <td align="center"><img src="assets/capture-10.jpeg" alt="System Interface - Another View 3" width="300"/><br><sub>Additional View 3</sub></td>
    </tr>
  </table>
</div>

---

## 🛠️ Core Implementation Details

Our system employs a multi-stage process to deliver accurate and fast video retrieval:

### 1. Intelligent Video Processing & Frame Selection

- **Frame Segmentation & Deduplication:** Input videos are meticulously segmented into constituent frames. To optimize processing and storage, redundant or non-informative frames are intelligently discarded by analyzing the similarity of their embedding vectors.
- **Embedding Generation & Similarity Matching:** We utilize state-of-the-art models like **CLIP** and **CLIP4Clip** to transform both video frames and user queries into rich, high-dimensional embedding vectors. The relevance between a query and video frames is then precisely quantified using `cosine similarity`.
  <p align="center">
    <img src="assets/cosine_similarity.png" alt="Cosine Similarity Calculation" width="400"/>
    <br><sub><em>Conceptual representation of Cosine Similarity.</em></sub>
  </p>

### 2. Multi-Modal Information Extraction

- **Optical Character Recognition (OCR):** OCR technology is employed to extract textual information directly from video frames. This enriches the metadata associated with each frame, significantly boosting search accuracy for queries containing specific text.
- **Automated Speech Recognition (ASR):** For videos with spoken content (e.g., from YouTube), subtitles or transcriptions are extracted. This adds a crucial layer of semantic information, enabling effective retrieval based on spoken dialogue.

### 3. High-Performance Data Indexing & Retrieval

- **Milvus Vector Database:** The core of our similarity search relies on Milvus, a highly scalable and efficient open-source vector database. Milvus stores and indexes the embedding vectors of video frames, facilitating rapid similarity searches through optimized indexing structures (e.g., HNSW, IVF_FLAT), which dramatically reduces query latency.
- **Elasticsearch Integration:** Complementing Milvus, Elasticsearch is utilized for robust indexing and searching of textual data extracted via OCR and ASR. This dual-database approach allows for powerful hybrid searches, combining semantic vector similarity with keyword-based textual matching.

### 4. Advanced Result Reranking & Query Fusion

- To provide the most pertinent results, the system incorporates a sophisticated **reranking mechanism**. Search results originating from different query modalities (text, image, OCR, ASR) and feature extractors are intelligently combined and re-ordered, ensuring that the final output optimally aligns with the user's intent.

<p align="center">
  <em>Thank you for exploring our AI Challenge 2024 project!</em>
</p>
