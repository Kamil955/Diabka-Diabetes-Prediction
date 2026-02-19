# 🩺 Diabka - System Wspomagania Diagnostyki Cukrzycy Typu 2

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](TUTAJ_WKLEJ_LINK_DO_TWOJEJ_APLIKACJI_STREAMLIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

**Diabka** to interaktywna aplikacja webowa typu End-to-End stworzona w języku Python. Jej głównym celem jest oszacowanie ryzyka wystąpienia cukrzycy typu 2 z wykorzystaniem algorytmów uczenia maszynowego (Machine Learning). 

Projekt powstał z myślą o szerokim zastosowaniu, dlatego oferuje dwa niezależne modele predykcyjne:
1. 🩸 **Model Kliniczny** – wymaga wprowadzenia dokładnych danych medycznych i laboratoryjnych (np. poziom glukozy na czczo, ciśnienie krwi, tętno).
2. 📋 **Model Ankietowy (BRFSS)** – oparty wyłącznie na czynnikach behawioralnych i stylu życia (m.in. dieta, aktywność fizyczna, BMI, palenie tytoniu). Pozwala na szybki "screening" bez konieczności robienia badań krwi.

## 🚀 Live Demo
Aplikacja jest wdrożona w chmurze i dostępna pod adresem: 
👉 **https://diabka.streamlit.app/**

## 🛠️ Technologie i Biblioteki
* **Język:** Python
* **Machine Learning:** Scikit-learn, Joblib
* **Analiza Danych:** Pandas
* **Interfejs i Wdrożenie:** Streamlit
* **Wizualizacja:** Grafiki z oficjalnych raportów IDF (International Diabetes Federation)

## 📂 Struktura Projektu

W repozytorium znajdują się następujące pliki:
* `app_final_version.py` - Główny skrypt aplikacji Streamlit, zawierający logikę interfejsu i obsługę modeli.
* `medical_diabetes_model.pkl` - Wytrenowany model uczenia maszynowego (Kliniczny).
* `best_model_tuned.pkl` - Wytrenowany i zoptymalizowany model uczenia maszynowego (Ankietowy).
* `requirements.txt` - Lista zależności i bibliotek niezbędnych do uruchomienia projektu w środowisku Streamlit Cloud.
* `img/` - Folder zawierający grafiki wykorzystane w interfejsie użytkownika.

## 📊 Źródła Danych
Modele zostały wytrenowane na zaufanych zbiorach danych udostępnionych w serwisie Kaggle:
* **Zbiór Kliniczny:** [Kaggle Diabetes Health Indicators - Clinical](https://www.kaggle.com/datasets/mohankrishnathalla/diabetes-health-indicators-dataset)
* **Zbiór Ankietowy:** [Diabetes Health Indicators Dataset - BRFSS](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset)

## 💻 Jak uruchomić projekt lokalnie na swoim komputerze?

Jeśli chcesz pobrać ten projekt i uruchomić go na własnym komputerze, wykonaj poniższe kroki w terminalu:

1. **Sklonuj repozytorium:**
   ```bash
   git clone [https://github.com/Kamil955/Diabka-Diabetes-Prediction.git](https://github.com/Kamil955/Diabka-Diabetes-Prediction.git)
   cd Diabka-Diabetes-Prediction
   ```

2. **(Opcjonalnie) Stwórz wirtualne środowisko:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # MacOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Zainstaluj wymagane biblioteki:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Uruchom aplikację:**
   ```bash
   streamlit run app_final_version.py
   ```

## ⚠️ Zastrzeżenie
*Aplikacja ma charakter wyłącznie edukacyjny i demonstracyjny. Zastosowane modele sztucznej inteligencji służą do oszacowania prawdopodobieństwa ryzyka i **nie stanowią diagnozy medycznej**. Wszelkie niepokojące objawy należy konsultować z lekarzem specjalistą.*

---
**Autor:** Kamil Kozik  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/kamil-kozik-a1447a220/)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/Kamil955)
