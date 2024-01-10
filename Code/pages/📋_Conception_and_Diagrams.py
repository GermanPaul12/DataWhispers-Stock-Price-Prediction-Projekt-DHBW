import streamlit as st
import base64

st.set_page_config(page_title='Conception and Diagrams',page_icon='📜')

with st.container():
    st.title("Konzeptionelle Modelle und Zeichnungen", anchor='center')
    st.write("Um den Erstellungsprozess dieser Webapplikation genaustmöglich dokumentieren zu können, sind hier die verschiedenen benutzten Modelle zur Projektentwicklung angegeben, die im Folgendem spezifisch erklärt werden.")

with st.container():  
    st.image('WI-Modelle_Bilder_Zeichnungen/Ereignisliste_dark.png', caption='Ereignisliste')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/Ereignis-Reaktions-Modelle_dark.png', caption='Ereignis-Reaktions-Modelle')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/Kontextdiagramm_dark.png', caption='Kontextdiagramm')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/SWOT_dark.png', caption='SWOT-Analyse')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/Kombinierte_SWOT_Analyse_dark.png', caption='Kombinierte SWOT-Analyse')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/Aktivitätsdiagramm_dark.png', caption='Aktivitätsdiagramm')

def displayPDF(file, Titel=""):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf" title="alternativText"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
displayPDF("Presentations/Auswirkungen_Marketing_Branding_PDF.pdf", "Marketing_Branding")
displayPDF("Presentations/Kosten-Nutzen-Analyse.pdf","Kosten_nutzen_Analyse")
displayPDF("Presentations/Zielgruppenanalyse_Data_Whispers_PDF.pdf","Zielgruppenanalyse")