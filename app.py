import streamlit as st

# Streamlit-Benutzeroberfläche
st.title("CV-Generator")

# Persönliche Informationen
st.header("Personal Information")
name = st.text_input("Name")
address = st.text_input("Adresse")
phone = st.text_input("Telefonnummer")
email = st.text_input("E-Mail")

# Education
st.header("Education")
university1 = st.text_input("Universität/Schule 1")
locationus1 = st.text_input("Standort 1")
majorus1 = st.text_input("Studiengang 1")
timeus1 = st.text_input("Zeitraum 1")
courses1 = st.text_input("Kurse 1")
gpa1 = st.text_input("GPA 1")
clubs1 = st.text_input("Clubs/Aktivitäten 1")

university2 = st.text_input("Universität/Schule 2", "")
locationus2 = st.text_input("Standort 2", "")
majorus2 = st.text_input("Studiengang 2", "")
timeus2 = st.text_input("Zeitraum 2", "")
courses2 = st.text_input("Kurse 2", "")
gpa2 = st.text_input("GPA 2", "")
clubs2 = st.text_input("Clubs/Aktivitäten 2", "")

# Professional Experience
st.header("Professional Experience")
experience1 = st.text_input("Erfahrung 1")
locatione1 = st.text_input("Standort Erfahrung 1")
position1 = st.text_input("Position 1")
timee1 = st.text_input("Zeitraum Erfahrung 1")
task11 = st.text_area("Aufgaben 1", key='task11', height=100)
task12 = st.text_area("Aufgaben 2", key='task12', height=100)
task13 = st.text_area("Aufgaben 3", key='task13', height=100)

experience2 = st.text_input("Erfahrung 2", "")
locatione2 = st.text_input("Standort Erfahrung 2", "")
position2 = st.text_input("Position 2", "")
timee2 = st.text_input("Zeitraum Erfahrung 2", "")
task21 = st.text_area("Aufgaben 1", key='task21', height=100)
task22 = st.text_area("Aufgaben 2", key='task22', height=100)
task23 = st.text_area("Aufgaben 3", key='task23', height=100)

experience3 = st.text_input("Erfahrung 3", "")
locatione3 = st.text_input("Standort Erfahrung 3", "")
position3 = st.text_input("Position 3", "")
timee3 = st.text_input("Zeitraum Erfahrung 3", "")
task31 = st.text_area("Aufgaben 1", key='task31', height=100)
task32 = st.text_area("Aufgaben 2", key='task32', height=100)
task33 = st.text_area("Aufgaben 3", key='task33', height=100)

# Extracurricular Activities / Engagement
st.header("Extracurricular Activities / Engagement")
extracurricular1 = st.text_input("Extrakurrikulare Aktivitäten")
additionaleducation1 = st.text_input("Zusätzliche Bildung")
certificates1 = st.text_input("Zertifikate und Errungenschaften")

# Skills & Interest
st.header("Skills & Interest")
languages1 = st.text_input("Sprachen")
computer1 = st.text_input("Computerkenntnisse")
interests1 = st.text_input("Interessen")

# Button zum Erstellen des CVs
if st.button("CV Erstellen"):
    try:
        with open('template_finance.tex', 'r', encoding='utf-8') as file:
            latex_template = file.read()

        try:
            # Formatierung des LaTeX-Templates
            latex_filled = latex_template.format(
                name=name,
                address=address,
                phone=phone,
                email=email,
                university1=university1, 
                locationus1=locationus1, 
                majorus1=majorus1, 
                timeus1=timeus1,
                courses1=courses1, 
                gpa1=gpa1, 
                clubs1=clubs1,
                university2=university2, 
                locationus2=locationus2, 
                majorus2=majorus2, 
                timeus2=timeus2, 
                courses2=courses2, 
                gpa2=gpa2, 
                clubs2=clubs2, 
                experience1=experience1, 
                locatione1=locatione1, 
                position1=position1, 
                timee1=timee1, 
                task11=task11, 
                task12=task12, 
                task13=task13, 
                experience2=experience2, 
                locatione2=locatione2, 
                position2=position2, 
                timee2=timee2, 
                task21=task21, 
                task22=task22, 
                task23=task23, 
                experience3=experience3,
                locatione3=locatione3, 
                position3=position3, 
                timee3=timee3, 
                task31=task31, 
                task32=task32, 
                task33=task33, 
                extracurricular1=extracurricular1, 
                additionaleducation1=additionaleducation1, 
                certificates1=certificates1, 
                languages1=languages1,
                computer1=computer1, 
                interests1=interests1
            )

            # Anzeigen des gefüllten LaTeX-Codes auf der Streamlit-Oberfläche
            st.text_area("Gefüllter LaTeX-Code", latex_filled, height=300)

        except KeyError as key_err:
            st.error(f"Fehler bei der Formatierung: Unbekannter Platzhalter {key_err}")
        except Exception as format_err:
            st.error(f"Fehler bei der Formatierung: {format_err}")

    except FileNotFoundError:
        st.error("Die LaTeX-Vorlagendatei wurde nicht gefunden.")
    except Exception as e:
        st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
