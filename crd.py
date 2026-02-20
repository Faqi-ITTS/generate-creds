import streamlit as st
import string
import secrets
import streamlit.components.v1 as components
import html
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="NEXUS | Ultimate Gen",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (AURORA GLASSMORPHISM - LIGHT THEME) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&family=Fira+Code:wght@500;700&display=swap');

    /* Animasi Latar Belakang Gradien Terang */
    .stApp {
        background: linear-gradient(-45deg, #F8FAFC, #EFF6FF, #F0FDF4, #F8FAFC);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Outfit', sans-serif;
        color: #0F172A;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    h1, h2, h3 { font-family: 'Outfit', sans-serif; font-weight: 700; letter-spacing: -0.5px; }
    
    /* Efek Glassmorphism untuk Container Password */
    .glass-panel {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .glass-panel:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.1);
    }

    /* Teks Password */
    .pwd-text {
        font-family: 'Fira Code', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
        letter-spacing: 2px;
        word-break: break-all;
        margin-bottom: 20px;
    }

    /* Tombol Copy Modern */
    .btn-copy-pro {
        background: linear-gradient(135deg, #0F172A, #334155);
        color: white;
        border: none;
        padding: 14px 28px;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        border-radius: 10px;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.2);
        transition: all 0.2s;
    }
    .btn-copy-pro:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.3);
    }

    /* Tombol Generate Utama di Sidebar */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #3B82F6, #6366F1);
        border: none;
        border-radius: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    /* Modifikasi Metrics Streamlit agar lebih clean */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #2563EB;
    }

</style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE ---
if 'current_pwd' not in st.session_state:
    st.session_state['current_pwd'] = None
if 'pwd_history' not in st.session_state:
    st.session_state['pwd_history'] = []

# --- FUNGSI KALKULASI & GENERATE ---
def format_time(seconds):
    if seconds < 1: return "Instan", "🔴 Sangat Bahaya"
    if seconds < 3600: return f"{int(seconds/60)} Menit", "🟡 Lemah"
    if seconds < 86400: return f"{int(seconds/3600)} Jam", "🟡 Lumayan"
    if seconds < 31536000: return f"{int(seconds/86400)} Hari", "🟢 Kuat"
    years = seconds / 31536000
    if years < 1000: return f"{int(years)} Tahun", "🟢 Sangat Kuat"
    if years < 1000000: return f"{int(years/1000)} Ribu Thn", "🔵 Level Militer"
    return "> 1 Miliar Abad", "💎 Sempurna (Anti-Quantum)"

def analyze_password(pwd, pool_size):
    length = len(pwd.replace("-", "")) # Jangan hitung pemisah sebagai kekuatan utama
    entropy = length * math.log2(pool_size) if pool_size > 0 else 0
    
    # Superkomputer masa depan (100 Triliun tebakan/detik)
    guesses_per_second = 100_000_000_000_000 
    crack_seconds = (pool_size ** length) / guesses_per_second

    time_str, status_str = format_time(crack_seconds)
    strength_pct = min(int((entropy / 130) * 100), 100)

    return {
        "pwd": pwd, "entropy": round(entropy, 1), 
        "crack_time": time_str, "status": status_str, "pct": strength_pct
    }

def generate_password(length, use_upper, use_lower, use_numbers, use_symbols, use_grouping):
    characters = ""
    password = []
    pool_size = 0
    
    if use_upper: characters += string.ascii_uppercase; password.append(secrets.choice(string.ascii_uppercase)); pool_size += 26
    if use_lower: characters += string.ascii_lowercase; password.append(secrets.choice(string.ascii_lowercase)); pool_size += 26
    if use_numbers: characters += string.digits; password.append(secrets.choice(string.digits)); pool_size += 10
    if use_symbols: characters += string.punctuation; password.append(secrets.choice(string.punctuation)); pool_size += len(string.punctuation)
        
    if not characters: return None
        
    while len(password) < length:
        password.append(secrets.choice(characters))
        
    secrets.SystemRandom().shuffle(password)
    raw_pwd = "".join(password)
    
    # Fitur Pemisah / Grouping (Setiap 4 karakter)
    if use_grouping:
        final_pwd = "-".join(raw_pwd[i:i+4] for i in range(0, len(raw_pwd), 4))
    else:
        final_pwd = raw_pwd
        
    data = analyze_password(final_pwd, pool_size)
    
    # Simpan ke history (Maksimal 5)
    st.session_state['pwd_history'].insert(0, data)
    if len(st.session_state['pwd_history']) > 5:
        st.session_state['pwd_history'].pop()
        
    return data

