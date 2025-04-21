# EmpathyBot – Therapist-Inspired LLM Chatbot

EmpathyBot is an interactive AI chatbot that simulates therapist-like conversations. It leverages Meta’s LLaMA 3.2-1B-Instruct model with integrated sentiment analysis to generate emotionally aware responses. The system features a full-stack implementation using React (frontend) and Flask (backend).

---

## Tech Stack

- **LLM**: [LLaMA 3.2-1B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct)
- **Frontend**: React with dynamic chat UI and sentiment feedback
- **Backend**: Flask API with `transformers`, `torch`, and `datasets`
- **Sentiment Analysis**: `distilbert-base-uncased-finetuned-sst-2-english`

---

##  Getting Started

### 1. Backend Setup

```bash
cd backend
python3 -m venv chatbot_env
source chatbot_env/bin/activate
pip install -r requirements.txt
python app.py
```

The Flask backend will start on `http://localhost:5050`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`.

---

## Fine-Tuning (Optional, GPU Required)

This project includes a full training pipeline using the [EmpatheticDialogues dataset](https://huggingface.co/datasets/Estwld/empathetic_dialogues_llm):

- `emp_dia.py` – preprocesses and formats the dataset -- run the file to pre-process the data
- `fineTune.py` – trains LLaMA 3.2-1B using Hugging Face `Trainer`

### GPU + Model Note

> While the project is fully set up to fine-tune a LLaMA model, training was not completed due to limited GPU availability. The script `fineTune.py` is ready to run on machines with sufficient GPU recources
>
> The chatbot currently runs on the **pretrained** base model to demonstrate working system architecture.
>
> Once GPU resources are available, simply run:
> ```bash
> python fineTune.py
> ```
> …and point the bot to the trained model (see below).

---

## Model Swapping

You can easily switch between the base model and your own fine-tuned version:

In `llama3.py` (if you want to test model specifically):
```python
bot = EmpathyBot(use_finetuned_model=True)
```
In `app.py` (if you want to use model in the frontend):
```python
USE_FINE_TUNED_MODEL = True
```
Your trained model should be saved to: `./empathetic_model/`.
