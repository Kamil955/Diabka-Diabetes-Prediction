import streamlit as st
import pandas as pd
import joblib
import os
from pathlib import Path



# =========================================================
# 1. KONFIGURACJA STRONY I STAN APLIKACJI
# =========================================================
st.set_page_config(
    page_title="Diabka - System AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicjalizacja stanu (nawigacja)
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_model_type' not in st.session_state:
    st.session_state.selected_model_type = None

# =========================================================
# 2. FUNKCJE POMOCNICZE
# =========================================================
def age_to_brfss_category(age_years: int) -> int:
    if age_years <= 24: return 1
    if age_years <= 29: return 2
    if age_years <= 34: return 3
    if age_years <= 39: return 4
    if age_years <= 44: return 5
    if age_years <= 49: return 6
    if age_years <= 54: return 7
    if age_years <= 59: return 8
    if age_years <= 64: return 9
    if age_years <= 69: return 10
    if age_years <= 74: return 11
    if age_years <= 79: return 12
    return 13

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0: return 0.0
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 1)

# Funkcja do bezpiecznego wyświetlania zdjęć
def show_image(path, caption, width = None):
    if os.path.exists(path):
        if width:
            # Jeśli podano szerokość, używamy jej (w pikselach)
            st.image(path, caption=caption, width=width)
        else:
            # W przeciwnym razie dopasuj do szerokości kontenera (domyślnie)
            st.image(path, caption=caption, use_container_width=True)
    else:
        st.warning(f"⚠️ Brak pliku: {path}. Sprawdź folder 'img'.")

# =========================================================
# 3. ŁADOWANIE MODELI
# =========================================================
HERE = Path(__file__).resolve().parent  # github-app/

@st.cache_resource
def load_models():
    models = {}

    # 1. Model kliniczny
    path_clinical = HERE / "medical_diabetes_model.pkl"
    if path_clinical.exists():
        models["clinical"] = joblib.load(path_clinical)
    else:
        st.error(f"❌ Nie znaleziono modelu: {path_clinical}")

    # 2. Model ankietowy (BRFSS)
    path_brfss = HERE / "best_model_tuned.pkl"
    if path_brfss.exists():
        models["brfss"] = joblib.load(path_brfss)
    else:
        st.error(f"❌ Nie znaleziono modelu: {path_brfss}")

    return models

loaded_models_data = load_models()

