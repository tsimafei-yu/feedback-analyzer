# feedback-analyzer

A Python tool that automatically categorizes user feedback using the OpenAI API (GPT-4).

## What it does

- Loads a CSV file with user feedback in any language
- Translates each entry to English via GPT-4
- Categorizes each entry into: Speed, Interface, Functionality, Bugs, or Other
- Exports results to a new CSV file

## Requirements

- Python 3.10+
- OpenAI API key

## Installation

```bash
git clone https://github.com/tsimafei-yu/feedback-analyzer.git
cd feedback-analyzer
pip install openai pandas python-dotenv
```

## Configuration

Create a `.env` file in the project root and add your API key:
feedback
The app is very slow
App crashes on startup
Interface is hard to navigate

Run the script:

```bash
python feedback_analyzer.py
```

A file picker will open — select your CSV and choose an output folder. The results will be saved as `categorized_feedback.csv`.

## Tech Stack

- Python 3.10+
- OpenAI API (GPT-4)
- pandas
- tkinter
- python-dotenv

## Author

Tsimafei Yutskevich — [LinkedIn](https://linkedin.com/in/tsimafei-yutskevich)
