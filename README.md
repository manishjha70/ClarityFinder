# ClarityFinder


https://github.com/user-attachments/assets/3a0bc364-cb4c-4d3b-9d26-c98d059d7ef8



## Overview

ClarityFinder is a powerful web query summarization tool that utilizes Gemini AI to deliver concise, relevant search results directly from the web. Designed for users who want to avoid sifting through countless pages, ClarityFinder aggregates and summarizes content, saving time and enhancing productivity.

## Why Use ClarityFinder?

- **Efficiency**: Get quick answers without the hassle of browsing multiple websites.
- **AI-Powered Summarization**: Benefit from advanced AI that condenses information into easily digestible summaries.
- **User-Friendly Interface**: Access the tool through a simple web interface, making it easy for anyone to use.

## Features

- **AI Summarization**: Utilizes Gemini AI for high-quality summaries.
- **Interactive Web Interface**: A clean and intuitive interface for submitting queries and viewing results.
- **Fast Results**: Quickly retrieves and summarizes information based on user queries.

## Getting Started

### Prerequisites
- Python 3.11 or higher

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/manishjha70/clarityfinder.git
   cd clarityfinder
   ```

2. **Install Dependencies**:
   Ensure you have pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your [Gemini API key](https://aistudio.google.com/) & [Tavily API Key](https://app.tavily.com/):
   ```plaintext
   TAVILY_API_KEY=your_tavily_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

### Running the Application

1. **Start the Server**:
   ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access ClarityFinder**:
   Open your web browser and navigate to `http://127.0.0.1:8000`.

### Using ClarityFinder

1. Enter your query in the input box on the homepage.
2. Click "Submit" to process your query.
3. The summarized result will be displayed along with the source URL.

### Code Explanation

- **Agent Creation**: ClarityFinder employs a Langchain agent configured with the Gemini AI model and a search tool (`TavilySearchResults`).
- **Data Processing**: The tool processes user input, invokes the AI for summarization, and returns both the summarized content and source URLs.
- **Web Framework**: Built using FastAPI for efficient and straightforward request handling.

## Conclusion

ClarityFinder is an innovative solution for users seeking fast and efficient information retrieval. By harnessing the power of Gemini AI, it streamlines the research process, making it accessible and user-friendly.