# --- UI SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=60) # Ikon Shield Premium
    st.title("Parameter")
    
    length = st.slider("Panjang Inti", min_value=12, max_value=64, value=20, 
                       help="Semakin panjang, semakin mustahil diretas.")
    
    st.markdown("**Opsi Cerdas**")
    use_grouping = st.toggle("Gunakan Pemisah (-)", value=True, 
                             help="Memecah password agar mudah dibaca oleh mata manusia.")

    st.markdown("**Karakter**")
    use_upper = st.checkbox("Huruf Besar (A-Z)", value=True)
    use_lower = st.checkbox("Huruf Kecil (a-z)", value=True)
    use_numbers = st.checkbox("Angka (0-9)", value=True)
    use_symbols = st.checkbox("Simbol (!@#$)", value=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate Password ✨", type="primary", use_container_width=True):
        if not (use_upper or use_lower or use_numbers or use_symbols):
            st.error("Pilih minimal satu kombinasi!")
        else:
            st.session_state['current_pwd'] = generate_password(length, use_upper, use_lower, use_numbers, use_symbols, use_grouping)

# --- UI UTAMA ---
st.markdown("<h1>NEXUS <span style='color: #3B82F6;'>Ultimate</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1.1rem; margin-bottom: 30px;'>Kriptografi tingkat militer dengan antarmuka memanjakan mata.</p>", unsafe_allow_html=True)

data = st.session_state['current_pwd']

if data:
    safe_display = html.escape(data['pwd'])
    safe_attr = html.escape(data['pwd'], quote=True)
    
    # 1. Glassmorphism Panel
    st.markdown(f"""
        <div class="glass-panel">
            <div style="font-size: 0.9rem; color: #64748B; margin-bottom: 10px; font-weight: bold; text-transform: uppercase;">Kata Sandi Anda</div>
            <div class="pwd-text">{safe_display}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tombol Copy JS
    copy_js = f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <input type="text" value="{safe_attr}" id="pwdInput" style="position: absolute; left: -9999px;">
            <button class="btn-copy-pro" onclick="copyToClipboard()" id="copyBtn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>
                Salin ke Clipboard
            </button>
            <div id="copyStatus" style="color: #059669; font-weight: 700; font-family: 'Outfit', sans-serif; margin-top: 12px; font-size: 0.9rem; height: 1.5rem;"></div>
        </div>
        <script>
            function copyToClipboard() {{
                var copyText = document.getElementById("pwdInput");
                copyText.select(); copyText.setSelectionRange(0, 99999);
                try {{
                    navigator.clipboard.writeText(copyText.value).then(function() {{
                        document.getElementById("copyStatus").innerText = "✨ Berhasil disalin dengan aman!";
                        setTimeout(function() {{ document.getElementById("copyStatus").innerText = ""; }}, 3000);
                    }});
                }} catch (err) {{ document.execCommand('copy'); document.getElementById("copyStatus").innerText = "✨ Tersalin!"; }}
            }}
        </script>
        """
    components.html(copy_js, height=90)

    # 2. Metrik Keamanan Canggih
    st.progress(data['pct'], text=f"Skor Ketahanan Kriptografi: {data['pct']}% - {data['status']}")
    st.write("")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Waktu Retas (Brute-Force)", data['crack_time'], delta="Aman", delta_color="normal")
    m2.metric("Skor Entropi", f"{data['entropy']} bits", delta="Standar Tinggi")
    m3.metric("Panjang Total", f"{len(data['pwd'])} char", delta="Termasuk Pemisah" if "-" in data['pwd'] else None)

    st.markdown("---")

    # 3. Fitur History (Brankas Sesi)
    with st.expander("🗄️ Lihat Riwayat Password (Sesi Ini)"):
        st.markdown("*(Menyimpan 5 password terakhir yang Anda buat agar tidak hilang jika salah klik)*")
        for i, hist in enumerate(st.session_state['pwd_history']):
            st.code(hist['pwd'], language="plaintext")

else:
    st.info("👋 Selamat datang! Tentukan parameter di sebelah kiri dan klik Generate.")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; color: #94A3B8; font-size: 0.85rem; margin-top: 60px; font-family: 'Outfit', sans-serif;">
        Arsitek Sistem: <b>Muhammad Nur Faqi</b><br>
        © 2026 Nexus Security Module
    </div>
""", unsafe_allow_html=True)
