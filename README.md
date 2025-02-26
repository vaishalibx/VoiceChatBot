# VoiceChatBot

## Overview

Voice Bot is a simple voice interaction application built using Streamlit, which allows users to record their voice and receive responses from a language model. The application utilizes speech recognition to convert spoken input into text and then processes that text to generate a response.

## Features

- Record audio directly from the microphone.
- Convert speech to text using Google Speech Recognition.
- Interact with a language model to generate responses.
- User-friendly interface built with Streamlit.

## Requirements

To run this project, you need to have Python 3.7 or higher installed. The following libraries are required:

- `streamlit`
- `langchain-groq`
- `python-dotenv`
- `speechrecognition`
- `sounddevice`
- `numpy`
- `scipy`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add your environment variables:

   ```plaintext
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit application:

   ```bash
   streamlit run VoiceBot.py
   ```

2. Open your web browser and go to `http://localhost:8501` to access the Voice Bot interface.

3. Click the "Start Recording" button to record your voice. After recording, you can process the audio to receive a response from the voice bot.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for providing an easy way to create web applications.
- [Google Speech Recognition](https://cloud.google.com/speech-to-text) for converting speech to text.
- [Langchain](https://langchain.com/) for the language model integration.
