
# PaperQueryAI

PaperQueryAI is a web application that allows users to query an AI model to get answers solely based on research papers. The application integrates a language model (LLM) to provide responses derived strictly from academic and peer-reviewed sources.

## Features

- Query an AI model using research papers.
- Get accurate answers based on academic sources.
- Focus on research-based data without irrelevant information.

## Installation

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/KeshavG69/PaperQueryAI.git
   ```

2. Navigate into the project directory:
   ```bash
   cd PaperQueryAI
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**:
   - Obtain your API key from the service provider (e.g., OpenAI, Hugging Face, etc.).
   - Create a `.env` file in the project directory.
   - Add your API key to the `.env` file like so:
     ```
     SERPAPI_KEY=your-api-key-here
     GOOGLE_API_KEY=your-api-key-here
     ```
   - The application will read this key from the `.env` file using the `python-dotenv` library (if you're using this library).

## Running the Application

1. To run the application using Streamlit, use the following command:
   ```bash
   streamlit run app.py
   ```

2. The app should open in your default browser. You can now interact with the AI model and query based on research papers.

## Contact

Your Name - [@KeshavG69](https://github.com/KeshavG69)

Project Link: [https://github.com/KeshavG69/PaperQueryAI](https://github.com/KeshavG69/PaperQueryAI)
