import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. KONFIGURASI HALAMAN & API GEMINI
# ==========================================
st.set_page_config(page_title="Asisten Tugas Kuliah", page_icon="🎓", layout="centered")

# GANTI DENGAN API KEY GEMINI ANDA!
API_KEY = "MASUKKAN_API_KEY_ANDA" 

genai.configure(api_key=API_KEY)

# Parameter Kreatif: Fokus ke edukasi dan bahasa yang rapi
generation_config = {
  "temperature": 0.5, # 0.5 membuat jawaban lebih terstruktur, tidak terlalu ngawur
  "top_p": 0.95,
}

# Inisialisasi Model dengan Persona (Use Case: Asisten Tugas)
model = genai.GenerativeModel(
  model_name="gemini-3.6-flash", # Gunakan model yang stabil
  generation_config=generation_config,
  system_instruction="""Kamu adalah Asisten Tugas Kuliah (Study Buddy). 
  Tugasmu adalah membantu mahasiswa memahami materi, membuat kerangka makalah, 
  menjelaskan konsep yang rumit dengan analogi sederhana, dan membantu brainstorming ide tugas. 
  Gunakan bahasa Indonesia yang rapi, ramah, dan suportif. 
  Jika diminta membuat esai atau jawaban panjang, buat dalam format terstruktur (poin-poin atau paragraf yang rapi)."""
)

# ==========================================
# 2. TAMPILAN UI CHATBOX
# ==========================================
st.title("🎓 Asisten Tugas Kuliah")
st.caption("Tanya materi, minta ide makalah, atau minta penjelasan konsep di sini!")

# Fitur Memory: Menyimpan riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Pesan pembuka
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🧑‍🏫"):
        greeting = "Halo! Ada tugas kuliah apa yang bisa aku bantu hari ini? Mau bahas materi, minta kerangka makalah, atau tanya rumus?"
        st.markdown(greeting)
        st.session_state.messages.append({"role": "assistant", "content": greeting})

# Menampilkan riwayat chat
for message in st.session_state.messages:
    avatar = "🧑‍🏫" if message["role"] == "assistant" else "🧑‍🎓"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ==========================================
# 3. LOGIKA INPUT & RESPON
# ==========================================
if prompt := st.chat_input("Ketik pertanyaan atau tugasmu di sini..."):
    # Tampilkan pertanyaan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    # Dapatkan respons dari Gemini
    with st.chat_message("assistant", avatar="🧑‍🏫"):
        with st.spinner("Sedang menganalisis materi..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")