import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="KPI Learning", layout="wide")

EXCEL_FILE = "Schema_KPI_Learning_Completo_ALL.xlsx"
RESPONSES_FILE = "risposte.csv"

df_questions = pd.read_excel(EXCEL_FILE, sheet_name="Domande")

if "responses" not in st.session_state:
    if os.path.exists(RESPONSES_FILE):
        st.session_state["responses"] = pd.read_csv(RESPONSES_FILE).to_dict("records")
    else:
        st.session_state["responses"] = []

forms = df_questions["Form"].unique().tolist()

def save_response(form_name, data):
    row = {"Form": form_name}
    row.update(data)
    st.session_state["responses"].append(row)
    pd.DataFrame(st.session_state["responses"]).to_csv(RESPONSES_FILE, index=False)
    st.success("Risposte salvate!")

def show_form(form_name):
    st.header(form_name)
    df_form = df_questions[df_questions["Form"] == form_name]

    with st.form(f"form_{form_name}"):
        data = {}
        for section in df_form["Section"].unique():
            st.subheader(section)
            section_df = df_form[df_form["Section"] == section]
            for _, row in section_df.iterrows():
                domanda = row["Domanda"]
                qtype = row["Tipo Risposta"]
                scale = str(row["Scala/Punteggio"])

                if "Scala lineare" in qtype:
                    try:
                        low, high = [int(x) for x in scale.replace("–","-").split("-")]
                    except:
                        low, high = 1, 5
                    data[domanda] = st.slider(domanda, low, high)
                elif "Risposta breve numerica" in qtype:
                    data[domanda] = st.number_input(domanda, step=1)
                elif "Risposta breve" in qtype:
                    data[domanda] = st.text_input(domanda)
                elif "Scelta multipla" in qtype:
                    options = scale.split("/") if "/" in scale else ["Sì","No"]
                    data[domanda] = st.selectbox(domanda, options)
                elif "Data" in qtype:
                    data[domanda] = st.date_input(domanda)
                else:
                    data[domanda] = st.text_area(domanda)
        submitted = st.form_submit_button("Invia")
        if submitted:
            save_response(form_name, data)

def show_dashboard():
    st.title("Dashboard KPI Learning")
    if len(st.session_state["responses"]) == 0:
        st.warning("Nessun dato disponibile ancora.")
        return

    df = pd.DataFrame(st.session_state["responses"])
    st.subheader("Dati grezzi")
    st.dataframe(df)

    st.subheader("Analisi sintetica")
    if "Soddisfazione complessiva" in df.columns:
        st.metric("Reaction (media)", round(df["Soddisfazione complessiva"].mean(),2))

    if "NPS" in df.columns:
        promoters = (df["NPS"] >= 9).sum()
        detractors = (df["NPS"] <= 6).sum()
        total = len(df["NPS"])
        if total > 0:
            nps_score = ((promoters - detractors) / total) * 100
            st.metric("NPS", f"{nps_score:.1f}")

st.sidebar.title("Menu")
choice = st.sidebar.radio("Naviga:", ["Home"] + list(forms) + ["Dashboard"])

if choice == "Home":
    st.title("📊 KPI Learning App")
    st.write("Scegli un form dal menu a sinistra per iniziare la compilazione, oppure vai alla Dashboard per analizzare i risultati.")
elif choice in forms:
    show_form(choice)
elif choice == "Dashboard":
    show_dashboard()
