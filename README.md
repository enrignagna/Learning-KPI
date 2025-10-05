# KPI Learning App

Applicazione Streamlit per la raccolta e analisi di KPI di apprendimento.

## Funzionalità
- 4 form (Pre, Post, Follow-up, Manager) generati dinamicamente dal file Excel `Schema_KPI_Learning_Completo_ALL.xlsx`
- Salvataggio risposte in CSV (`risposte.csv`)
- Dashboard con calcolo base di Reaction, NPS e altri KPI

## Installazione locale
```bash
pip install -r requirements.txt
streamlit run app.py
```

Apri il browser su `http://localhost:8501`

## Deployment su Streamlit Cloud
1. Carica questi file su un repository GitHub:
   - `app.py`
   - `requirements.txt`
   - `Schema_KPI_Learning_Completo_ALL.xlsx`
2. Vai su [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Collega il tuo account GitHub e scegli il repository
4. Seleziona branch e file `app.py`
5. Ottieni il link pubblico alla tua applicazione
