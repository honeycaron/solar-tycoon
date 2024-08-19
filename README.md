# Solar Tycoon

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/honeycaron/solar-tycoon.git)

## Overview

**Solar Tycoon: AI-Powered Review Analyzer for Local Businesses**

Solar Tycoon is an AI-driven platform designed to empower small business owners in Jeju Island by providing actionable insights from customer reviews. Developed by Team PLS (Hun Sohn, Ju Young Park, Su Min Lee), the project addresses the challenges of declining foot traffic and rapidly changing consumer trends that local businesses face.

### Development Background and Purpose

Jeju Island’s small businesses often struggle to stay competitive due to limited tools for understanding customer feedback in detail. Solar Tycoon bridges this gap by offering AI-powered sentiment analysis and real-time trend tracking, enabling businesses to quickly adapt and thrive. The project’s primary goal is to provide small business owners with easy access to deep insights derived from customer reviews.

### Main Features and Characteristics

Solar Tycoon offers a variety of features aimed at making sentiment analysis accessible and actionable:

- **Chatbot Interface:** An easy-to-use chatbot that simplifies interaction with the platform.
- **Real-Time Data Crawling:** Continuous data collection to keep insights up-to-date.
- **Sentiment Analysis:** Fine-tuned models designed specifically for analyzing customer reviews.
- **Multi-Model Approach:** Integrates Retrieval-Augmented Generation (RAG) and sentiment analysis for precise and reliable responses.
- **Interactive Visualization Tools:** Allows business owners to track sentiment trends and adjust strategies accordingly.

### Technology Stack and Upstage API Utilization

The project utilizes cutting-edge technology, including real-time data processing, natural language processing (NLP), and chatbot integration. The Upstage API is a critical component of the system’s architecture:

- **General Queries:** The "solar-1-mini-chat" and "solar-embedding-1-large" models are employed for data retrieval.
- **Sentiment Analysis:** The "solar-1-mini-chat" model, fine-tuned for sentiment classification, delivers highly accurate sentiment analysis. This model ensures consistent and reliable responses, allowing business owners to confidently use the insights.

### Social Impact and Innovation

Solar Tycoon is tailored specifically for Jeju’s local businesses, providing them with tools to boost customer satisfaction and adapt to market changes. By offering advanced AI solutions in an accessible format, the project supports digital transformation and promotes long-term economic growth in the region.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Upstage API Integration](#upstage-api-integration)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/honeycaron/solar-tycoon.git
    cd solar-tycoon
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory with the following content:

    ```bash
    UPSTAGE_API_KEY=add your upstage api key here
    PREDIBASE_API_KEY=add your predibase api key here
    ADAPTER_ID=review-classification-model_test1/1
    ```

    Replace the placeholders with your actual API keys and adapter ID.

## Usage

1. **Start the application using Streamlit:**

    ```bash
    streamlit run MY_리뷰_분석.py
    ```

2. **Access the web interface:**

    After running the above command, you can access the application in your browser at `http://localhost:8501` by default.

3. **Explore the Demo Server:**

    If you prefer to explore a live version of the project, you can visit our demo server at [http://3.38.50.229:8501/](http://3.38.50.229:8501/).

## Upstage API Integration

Solar Tycoon makes extensive use of the Upstage API for review classification and sentiment analysis. The integration is key to delivering high-quality insights for small business owners:

- **Review Classification Module:** The Upstage API is used for sentiment analysis and classification of customer reviews. The relevant code can be found in [`MY_리뷰_분석.py`](./MY_리뷰_분석.py).

    Example Integration:

    ```python
    from upstage import UpstageAPI
    import os

    api = UpstageAPI(api_key=os.getenv("UPSTAGE_API_KEY"))
    response = api.analyze_review("Sample review text")
    ```

- **Adapter ID for Model Usage:** The adapter specified by `ADAPTER_ID` is used to fine-tune the model for sentiment classification tasks, ensuring high accuracy.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

Feel free to reach out if you have any questions or issues. We hope Solar Tycoon provides valuable insights for your business and helps you stay competitive in a rapidly changing market!
