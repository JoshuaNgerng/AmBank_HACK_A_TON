# Financial Intelligence Platform

An end-to-end financial document intelligence application built with FastAPI, React, and PostgreSQL, powered by Azure AI Intelligence.
The platform extracts, structures, and analyzes financial reports, then enables users to ask natural-language financial questions and receive explainable answers.

---

## 🚀 Features

- 📄 OCR & Document Processing

  - Upload financial reports (PDFs, scans, etc.)

  - Uses Azure AI Intelligence to perform OCR on documents

-  🧩 Smart Chunking & Information Extraction

   - Groups extracted text into semantically related chunks

   - Applies AI models to extract structured financial data

   - Stores processed data in PostgreSQL

- 💬 AI-Powered Financial Q&A

   - Ask natural-language questions about uploaded company reports

   - Returns accurate, contextual answers with explanations

   - Uses extracted financial knowledge as the source of truth

- 🐳 Dockerized Architecture

   - Fully containerized using Docker Compose

   - Simple one-command startup

---

# 🏗️ Architecture Overview
```
Frontend (React)
      |
      v
Backend (FastAPI)
      |
      +--> Azure AI Intelligence (OCR & AI Extraction)
      |
      v
Database (PostgreSQL)
```

---
# 🧰 Tech Stack

## Backend
- FastAPI

- Python

- Azure AI Intelligence

- PostgreSQL

## Frontend

- React

- JavaScript / TypeScript

## Infrastructure

- Docker

- Docker Compose
---

## 📦 Project Structure
```
.
├── backend/        # FastAPI application
├── frontend/       # React application
├── db/             # Database-related files (migrations, init scripts)
├── docker-compose.yml
└── README.md

```

---

## ⚙️ Getting Started

Prerequisites

- Docker

- Docker Compose

- Azure AI credentials (OCR / AI services)

---


Environment Variables

Create a .env file in the root directory and configure the following:

```
POSTGRES_DB=db_name 
POSTGRES_PASSWORD=12345
POSTGRES_USER=user

SECRET_KEY=some_key

APP_NAME=app_name

AZURE_TARGET_URL=url_ai
AZURE_API_KEY=api_key_ai
AZURE_DOC_URL=url_ocr
AZURE_DOC_KEY=api_key_ocr
```

---
## Run the Application

Start all services with:
```
docker-compose up --d
```

- Frontend: http://localhost:5173

- Backend API: http://localhost:8000

- API Docs (Swagger): http://localhost:8000/api/docs

---

# 🔌 API Overview

## Upload Financial Reports

- Accepts financial documents

- Performs OCR and AI-based extraction

- Saves structured data to the database

## Ask Financial Questions

- Ask questions about uploaded companies

- Uses AI reasoning over extracted data

- Returns answers with explanations

---

## 🧠 How It Works

1. User uploads financial documents

2. Azure AI performs OCR and text extraction

3. Text is grouped into meaningful financial chunks

4. AI extracts structured financial insights

5. Data is stored in PostgreSQL

6.  User queries are answered using extracted knowledge with reasoning

---

## 🔒 Security & Data Integrity

- No raw documents are modified

- Extracted data is validated before persistence

- Answers are grounded in stored financial data

---

## 📈 Future Improvements

- Multi-company comparison

- Financial trend visualization

- User authentication & access control

- Caching for faster Q&A responses

---

## Additional sources

- presentation deck
https://www.canva.com/design/DAG-SKDQjb4/A1-OkNjE8pGxUHt6l6nsjw/view?utm_content=DAG-SKDQjb4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h34477e93f8



---

## 📄 License

This project is licensed under the MIT License.


--- 