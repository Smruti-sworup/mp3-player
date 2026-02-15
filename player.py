import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client

# Initialize Supabase Client with a simpler, direct connection
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    
    # We remove the "options" parameter entirely to stop the AttributeError
    # This uses the default settings which are most stable for local VS Code runs
    return create_client(url, key)

supabase = init_supabase()
BUCKET = "music-library" # Your confirmed bucket name

def show_player():
    DANCER_GIF = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXZueXJueXJueXJueXJueXJueXJueXJueXJueXJueXJueCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/3o7TKMGpxxS0D6052w/giphy.gif"

    st.markdown("""
        <style>
        .audio-container { width: 100%; max-width: 400px; margin: auto; overflow: hidden; border-radius: 20px; background: #282828; }
        audio { width: 150%; margin-left: -10px; filter: invert(1) hue-rotate(150deg) brightness(1.5); }
        .disc-plate {
            width: 220px; height: 220px; border-radius: 50%;
            background: radial-gradient(circle, #222 10%, #111 100%);
            border: 5px solid #444; margin: auto;
            animation: spin 4s linear infinite; animation-play-state: paused;
            box-shadow: 0 15px 40px rgba(0,0,0,0.8);
            position: relative; z-index: 2;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        .stButton>button { background: none!important; color: #fa243c!important; border: none!important; font-size: 2.5rem!important; }
        .dancer { position: absolute; top: -40px; left: 50%; transform: translateX(-50%); width: 180px; z-index: 1; display: none; }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state.role}**")
        if st.session_state.role == "admin":
            st.markdown("### ☁️ Admin Upload")
            f = st.file_uploader("Select MP3 file", type=["mp3"]) #
            
            if f is not None:
                if st.button("🚀 Confirm Cloud Upload"):
                    try:
                        file_bytes = f.getvalue()
                        # Uploading directly to FavMP3
                        supabase.storage.from_(BUCKET).upload(f.name, file_bytes)
                        st.success(f"Successfully uploaded: {f.name}")
                        st.rerun() #
                    except Exception as e:
                        st.error(f"Upload failed: {e}")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # Fetch song list from FavMP3 bucket
    try:
        res = supabase.storage.from_(BUCKET).list()
        mp3_files = [item['name'] for item in res if item['name'].endswith('.mp3')]
    except Exception as e:
        st.error(f"Could not connect to FavMP3 bucket: {e}")
        mp3_files = []

    if mp3_files:
        song_name = mp3_files[st.session_state.current_index]
        # Remove the .public_url at the end
        song_url = supabase.storage.from_(BUCKET).get_public_url(song_name)

        st.markdown('<div style="text-align:center; position:relative; margin-top:60px;">', unsafe_allow_html=True)
        st.markdown(f'<img src="{DANCER_GIF}" class="dancer" id="dancer">', unsafe_allow_html=True)
        st.markdown('<div class="disc-plate" id="disc"><div style="width:45px;height:45px;background:#fa243c;border-radius:50%;margin:83px auto;border:2px solid #fff;"></div></div>', unsafe_allow_html=True)
        
        st.header(song_name.split('.')[0])
        
        c1, c2, c3 = st.columns([1,1,1])
        if c1.button("⏪"):
            st.session_state.current_index = (st.session_state.current_index - 1) % len(mp3_files)
            st.rerun()
        if c2.button("⏸️" if st.session_state.is_playing else "▶️"):
            st.session_state.is_playing = not st.session_state.is_playing
            st.rerun()
        if c3.button("⏩"):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(mp3_files)
            st.rerun()

        st.markdown('<div class="audio-container">', unsafe_allow_html=True)
        st.audio(song_url)
        st.markdown('</div>', unsafe_allow_html=True)

        state = "running" if st.session_state.is_playing else "paused"
        disp = "block" if st.session_state.is_playing else "none"
        cmd = "play()" if st.session_state.is_playing else "pause()"
        
        components.html(f"""
            <script>
            var a = window.parent.document.querySelector('audio');
            if(a) {{
                a.{cmd};
                window.parent.document.getElementById('disc').style.animationPlayState = '{state}';
                window.parent.document.getElementById('dancer').style.display = '{disp}';
            }}
            </script>
        """, height=0)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("The FavMP3 Cloud Library is empty.")