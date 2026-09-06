from base64 import b64encode
from pathlib import Path

import streamlit as st

_ASSETS = Path(__file__).with_name("assets")


def _data_uri(filename: str) -> str:
    data = (_ASSETS / filename).read_bytes()
    return "data:image/png;base64," + b64encode(data).decode("ascii")


_BACKGROUND = _data_uri("welcome-background.png")
_LOGO = _data_uri("migrobot-logo.png")
_DASHBOARD_BACKGROUND = _data_uri("dashboard-background.png")


def show_welcome_gate() -> tuple[str, bool]:
    """Форма приветствия: имя и состояние отправки."""
    st.html(f"""
    <style>
      [data-testid="stHeader"] {{display:none;}}
      [data-testid="stAppViewContainer"] {{background:transparent;}}
      .stApp {{min-height:100vh;background:#f254af;overflow:hidden;}}
      .stApp::before {{
        content:"";position:fixed;z-index:0;pointer-events:none;
        left:50%;top:50%;width:100vh;height:100vw;
        transform:translate(-50%,-50%) rotate(90deg);
        background:url("{_BACKGROUND}") center/cover no-repeat;
      }}
      .stApp > * {{position:relative;z-index:1;}}
      .block-container {{max-width:none;padding:0 24px 40px;}}
      .mb-logo-info {{position:fixed;right:5vw;top:5vh;width:85px;height:85px;z-index:10;}}
      .mb-logo-trigger {{display:block;width:100%;height:100%;padding:0;border:0;background:transparent;cursor:help;border-radius:50%;}}
      .mb-logo-trigger:focus-visible {{outline:2px solid white;outline-offset:5px;}}
      .mb-figma-logo {{display:block;width:100%;height:100%;object-fit:contain;}}
      .mb-logo-popover {{position:absolute;right:0;top:100%;width:min(350px,calc(100vw - 48px));padding-top:12px;opacity:0;visibility:hidden;transform:translateY(-4px);transition:opacity .15s ease .25s,transform .15s ease .25s,visibility 0s linear .4s;}}
      .mb-logo-info:hover .mb-logo-popover,.mb-logo-info:focus-within .mb-logo-popover {{opacity:1;visibility:visible;transform:translateY(0);transition-delay:0s;}}
      .mb-logo-note {{padding:18px 20px;border:1px solid rgba(255,255,255,.35);border-radius:16px;background:rgba(69,40,88,.94);box-shadow:0 8px 28px rgba(49,22,68,.16);color:white;font-family:Arial,sans-serif;font-size:14px;line-height:1.6;text-align:left;}}
      .mb-logo-note p {{margin:0;font-size:inherit;line-height:inherit;}}
      .mb-logo-note p + p {{margin-top:12px;}}
      .mb-logo-note a,.mb-logo-note a:visited {{color:white;text-decoration:underline;text-underline-offset:3px;}}
      .mb-logo-note a:hover {{text-decoration-thickness:2px;}}
      .mb-logo-note a:focus-visible {{outline:2px solid white;outline-offset:3px;border-radius:2px;}}
      @media(prefers-reduced-motion:reduce) {{.mb-logo-popover{{transition:none;transform:none;}}}}
      .st-key-welcome-content {{max-width:720px;margin:0 auto;padding-top:37vh;text-align:center;color:white;}}
      .mb-question {{margin:0 auto 28px;color:white;font-family:"Trebuchet MS",Arial,sans-serif;font-size:clamp(25px,2.5vw,40px);font-weight:400;line-height:1.42;letter-spacing:.28em;text-align:center;}}
      .st-key-welcome-name {{max-width:430px;margin:0 auto;}}
      .st-key-welcome-name [data-testid="stTextInputRootElement"],.st-key-welcome-name [data-baseweb="input"],.st-key-welcome-name [data-baseweb="base-input"] {{background:transparent!important;border:0!important;box-shadow:none!important;border-radius:0!important;}}
      .st-key-welcome-name input {{background:transparent!important;border:0!important;border-bottom:2px solid white!important;border-radius:0!important;color:white!important;text-align:center;font-size:23px!important;letter-spacing:.13em!important;box-shadow:none!important;}}
      .st-key-welcome-name input::placeholder {{color:rgba(255,255,255,.22)!important;}}
      .st-key-welcome-actions {{margin-top:18px;}}
      .st-key-welcome-actions button {{border:1px solid rgba(255,255,255,.8);background:transparent!important;color:white;border-radius:24px;padding:8px 30px;box-shadow:none!important;}}
      .st-key-welcome-actions button:hover,.st-key-welcome-actions button:active {{border-color:white;background:transparent!important;color:white;}}
      .st-key-welcome-actions button:focus-visible {{outline:2px solid white;outline-offset:4px;}}
      .st-key-welcome-content [data-testid="stAlert"] {{max-width:430px;margin:12px auto 0;text-align:left;}}
      @media(max-width:700px) {{.mb-logo-info{{width:66px;height:66px;right:24px;top:22px}}.st-key-welcome-content{{padding-top:32vh}}.mb-question{{letter-spacing:.16em}}}}
    </style>
    <div class="mb-logo-info">
      <button class="mb-logo-trigger" type="button" aria-label="О Migrebot и дневнике головной боли" aria-describedby="mb-logo-about">
        <img class="mb-figma-logo" src="{_LOGO}" alt="Логотип MigreBot">
      </button>
      <div class="mb-logo-popover">
        <div class="mb-logo-note" id="mb-logo-about" role="note">
          <p>Сделано для аналитики данных из бота <a href="https://t.me/migrebot" target="_blank" rel="noopener noreferrer">t.me/migrebot</a></p>
          <p>Дневник головной боли сделан в Университетской клинике головной боли <a href="https://headache.ru" target="_blank" rel="noopener noreferrer">https://headache.ru</a>.</p>
        </div>
      </div>
    </div>
    """)
    with st.container(key="welcome-content"):
        st.html('<p class="mb-question">привет, как к тебе<br>можно обращаться?</p>')
        with st.form("welcome-form", border=False):
            name = st.text_input(
                "Как к вам обращаться?", placeholder="ваше имя", max_chars=20,
                label_visibility="collapsed", key="welcome-name",
            )
            with st.container(horizontal=True, horizontal_alignment="center", key="welcome-actions"):
                submitted = st.form_submit_button("Продолжить", key="welcome-continue")
        return name, submitted


