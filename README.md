# 📊 ContentWatch

ContentWatch is a platform-agnostic content analytics and intelligence system designed for creators. It aggregates cross-platform social media data, normalizes it into a unified schema, and runs a lightweight analysis pipeline to deliver clear, actionable growth strategies rather than just raw, overwhelming dashboards.

Whether analyzing a long-form YouTube video, a viral TikTok, or an X thread, ContentWatch unifies performance metrics to build a comprehensive **Content DNA** profile for every creator.

---

## ⚡ Quick Start Guide

Get your local environment up and running in minutes.

### Prerequisites
Make sure you have the following installed on your machine:
* [Docker & Docker Compose](https://www.docker.com/)
* [Node.js](https://nodejs.org/) (with `pnpm` configured)

### Installation Steps

1. **Clone the repository & start backend services:**
   ```bash
   $ git clone git@github.com:XST-BD/ContentWatch.git
   $ cd ContentWatch
   $ cd server 
   $ docker compose build --parallel && docker compose up
   ```

2. **In a new terminal window, initialize and start the frontend client:**
   ```bash
   $ cd client 
   $ pnpm install && pnpm approve-builds 
   $ pnpm dev
   ```

### Accessing the Application
Once the local builds and compilation processes finish, you can access the stack at:
* 🌐 **User Interface:** [http://localhost:3000](http://localhost:3000)
* ⚙️ **REST API Gateway:** [http://localhost:8000](http://localhost:8000)

---

## 🚀 Features

* **🌐 Cross-Platform Ingestion:** Fetches and normalizes raw content data from multiple social media APIs (YouTube, TikTok, X, and more) into a standardized structure.
* **🧬 Content DNA Profiling:** Decodes creator tendencies by analyzing publishing patterns across formats, topics, timing, and durations.
* **💡 Actionable Insights:** Moves beyond passive vanity metrics to provide explicit recommendations on *what* to post, *when* to post, and *how* to optimize engagement.
* **📊 Performance Buckets (Breakdowns):** Automatically categorizes and compares performance across distinct content types, specific time slots, and video length ranges.
* **📈 Time-Series Analytics:** Tracks and visualizes complex historical trends in views and engagement over time.
* **🧩 Modular Architecture:** Built as a robust *modular monolith*, enforcing strict domain boundaries to allow individual pipelines to easily scale into independent microservices later.

---

## 🏗️ Architecture Overview

ContentWatch implements a complete intelligence loop, handling everything from raw data ingestion to user-facing strategic recommendations.

```text
       ┌────────────────────────┐
       │ External Platforms API │ (YouTube, TikTok, X, etc.)
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │    Fetcher Service     │ (External / Ingestion Layer)
       └───────────┬────────────┘
                   │ [Normalized Data]
                   ▼
       ┌────────────────────────┐
       │     Django Backend     │ (API Orchestration & Core Logic)
       └─────┬───────────┬──────┘
             │           │
             ▼           ▼
  ┌─────────────┐     ┌─────────────────┐
  │   Feature   │     │ Analysis Engine │ (Heuristics & ML-Ready)
  │ Engineering │     └────────┬────────┘
  └─────────────┘              │
                               ▼
                      ┌─────────────────┐
                      │   PostgreSQL    │ (Persistent Storage)
                      └────────┬────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │ Frontend (Nuxt) │ (User Interface / UI)
                      └─────────────────┘
```

* **Fetcher Service:** Connects to external APIs, handles rate limits, and standardizes raw payloads into a unified format.
* **Backend (Django + DRF):** Orchestrates data processing pipelines, calculates heuristics, and exposes standard RESTful endpoints.
* **Client (Nuxt + Tailwind CSS):** A fast, intuitive frontend for data visualization and strategy delivery.
* **Redis (Optional Extension):** Used as a high-speed caching tier for demanding time-series and breakdown operations.

---

## 🛠️ Tech Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | ![Nuxt](https://img.shields.io/badge/Nuxt-00DC82?style=flat-square&logo=nuxt.js&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white) |
| **Backend** | ![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white) ![DRF](https://img.shields.io/badge/DRF-FF0000?style=flat-square&logo=django&logoColor=white) |
| **Database & Cache** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white) *(Optional)* |
| **Authentication** | ![OAuth2](https://img.shields.io/badge/OAuth2-Django_OAuth_Google-4285F4?style=flat-square&logo=google&logoColor=white) |
| **DevOps & CI/CD** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white) |

---

## 🔌 API Reference

### Core Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/analyze/` | Triggers the underlying feature engineering/analysis pipeline and updates insights. |
| `GET` | `/api/insights/` | Returns the final, compiled strategic creator recommendations. |
| `GET` | `/api/content-dna/` | Retrieves the creator's behavioral profile (tendencies, formatting, timing). |
| `GET` | `/api/timeseries/` | Exposes engagement data mapped over historical time matrices. |
| `GET` | `/api/breakdowns/` | Returns multi-dimensional aggregated performance buckets. |

### Ingestion Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/ingest/{integration_id}/structured` | Exposes the post-normalization data payload. |
| `GET` | `/api/ingest/{integration_id}/raw` | Retrieves the immutable, raw API response from the source platform. |

---

## 🎯 Design Philosophy

ContentWatch aims to bridge the gap between **raw data collection** and **strategic content execution**. Most analytics platforms bury valuable conclusions under endless tabs of charts. ContentWatch prioritizes clarity—turning patterns into natural language rules that creators can immediately action in their next production cycle.

By implementing strict decoupling boundaries between our domains within a *modular monolith*, we keep development overhead light without boxing ourselves into a corner. When ingestion traffic bursts scale up, components like the `Fetcher Service` or the `Analysis Engine` can cleanly decouple into distributed microservices.

---

## 🔮 Future Roadmap

* [ ] Deep native connectors for expanded networks (Pinterest, Facebook).
* [ ] Integration of predictive ML pipelines for video viral-coefficient forecasting.
* [ ] Transition to Apache Kafka/RabbitMQ for real-time stream processing of analytics.
* [ ] Microservice decoupling and deployment targeting Kubernetes environments.
* [ ] Complex key-value caching optimizations via Redis layers.

---

## 📄 License

This project is licensed under the **GPL License**. See the `LICENSE` file for more details.
