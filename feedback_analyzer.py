import openai
import os
import json
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    return file_path


def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder to save the output")
    return folder_path


def translate_to_english(text):
    prompt = f"Translate the following text to English:\n\n{text}"
    client = openai.OpenAI(api_key=API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def analyze_feedback(feedback_text):
    prompt = f"""
    Analyze the following user feedback and return a JSON object:
    {{
        "category": "One of: Speed, Interface, Functionality, Bugs, Other",
        "problem": "A short description of the issue (if applicable)"
    }}

    Return ONLY valid JSON, no extra text.

    Feedback: "{feedback_text}"
    """
    client = openai.OpenAI(api_key=API_KEY)
    try:
        print(f"Processing: {feedback_text[:50]}...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        data = json.loads(result)  # Safe JSON parsing
        print(f"Category: {data['category']}, Problem: {data['problem']}")
        time.sleep(1)  # Avoid hitting API rate limits
        return data["category"], data["problem"]
    except Exception as e:
        print(f"Error analyzing feedback: {e}")
        return "Error", "Could not identify the problem"


def main():
    file_path = select_file()
    if not file_path:
        print("No file selected. Exiting.")
        return

    output_folder = select_output_folder()
    if not output_folder:
        print("No output folder selected. Exiting.")
        return

    feedback_df = pd.read_csv(file_path, encoding="utf-8")

    # Translate all feedback to English
    print("Translating feedback...")
    feedback_df["feedback"] = feedback_df["feedback"].apply(translate_to_english)

    # Analyze and categorize feedback
    print("Analyzing feedback...")
    feedback_df[["Category", "Problem"]] = feedback_df["feedback"].apply(
        lambda x: pd.Series(analyze_feedback(x))
    )

    # Save results
    output_path = os.path.join(output_folder, "categorized_feedback.csv")
    feedback_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Done! Results saved to: {output_path}")


if __name__ == "__main__":
    main()