# =========================================================
# 4. PASEK BOCZNY (SIDEBAR)
# =========================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3004/3004458.png", width=100)
    st.title("Diabka")
    st.markdown("System wspomagania diagnostyki cukrzycy typu 2.")
    
    st.markdown("---")
    st.subheader("Nawigacja")
    
    if st.button("🏠 Start / Wybór Modelu", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.selected_model_type = None
        st.rerun()

    st.markdown("### 📚 Baza Wiedzy")
    
    if st.button("📊 Zbiory Danych", use_container_width=True):
        st.session_state.page = "dane"
        st.rerun()
        
    if st.button("📈 Statystyki Cukrzycy", use_container_width=True):
        st.session_state.page = "statystyki"
        st.rerun()
        
    if st.button("🛡️ Prewencja i objawy", use_container_width=True):
        st.session_state.page = "prewencja"
        st.rerun()
        
    if st.button("🧪 Zalecane Badania", use_container_width=True):
        st.session_state.page = "badania"
        st.rerun()
  

# =========================================================
# 5. LOGIKA STRON
# =========================================================

# --- STRONA: DANE ---
if st.session_state.page == "dane":
    st.title("📊 Zbiory danych")
    st.markdown("""
    Aplikacja opiera się na dwóch głównych zbiorach danych, na których modele były trenowane:
    
    1. **Zbiór Kliniczny (Laboratoryjny)** 👉 [Kaggle Diabetes Health Indicators](https://www.kaggle.com/datasets/mohankrishnathalla/diabetes-health-indicators-dataset)
       
    2. **Zbiór Ankietowy** 👉 [Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset)
    """)

# --- STRONA: STATYSTYKI ---
elif st.session_state.page == "statystyki":
    st.title("📈 Statystyki")
    
    # LINK DO RAPORTU
    st.markdown("""
    Poniższe mapy i wykresy pochodzą z najnowszego raportu:  
    👉 **[IDF Diabetes Atlas 10th Edition (2025 Update)](https://diabetesatlas.org/resources/idf-diabetes-atlas-2025/)**
    """)
    
    # Kluczowe liczby
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Chorzy na świecie", "589 mln", delta="Wzrost r/r", delta_color="inverse")
    with col2:
        st.metric("Prognoza 2050", "852 mln", "Alarmujący trend", delta_color='inverse')
    with col3:
        st.metric("Niezdiagnozowani", "~43%", "Nie wiedzą o chorobie", delta_arrow='off', delta_color='inverse')
    st.divider()

    # 1. PODSUMOWANIE I MAPA
    st.subheader("1. Skala globalna i liczby chorych")
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        show_image("img/stats_diabetes_map.png", "Mapa 1: Liczba osób z cukrzycą na świecie")
    with col_img2:
        show_image("img/stats_estimated_with_diabetes.png", "Mapa 3.1: Szacowana liczba dorosłych (20-79 lat) z cukrzycą wg krajów")

    st.divider()

    # 2. TRENDY
    st.subheader("2. Trendy i Prognozy")
    show_image("img/stats_estimates_global_prevalence.png", "Ryc 1: Szacunki i prognozy globalnego rozpowszechnienia cukrzycy (2000–2050).")
        
    st.divider()
    
    # 3. UKRYTA CHOROBA I ZGONY
    st.subheader("3. Niezdiagnozowana cukrzyca i śmiertelność")
    col_img3, col_img4 = st.columns(2)
    with col_img3:
        show_image("img/stats_proportion_undiagnosed.png", "Mapa 3.4: Odsetek dorosłych z niezdiagnozowaną cukrzycą (ciemny kolor = wysoki odsetek).")
    with col_img4:
        show_image("img/stats_proportion_total_deaths.png", "Mapa 3.7: Odsetek zgonów powiązanych z cukrzycą wśród dorosłych.")


# --- STRONA: PREWENCJA I OBJAWY ---
elif st.session_state.page == "prewencja":
    st.title("🛡️ Prewencja i Objawy Cukrzycy")
    
    # Zakładki
    tab_objawy, tab_prewencja = st.tabs(["⚠️ Objawy i Powikłania", "🛡️ Jak zapobiegać?"])

    # --- ZAKŁADKA 1: OBJAWY ---
    with tab_objawy:
        st.header("Jak rozpoznać cukrzycę?")
        st.markdown("""
        Objawy cukrzycy mogą pojawić się nagle. Jednak w przypadku **cukrzycy typu 2** objawy mogą być łagodne i **rozwijać się przez wiele lat**, zanim zostaną zauważone.
        """)
        
        st.subheader("Główne objawy alarmowe:")
        
        col_sym1, col_sym2 = st.columns(2)
        with col_sym1:
            st.info("💧 **Wzmożone pragnienie** (uczucie silnego pragnienia)")
            st.info("🚻 **Częste oddawanie moczu** (częściej niż zwykle)")
            st.info("👁️ **Niewyraźne widzenie** (rozmazany obraz)")
        with col_sym2:
            st.info("🔋 **Uczucie zmęczenia** (przewlekłe osłabienie)")
            st.info("⚖️ **Niezamierzona utrata wagi** (chudnięcie bez diety)")

        st.divider()
        
        st.subheader("Poważne powikłania (gdy cukrzyca nie jest leczona)")
        st.warning("Z czasem cukrzyca może uszkodzić naczynia krwionośne w sercu, oczach, nerkach i nerwach.")
        
        c_com1, c_com2, c_com3, c_com4 = st.columns(4)
        with c_com1:
            st.markdown("#### ❤️ Serce")
            st.caption("Wyższe ryzyko zawału serca i udaru mózgu.")
        with c_com2:
            st.markdown("#### 👁️ Oczy")
            st.caption("Uszkodzenie naczyń w oczach może prowadzić do trwałej utraty wzroku.")
        with c_com3:
            st.markdown("#### 🦶 Stopy")
            st.caption("Słaby przepływ krwi i uszkodzenie nerwów mogą powodować owrzodzenia, a nawet amputację.")
        with c_com4:
            st.markdown("#### 🚽 Nerki")
            st.caption("Ryzyko niewydolności nerek.")
        
        # Źródło
        with st.expander("📚 Źródło danych (WHO)"):
            st.markdown("""
            **World Health Organization (WHO) - Diabetes Fact Sheet** *Dostęp:* https://www.who.int/news-room/fact-sheets/detail/diabetes
            """)

    # --- ZAKŁADKA 2: PREWENCJA ---
    with tab_prewencja:
        st.header("Styl życia to najlepsza ochrona")
        st.markdown("""
        Zmiany w stylu życia są najskuteczniejszym sposobem na **zapobieganie lub opóźnienie** wystąpienia cukrzycy typu 2. 
        WHO zaleca skupienie się na 4 głównych obszarach:
        """)
        
        st.divider()
        # Układ kafelkowy 2x2
        col_p1, col_p2 = st.columns(2)

        with col_p1:
            with st.container(border=True):
                st.markdown("### 🍏 1. Zdrowa Waga")
                st.write("Osiągnij i utrzymaj zdrową masę ciała. Redukcja wagi, nawet niewielka, drastycznie zmniejsza ryzyko.")
            
            with st.container(border=True):
                st.markdown("### 🥗 3. Zdrowa Dieta")
                st.write("Jedz zdrowo. Unikaj cukru i tłuszczów nasyconych. Zwiększ spożycie błonnika, owoców i warzyw.")

        with col_p2:
            with st.container(border=True):
                st.markdown("### 🏃‍♂️ 2. Aktywność Fizyczna")
                st.write("Bądź aktywny fizycznie. WHO zaleca co najmniej **150 minut** umiarkowanych ćwiczeń tygodniowo (np. szybki spacer).")
            
            with st.container(border=True):
                st.markdown("### 🚬 4. Unikanie Tytoniu")
                st.write("Nie pal tytoniu. Palenie zwiększa ryzyko cukrzycy typu 2 oraz znacznie przyspiesza rozwój powikłań sercowych.")

        st.divider()
        
        # Źródło
        with st.expander("📚 Źródło danych (WHO)"):
            st.markdown("""
            **World Health Organization (WHO) - Diabetes Fact Sheet** *Dostęp:* https://www.who.int/news-room/fact-sheets/detail/diabetes
            """)



# --- STRONA: BADANIA  ---
elif st.session_state.page == "badania":
    st.title("🧪 Diagnostyka Cukrzycy")
    
    # st.markdown("""
    # Aby potwierdzić lub wykluczyć cukrzycę, lekarze stosują ściśle określone kryteria. 
    # Poniższa grafika przedstawia oficjalne wytyczne diagnostyczne (IDF/WHO).
    # """)

    # # Wyświetlenie schematu diagnostycznego
    # show_image("img/diagnostyka.png", "Ryc. 1.1 Kryteria diagnostyczne cukrzycy (Źródło: IDF Diabetes Atlas).", width=600)

    st.divider()

    st.header("Jakie badania wykonać, aby mieć pewność?")
    st.markdown("Zgodnie z zaleceniami IDF cukrzycę rozpoznaje się, jeśli spełnione jest **JEDNO lub WIĘCEJ** z poniższych kryteriów:")

    # Lista badań z opisem na podstawie grafiki
    st.info("""
    ### 1. Glukoza na czczo
    * **Kryterium:** Wynik **≥ 126 mg/dL** (7.0 mmol/L).
    * **Jak wykonać:** Krew pobierana jest rano, po minimum 8 godzinach bez jedzenia i picia słodkich napojów.
    """)

    st.info("""
    ### 2. Test obciążenia glukozą (OGTT)
    * **Kryterium:** Wynik **≥ 200 mg/dL** (11.1 mmol/L) po 2 godzinach.
    * **Jak wykonać:** Pacjent wypija roztwór 75g glukozy. Pomiar następuje przed wypiciem i 2 godziny po. To „złoty standard” w wykrywaniu cukrzycy utajonej.
    """)

    st.info("""
    ### 3. Hemoglobina glikowana (HbA1c)
    * **Kryterium:** Wynik **≥ 6.5%** (48 mmol/mol).
    * **Jak wykonać:** Badanie krwi, które nie wymaga bycia na czczo. 
    """)

    st.warning("""
    ### 4. Glikemia przygodna (Random Plasma Glucose)
    * **Kryterium:** Wynik **≥ 200 mg/dL** (11.1 mmol/L) **ORAZ** występowanie objawów.
    * **Objawy:** Wzmożone pragnienie, częste oddawanie moczu, nagła utrata wagi.
    * **Jak wykonać:** Pomiar o dowolnej porze dnia, niezależnie od posiłku.
    """)

    st.markdown("---")
    st.caption("Pamiętaj: Jeśli nie masz wyraźnych objawów hiperglikemii, wynik zazwyczaj musi zostać potwierdzony powtórnym badaniem w innym dniu.")

# --- STRONA GŁÓWNA ---
elif st.session_state.page == "home":
    
    if st.session_state.selected_model_type is None:
        st.title("Witaj w Diabka 👋")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown("### 🩸 Mam wyniki badań")
                if st.button("Model Kliniczny", type="primary", use_container_width=True):
                    st.session_state.selected_model_type = "clinical"
                    st.rerun()
        with col2:
            with st.container(border=True):
                st.markdown("### 📋 Tylko ankieta")
                if st.button("Model Ankietowy", type="secondary", use_container_width=True):
                    st.session_state.selected_model_type = "brfss"
                    st.rerun()
    else:
        model_key = st.session_state.selected_model_type
        if model_key not in loaded_models_data:
            st.error("Błąd ładowania modelu.")
            if st.button("Wróć"): st.rerun()
            st.stop()
            
        current_pkg = loaded_models_data[model_key]
        model = current_pkg["model"]
        scaler = current_pkg.get("scaler", None)
        features = current_pkg.get("features", current_pkg.get("feature_names", None))
        threshold = current_pkg.get("threshold", 0.5)
        is_brfss = (model_key == "brfss")
        
        st.title(f"Diagnostyka: {'Model Ankietowy' if is_brfss else 'Model Kliniczny'}")
        if st.button("⬅️ Zmień model"):
            st.session_state.selected_model_type = None
            st.rerun()
        st.divider()

        submit_btn = False
        
        if is_brfss:
            with st.form("brfss_form"):
                st.info("ℹ️ Model oparty na stylu życia. Wypełnij pola zgodnie z prawdą.")
                
                # SEKCJA 1
                c1, c2, c3 = st.columns(3)
                with c1:
                    age = st.number_input("Wiek (lata)", 18, 120, 30)
                    gender = st.selectbox("Płeć", ["Kobieta", "Mężczyzna"])
                with c2:
                    education = st.selectbox("Wykształcenie", [
                        "Podstawowe / brak", "Zasadnicze zawodowe", "Średnie", 
                        "Policealne", "Wyższe (licencjat)", "Wyższe (mgr)", "Doktorat"
                    ], help="Najwyższy ukończony poziom edukacji.")
                with c3:
                    income = st.selectbox("Dochód", [
                        "Bardzo niski", "Niski", "Niższy-średni", "Średni", 
                        "Wyższy-średni", "Wysoki", "Bardzo wysoki"
                    ])

                # SEKCJA 2
                st.markdown("#### Zdrowie i Styl Życia")
                c4, c5, c6 = st.columns(3)
                with c4:
                    weight = st.number_input("Waga (kg)", 30.0, 250.0, 75.0, step=0.5, format="%.1f")
                    height = st.number_input("Wzrost (cm)", 120.0, 220.0, 175.0, step=1.0, format="%.0f")
                    bmi = calculate_bmi(weight, height)
                    st.metric("BMI", bmi, help="Wskaźnik masy ciała (BMI). Norma: 18.5 - 24.9")
                    
                    genhlth_label = st.select_slider(
                        "Jak oceniasz swoje zdrowie?", 
                        options=["Zły", "Średni", "Dobry", "Bardzo dobry", "Doskonały"],
                        value="Dobry",
                        help="Subiektywna ocena ogólnego stanu zdrowia."
                    )
                    
                with c5:
                    highbp = st.radio("Nadciśnienie", ["Nie", "Tak"], horizontal=True, 
                                      help="Czy lekarz kiedykolwiek stwierdził u Ciebie wysokie ciśnienie krwi?")
                    highchol = st.radio("Wysoki cholesterol", ["Nie", "Tak"], horizontal=True,
                                        help="Czy lekarz kiedykolwiek stwierdził u Ciebie podwyższony poziom cholesterolu?")
                    cholcheck = st.radio("Badanie cholesterolu", ["Nie", "Tak"], horizontal=True,
                                         help="Czy w ciągu ostatnich 5 lat miałeś/aś badany poziom cholesterolu?")
                with c6:
                    stroke = st.radio("Przebyty udar", ["Nie", "Tak"], horizontal=True, help="Czy kiedykolwiek zdiagnozowano u Ciebie udar mózgu?")
                    heart = st.radio("Choroba wieńcowa", ["Nie", "Tak"], horizontal=True, help="Czy masz zdiagnozowaną chorobę niedokrwienną serca lub przeszedłeś zawał?")
                    diffwalk = st.radio("Trudności w chodzeniu", ["Nie", "Tak"], horizontal=True, help="Czy masz trudności z wchodzeniem po schodach?")

                # SEKCJA 3
                st.markdown("#### Używki i Aktywność")
                c7, c8, c9 = st.columns(3)
                with c7:
                    smoker = st.radio("Palacz", ["Nie", "Tak"], horizontal=True, 
                                      help="Definicja: Czy wypaliłeś/aś w swoim życiu łącznie przynajmniej 100 papierosów (5 paczek)?")
                    physact = st.radio("Aktywność fizyczna", ["Nie", "Tak"], horizontal=True,
                                       help="Czy w ciągu ostatnich 30 dni uprawiałeś/aś sport?")
                with c8:
                    fruits = st.radio("Owoce (codziennie)", ["Nie", "Tak"], horizontal=True, help="Czy spożywasz owoce lub pijesz sok 100% przynajmniej raz dziennie?")
                    veggies = st.radio("Warzywa (codziennie)", ["Nie", "Tak"], horizontal=True, help="Czy spożywasz warzywa przynajmniej raz dziennie?")
                with c9:
                    hvyalc = st.radio("Dużo alkoholu", ["Nie", "Tak"], horizontal=True,
                                        help=(
                                            "Mężczyźni: >28 porcji standardowych (SJA)/tydzień. "
                                            "Kobiety: >14 porcji standardowych (SJA)/tydzień. "
                                            "1 porcja (SJA) = 10 g etanolu ≈ 250 ml piwa 5%, "
                                            "100 ml wina 12% lub 30 ml wódki 40%."
                                     ))
                    anyhc = st.radio("Ubezpieczenie", ["Nie", "Tak"], horizontal=True, help="Czy posiadasz jakiekolwiek ubezpieczenie zdrowotne?")
                    nodoc = st.radio("Brak lekarza (koszty)", ["Nie", "Tak"], horizontal=True, help="Czy w ciągu ostatnich 12 msc zrezygnowałeś z wizyty u lekarza z powodu braku pieniędzy?")

                st.markdown("---")
                c10, c11 = st.columns(2)
                with c10: 
                    ment = st.slider("Złe zdrowie psychiczne (dni/msc)", 0, 30, 0, 
                                     help="Ile dni w ciągu ostatnich 30 dni Twój stan psychiczny był zły (stres, depresja, emocje)?")
                with c11: 
                    phys = st.slider("Złe zdrowie fizyczne (dni/msc)", 0, 30, 0, 
                                     help="Ile dni w ciągu ostatnich 30 dni Twój stan fizyczny był zły (choroba, kontuzja)?")

                submit_btn = st.form_submit_button("PRZELICZ RYZYKO", type="primary")

        else:
            # Formularz Kliniczny
            with st.form("medical_form"):
                st.info("ℹ️ Model kliniczny. Wymaga dokładnych danych medycznych.")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    age = st.number_input("Wiek", 18, 120, 30)
                    gender = st.selectbox("Płeć", ["Kobieta", "Mężczyzna", "Inna"])
                with c2:
                    ethnicity = st.selectbox("Etniczność", ["Biała", "Afroamerykańska", "Latynoska", "Inna"], 
                                            )
                    education = st.selectbox("Wykształcenie", ["Podstawowe", "Średnie", "Licencjat", "Magister", "Doktorat"])
                with c3:
                    income = st.selectbox("Dochód", ["Niski", "Średni", "Wysoki"])
                    employment = st.selectbox("Status", ["Zatrudniony", "Bezrobotny", "Student", "Emeryt"])

                st.markdown("#### Pomiary")
                c4, c5, c6 = st.columns(3)
                with c4:
                    weight = st.number_input("Waga (kg)", 0.0, 250.0, 75.0, step=0.5, format="%.1f")
                    height = st.number_input("Wzrost (cm)", 0.0, 220.0, 175.0, step=1.0, format="%.0f")
                    bmi = calculate_bmi(weight, height)
                    st.metric("BMI", bmi, help="Body Mass Index")
                    whr = st.number_input("WHR", 0.0, 2.5, 0.85, step=0.01, 
                                          help="Waist-to-Hip Ratio: Podziel obwód talii (cm) przez obwód bioder (cm).")
                with c5:
                    sys_bp = st.number_input("Ciśnienie skurczowe", 0, 250, 120, help="Górna wartość ciśnienia krwi (mm Hg).")
                    dia_bp = st.number_input("Ciśnienie rozkurczowe", 0, 160, 80, help="Dolna wartość ciśnienia krwi (mm Hg).")
                with c6:
                    heart_rate = st.number_input("Tętno", 0, 220, 70, help="Tętno spoczynkowe (uderzenia na minutę).")

                st.markdown("#### Styl Życia")
                c7, c8, c9 = st.columns(3)
                with c7:
                    activity = st.number_input("Aktywność (min/tydz)", 0, 1000, 150, help="Suma minut umiarkowanej aktywności fizycznej w tygodniu.")
                    sleep = st.number_input("Sen (h)", 0.0, 16.0, 7.0, step=0.5, help="Średnia liczba godzin snu na dobę.")
                with c8:
                    diet = st.slider("Dieta (0-10)", 0, 10, 5, help="Subiektywna ocena jakości diety (0=Bardzo niezdrowa, 10=Bardzo zdrowa).")
                    alcohol = st.number_input("Alkohol (jedn/tydz)", 0, 100, 0, help=(
                                            "Mężczyźni: >28 porcji standardowych (SJA)/tydzień. "
                                            "Kobiety: >14 porcji standardowych (SJA)/tydzień. "
                                            "1 porcja (SJA) = 10 g etanolu ≈ 250 ml piwa 5%, "
                                            "100 ml wina 12% lub 30 ml wódki 40%."
                                            ))
                with c9:
                    screen = st.number_input("Ekran (h/dobę)", 0.0, 24.0, 2.0, step=0.5, help="Czas spędzany przed telewizorem/komputerem (poza pracą).")
                    smoking = st.selectbox("Palacz", ["Nigdy", "Były palacz", "Obecnie"], help="Status palenia tytoniu.")

                st.markdown("#### Badania")
                c10, c11 = st.columns([1, 2])
                with c10:
                    fam_hist = st.radio("Cukrzyca w rodzinie", ["Nie", "Tak"], help="Czy rodzice lub rodzeństwo chorują na cukrzycę?")
                    hyper_hist = st.radio("Leczenie Nadciśnienia", ["Nie", "Tak"], help="Czy przyjmujesz leki na nadciśnienie?")
                    cardio_hist = st.radio("Choroby Serca", ["Nie", "Tak"], help="Zdiagnozowane choroby układu krążenia.")
                with c11:
                    st.markdown("##### 🩸 Glukoza na czczo")
                    glucose = st.number_input("Wynik (mg/dL)", 0, 600, 0, help="Poziom glukozy we krwi na czczo (minimum 8h bez jedzenia).")

                submit_btn = st.form_submit_button("PRZELICZ RYZYKO", type="primary")

        if submit_btn:
            try:
                input_data = {f: 0 for f in features}
                
                if is_brfss:
                    gen_map_ui = {
                        "Doskonały": 1, "Bardzo dobry": 2, "Dobry": 3, "Średni": 4, "Zły": 5
                    }
                    
                    # Mapowania
                    edu_map = {"Podstawowe / brak": 2, "Zasadnicze zawodowe": 3, "Średnie": 4, 
                               "Policealne": 5, "Wyższe (licencjat)": 5, "Wyższe (mgr)": 6, "Doktorat": 6}
                    inc_map = {"Bardzo niski": 1, "Niski": 2, "Niższy-średni": 4, "Średni": 5, 
                               "Wyższy-średni": 6, "Wysoki": 7, "Bardzo wysoki": 8}

                    input_data["GenHlth"] = gen_map_ui[genhlth_label]
                    input_data["HighBP"] = 1 if highbp == "Tak" else 0
                    input_data["HighChol"] = 1 if highchol == "Tak" else 0
                    input_data["CholCheck"] = 1 if cholcheck == "Tak" else 0
                    input_data["BMI"] = float(bmi)
                    input_data["Smoker"] = 1 if smoker == "Tak" else 0
                    input_data["Stroke"] = 1 if stroke == "Tak" else 0
                    input_data["HeartDiseaseorAttack"] = 1 if heart == "Tak" else 0
                    input_data["PhysActivity"] = 1 if physact == "Tak" else 0
                    input_data["Fruits"] = 1 if fruits == "Tak" else 0
                    input_data["Veggies"] = 1 if veggies == "Tak" else 0
                    input_data["HvyAlcoholConsump"] = 1 if hvyalc == "Tak" else 0
                    input_data["AnyHealthcare"] = 1 if anyhc == "Tak" else 0
                    input_data["NoDocbcCost"] = 1 if nodoc == "Tak" else 0
                    input_data["MentHlth"] = float(ment)
                    input_data["PhysHlth"] = float(phys)
                    input_data["DiffWalk"] = 1 if diffwalk == "Tak" else 0
                    input_data["Sex"] = 1 if gender == "Mężczyzna" else 0
                    input_data["Age"] = age_to_brfss_category(int(age))
                    
                    input_data["Education"] = 4 
                    input_data["Income"] = 5
                    if education in edu_map: input_data["Education"] = edu_map[education]
                    if income in inc_map: input_data["Income"] = inc_map[income]

                else:
                    if glucose == 0:
                        st.error("Podaj glukozę!")
                        st.stop()
                    
                    input_data['age'] = age
                    input_data['bmi'] = bmi
                    input_data['waist_to_hip_ratio'] = whr
                    input_data['systolic_bp'] = sys_bp
                    input_data['diastolic_bp'] = dia_bp
                    input_data['heart_rate'] = heart_rate
                    input_data['physical_activity_minutes_per_week'] = activity
                    input_data['alcohol_consumption_per_week'] = alcohol
                    input_data['diet_score'] = diet
                    input_data['sleep_hours_per_day'] = sleep
                    input_data['screen_time_hours_per_day'] = screen
                    input_data['glucose_fasting'] = glucose
                    input_data['family_history_diabetes'] = 1 if fam_hist == "Tak" else 0
                    input_data['hypertension_history'] = 1 if hyper_hist == "Tak" else 0
                    input_data['cardiovascular_history'] = 1 if cardio_hist == "Tak" else 0
                    
                    if gender == "Mężczyzna": input_data['gender_Male'] = 1
                    if ethnicity == "Afroamerykańska": input_data['ethnicity_Black'] = 1
                    if ethnicity == "Latynoska": input_data['ethnicity_Hispanic'] = 1
                    if ethnicity == "Biała": input_data['ethnicity_White'] = 1
                    if ethnicity == "Inna": input_data['ethnicity_Other'] = 1
                    if employment == "Bezrobotny": input_data['employment_status_Unemployed'] = 1
                    if employment == "Student": input_data['employment_status_Student'] = 1
                    if employment == "Emeryt": input_data['employment_status_Retired'] = 1
                    
                    edu_k_map = {"Podstawowe": 0, "Średnie": 1, "Licencjat": 2, "Magister": 3, "Doktorat": 4}
                    inc_k_map = {"Niski": 0, "Średni": 2, "Wysoki": 4}
                    smoke_k_map = {"Nigdy": 0, "Były palacz": 1, "Obecnie": 2}
                    
                    # Poprawione mapowanie dla formularza klinicznego
                    input_data['education_level_encoded'] = edu_k_map.get(education, 1)
                    input_data['income_level_encoded'] = inc_k_map.get(income, 2)
                    input_data['smoking_status_encoded'] = smoke_k_map.get(smoking, 0)

                # Predykcja
                df_input = pd.DataFrame([input_data])
                df_input = df_input[features].astype(float)
                
                if scaler: X_final = scaler.transform(df_input)
                else: X_final = df_input
                
                prob = model.predict_proba(X_final)[0, 1]
                prob_pct = prob * 100
                
                color = "red" if prob >= threshold else "green"
                label = "WYSOKIE RYZYKO" if prob >= threshold else "NISKIE RYZYKO"
                
                st.divider()
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"<h1 style='text-align: center; color: {color}'>{prob_pct:.1f}%</h1>", unsafe_allow_html=True)
                with c2:
                    st.subheader(label)
                    st.progress(int(min(prob_pct, 100)))
                    if prob >= threshold: st.warning("Zalecana konsultacja lekarska. Twój wynik przekracza próg dla grupy ryzyka.")
                    else: st.success("Ryzyko niskie. Pamiętaj o regularnej profilaktyce.")
                st.markdown("---")
                st.warning("""
                **Zastrzeżenie prawne:**
                Ta aplikacja wykorzystuje algorytmy sztucznej inteligencji do oszacowania ryzyka.
                Wynik **NIE JEST** diagnozą medyczną. Nie podejmuj decyzji zdrowotnych wyłącznie na podstawie tego wyniku.
                Zawsze konsultuj się z lekarzem.
                """)

            except Exception as e:
                st.error("Błąd przetwarzania danych. Sprawdź czy wszystkie pola są uzupełnione.")


# =========================================================
# 6. Footer
# =========================================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: grey; font-size: 0.8em;">
        Autor: Kamil Kozik<br>
        <em></em>
        <a href="https://github.com/Kamil955" target="_blank" style="color: grey; text-decoration: none;">
            GitHub 💻
        </a>
    </div>
    """,
    unsafe_allow_html=True
)