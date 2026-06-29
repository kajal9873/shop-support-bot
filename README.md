# Multilingual Customer Support Bot for Local Shops

A bilingual (Hindi-English code-mixed) RAG-based customer support chatbot 
for small/local retail shops — handles order status, FAQs, and product 
queries in natural Hinglish input.

**Live Demo:** [https://shop-wave-gamma.vercel.app/] 

<img width="1918" height="1087" alt="image" src="https://github.com/user-attachments/assets/32be3690-85f1-432a-81de-f00ad61e7a70" />

**Backend API:** [https://shopwave-backend-wdbs.onrender.com]


## 🎯 Research Focus

This project doubles as a research study on **NLU robustness for 
code-mixed Hindi-English queries** in low-resource, domain-specific 
chatbot settings. See [`research/`](./research) for datasets, evaluation 
scripts, and results.

**Key questions explored:**
- How does intent/NER accuracy degrade as code-mixing intensity increases?
- Does Roman→Devanagari transliteration normalization improve NLU performance?
- Are multilingual embeddings retrieval-consistent across script variants 
  (Hindi / Romanized / English) of the same query?

## 🏗️ Architecture

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI |
| NLU | Custom CMI calculator, transliteration, intent classifier |
| Retrieval | ChromaDB + multilingual sentence-transformers |
| LLM | Groq (LLaMA3) |
| Frontend | React + Vite |
| DB | SQLite (dev) / Postgres (prod) |

## 🚀 Quick Start

```bash
git clone https://github.com/kajal9873/shop-support-bot.git
cd shop-support-bot
cp .env.example .env   # add your GROQ_API_KEY

docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

### Manual setup (without Docker)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## 📊 Research / Evaluation

```bash
cd research/eval
python codemix_ratio_analysis.py      # CMI bucketing
python intent_accuracy_eval.py        # accuracy by CMI bucket
python ner_eval.py                    # entity F1, code-mixed vs mono
python retrieval_eval.py              # Hit@K / MRR across script forms
python transliteration_eval.py        # normalization ablation
```

Results saved to `research/results/`.

## 📁 Project Structure

See full structure in [project layout](#) — key folders:
- `backend/app/nlu/` — code-mix detection, normalization, intent/NER
- `backend/app/rag/` — retrieval pipeline
- `research/` — paper-core datasets, eval scripts, results
- `paper/` — manuscript draft + related work

## 📄 Paper

**Working title:** *Evaluating NLU Robustness on Code-Mixed Hindi-English 
Queries for Low-Resource Domain-Specific Chatbots*

Related work baseline: HingBERT, L3Cube-HingCorpus, Sanvaad-style 
code-mix benchmarks (domain-general) — this work targets retail/shop 
domain specifically.

## 📝 License

MIT
