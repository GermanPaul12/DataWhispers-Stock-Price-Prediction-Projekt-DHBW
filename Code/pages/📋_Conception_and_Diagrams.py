import streamlit as st

with st.container():
    st.title("Konzeptionelle Modelle und Zeichnungen", anchor='center')
    st.write("Um den Erstellungsprozess dieser Webapplikation genausmöglich dokumentieren zu können, sind hier die verscheidnen benutzten Modelle zu Projektentwicklung angegeben, die im folgenden spezifisch erklährt werden.")

with st.container():  
    st.image('WI-Modelle_Bilder_Zeichnungen/Ereignisliste_dark.png', caption='Ereignisliste')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/Ereignis-Reaktions-Modelle-dark.png', caption='Ereignis-Reaktions-Modelle')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/Kontextdiagramm_dark.png', caption='Kontextdiagramm')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/SWOT_dark.png', caption='SWOT-Analyse')
    st.write("\n")
    st.image('WI-Modelle_Bilder_Zeichnungen/Kombinierte_SWOT_Analyse_dark.png', caption='Kombinierte SWOT-Analyse')