def show_main_header(name: str) -> None:
    st.html(f"""
    <style>
      .stApp {{font-family:Arial,sans-serif;background:#FFE0CA url("{_DASHBOARD_BACKGROUND}") center/cover no-repeat fixed;overflow:auto;}}
      [data-testid="stAppViewContainer"] {{background:transparent;}}
      [data-testid="stHeader"] {{display:none;}}
      .block-container {{max-width:1320px;padding-top:2.4rem;}}
      .mb-brand {{display:flex;align-items:center;gap:12px;padding-bottom:24px;margin-bottom:34px;border-bottom:1px solid #DEE7E3;color:#243B3B;}}
      .mb-mark {{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:12px;background:#45877C;color:white;font-size:26px;font-weight:700;}}
      .mb-brand-name {{font-size:27px;font-weight:700;}}
      .mb-brand-note {{margin-left:auto;font-size:14px;color:#687B79;}}
      .st-key-diary-upload {{border-radius:24px;padding:24px;background:rgba(255,255,255,.88);}}
      .mb-figma-logo {{width: 3vw;height: auto;}}
      .mb-steps {{margin:44px 0 20px;color:#243B3B;}}
      .mb-steps h2 {{font-size:27px;letter-spacing:-.6px;margin-bottom:24px;}}
      .mb-step-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}}
      .mb-step {{padding:24px;border-radius:18px;background:#F2F6F5;}}
      .mb-step-number {{font-size:14px;font-weight:700;color:#45877C;}}
      .mb-step h3 {{font-size:20px;margin:16px 0 10px;}}
      .mb-step p {{color:#687B79;font-size:15px;line-height:1.6;margin:0;}}
      @media(max-width:740px) {{.mb-brand-note{{display:none}}.mb-step-grid{{grid-template-columns:1fr}}.block-container{{padding-top:1.5rem}}}}
    </style>
    <div class="mb-brand"><img class="mb-figma-logo" src="{_LOGO}"><span class="mb-brand-name"> Migrebot</span>Ваш дневник головной боли</span></div>
    """)
    st.title(f"Привет, {name}!")
    st.write("Загрузите дневник из бота, чтобы увидеть частоту и интенсивность боли.")


def show_steps() -> None:
    st.html("""
    <section class="mb-steps"><h2>От записей — к понятной картине</h2><div class="mb-step-grid">
      <article class="mb-step"><span class="mb-step-number">01</span><h3>Выгрузите дневник</h3><p>Сохраните историю записей из Migrebot в формате CSV.</p></article>
      <article class="mb-step"><span class="mb-step-number">02</span><h3>Загрузите файл</h3><p>Выберите CSV на этой странице. Данные появятся автоматически.</p></article>
      <article class="mb-step"><span class="mb-step-number">03</span><h3>Посмотрите динамику</h3><p>Выберите период и изучите частоту и интенсивность боли.</p></article>
    </div></section>
    """)
