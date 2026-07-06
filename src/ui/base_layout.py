import streamlit as st


def style_base_layout():
    """Inject custom CSS for a premium, flat attendance dashboard."""
    st.markdown(
        """
        <style>
@import url('https://fonts.googleapis.com/css2?family=Bowlby+One&family=Changa+One:ital@0;1&display=swap');
        
        #MainMenu, footer, header{
        visibility: hidden;
        }
        :root {
            --space-1: 0.5rem;
            --space-2: 1rem;
            --space-3: 1.5rem;
            --space-4: 2rem;
            --space-5: 2.5rem;
            --bg: #F7FBFF;
            --surface: #FFFFFF;
            --surface-alt: #FDFEFF;
            --text-main: #1F2937;
            --text-muted: #64748B;
            --primary: #5789FF;
            --primary-hover: #517891;
            --primary-light: #90D5FF;
            --primary-soft: rgba(87, 137, 255, 0.10);
            --accent: #77B1D4;
            --border: #DCE8F4;
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
            --shadow: 0 2px 12px rgba(31, 41, 55, 0.04);
            --shadow-hover: 0 10px 24px rgba(31, 41, 55, 0.08);
        }

        html, body, [class*="css"] {
            font-family: "Changa One", sans-serif !important;
            color: var(--text-main) !important;
            background: var(--bg) !important;
        }

        .material-symbols-rounded {
            font-family: 'Material Symbols Rounded';
            font-weight: normal;
            font-style: normal;
            font-size: 1.1rem;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
        }

        [data-testid="stAppViewContainer"] {
            background: var(--bg) !important;
        }

        [data-testid="stHeader"] {
            background: var(--surface) !important;
            border-bottom: 1px solid var(--border) !important;
        }

        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 2rem !important;
            max-width: 1240px;
        }

        .main-stack {
            display: grid;
            gap: var(--space-4);
        }

        .top-nav {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 20px;
            padding: 1rem 1.25rem;
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: var(--space-3);
            flex-wrap: wrap;
        }

        .top-nav__brand {
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .brand-mark {
            width: 2.75rem;
            height: 2.75rem;
            border-radius: 16px;
            background: var(--primary-soft) !important;
            border: 1px solid var(--border) !important;
            display: grid;
            place-items: center;
            color: var(--primary) !important;
        }

        .brand-title {
            display: block;
            font-family: 'Syne', sans-serif;
            font-size: 1.02rem;
            font-weight: 800;
            color: var(--text-main) !important;
            line-height: 1.1;
        }

        .brand-subtitle {
            display: block;
            font-size: 0.78rem;
            color: var(--text-muted) !important;
            margin-top: 0.1rem;
        }

        .top-nav__links {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .nav-link {
            padding: 0.6rem 0.9rem;
            border-radius: 12px;
            color: var(--text-muted) !important;
            font-size: 0.92rem;
            font-weight: 600;
            line-height: 1;
        }

        .nav-link.active {
            color: var(--text-main) !important;
            background: var(--primary-soft) !important;
        }

        .top-nav__actions {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-left: auto;
        }

        .nav-icon {
            width: 2.5rem;
            height: 2.5rem;
            border-radius: 999px;
            border: 1px solid var(--border) !important;
            background: var(--surface-alt) !important;
            display: grid;
            place-items: center;
            color: var(--text-main) !important;
        }

        .section-kicker {
            margin: 0 0 0.5rem;
            color: var(--primary) !important;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .section-title {
            margin: 0;
            font-family: 'Syne', sans-serif;
            font-size: clamp(1.8rem, 3vw, 2.8rem);
            line-height: 1.05;
            color: var(--text-main) !important;
        }

        .section-description {
            margin: 0.75rem 0 0;
            color: var(--text-muted) !important;
            line-height: 1.65;
            max-width: 52rem;
        }

        .hero-section,
        .hero-visual,
        .feature-card,
        .portal-card,
        .metric-card {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 20px;
            box-shadow: var(--shadow);
        }

        .hero-section {
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 100%;
        }

        .hero-title {
            margin: 0.15rem 0 0;
            font-family: 'Syne', sans-serif;
            font-size: clamp(2.5rem, 5vw, 4.8rem);
            line-height: 0.95;
            letter-spacing: -0.04em;
            color: #1F2937 !important;
        }

        .hero-subtitle {
            margin: 1rem 0 0;
            font-size: 1.02rem;
            font-weight: 600;
            color: var(--primary) !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .hero-description {
            margin: 0.85rem 0 0;
            color: var(--text-muted) !important;
            line-height: 1.75;
            max-width: 40rem;
        }

        .hero-actions,
        .btn-row,
        .hero-meta,
        .hero-visual__chips {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .hero-actions,
        .btn-row {
            margin-top: 1.25rem;
        }

        .hero-meta {
            margin-top: 1rem;
        }

        .hero-meta__item,
        .chip {
            padding: 0.55rem 0.8rem;
            border: 1px solid var(--border) !important;
            border-radius: 999px;
            background: var(--surface-alt) !important;
            color: var(--text-muted) !important;
            font-size: 0.86rem;
            font-weight: 600;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            color: var(--text-main) !important;
        }

        .chip.primary {
            background: var(--primary-soft) !important;
            color: var(--primary-hover) !important;
        }

        .hero-visual {
            padding: 1.5rem;
            height: 100%;
            display: flex;
            align-items: stretch;
        }

        .hero-image-wrap {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 18rem;
            border: 1px solid var(--border) !important;
            border-radius: 18px;
            background: var(--surface-alt) !important;
            padding: 1rem;
        }

        .hero-image-wrap img {
            display: block;
            width: 100%;
            max-width: 240px;
            height: auto;
        }

        .hero-visual__canvas {
            display: grid;
            gap: 1rem;
            width: 100%;
        }

        .hero-stat-grid,
        .feature-grid,
        .portal-grid {
            display: grid;
            gap: 1rem;
        }

        .hero-stat-grid {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .feature-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .portal-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .metric-card,
        .feature-card,
        .portal-card {
            transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        .metric-card {
            padding: 1.25rem;
            justify-content: center;
        }

        .feature-card {
            padding: 1.5rem;
            justify-content: flex-start;
        }

        .portal-card {
            padding: 1.5rem;
            justify-content: flex-start;
        }

        .metric-card:hover,
        .feature-card:hover,
        .portal-card:hover {
            transform: translateY(-3px);
            border-color: var(--primary) !important;
            box-shadow: var(--shadow-hover);
        }

        .metric-card__icon,
        .feature-card__icon,
        .portal-card__icon {
            width: 2.7rem;
            height: 2.7rem;
            border-radius: 14px;
            background: var(--primary-soft) !important;
            border: 1px solid rgba(87, 137, 255, 0.15) !important;
            color: var(--primary) !important;
            display: grid;
            place-items: center;
            margin-bottom: 1rem;
            flex: 0 0 auto;
        }

        .metric-card__icon {
            margin-bottom: 0.75rem;
        }

        .metric-card__value {
            font-family: 'Syne', sans-serif;
            font-size: 2rem;
            line-height: 1;
            color: #1F2937 !important;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .metric-card__label {
            margin-top: 0.45rem;
            color: var(--text-muted) !important;
            font-size: 0.92rem;
            font-weight: 600;
        }

        .feature-card__title,
        .portal-card__title {
            margin: 0;
            font-family: 'Syne', sans-serif;
            font-size: 1.35rem;
            line-height: 1.1;
            color: #1F2937 !important;
        }

        .feature-card__text,
        .portal-card__text,
        .muted-copy {
            margin: 0.7rem 0 0;
            color: var(--text-muted) !important;
            line-height: 1.7;
            flex: 1 1 auto;
        }

        .feature-card__text,
        .portal-card__text {
            max-width: 34rem;
        }

        .portal-card__header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .portal-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.4rem 0.7rem;
            border-radius: 999px;
            background: var(--primary-soft) !important;
            color: var(--primary-hover) !important;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .portal-points {
            list-style: none;
            padding: 0;
            margin: 1rem 0 0;
            display: grid;
            gap: 0.75rem;
        }

        .portal-points li {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            color: var(--text-main);
            font-size: 0.95rem;
        }

        .portal-points li .material-symbols-rounded {
            color: var(--success);
            font-size: 1rem;
        }

        div.stButton {
            width: 100%;
        }

        div.stButton > button {
            width: 100%;
            min-height: 3rem;
            border-radius: 14px;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem !important;
            font-weight: 600;
            border: 1px solid transparent;
            transition: transform 0.16s ease, box-shadow 0.16s ease, background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease;
        }

        div.stButton > button[kind="primary"] {
            background: var(--primary) !important;
            color: #FFFFFF !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background: var(--primary-hover) !important;
            transform: translateY(-1px);
            box-shadow: var(--shadow-hover);
        }

        div.stButton > button[kind="secondary"] {
            background: #FFFFFF !important;
            color: var(--primary) !important;
            border-color: var(--primary) !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            background: #FFFFFF !important;
            color: var(--primary-hover) !important;
            border-color: var(--primary-hover) !important;
            transform: translateY(-1px);
            box-shadow: var(--shadow-hover);
        }

        div.stButton > button:focus {
            box-shadow: 0 0 0 3px rgba(87, 137, 255, 0.2);
        }

        .hide-mobile {
            display: block;
        }

        .portal-button-row,
        .hero-button-row {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            align-items: stretch;
        }

        .page-section {
            display: grid;
            gap: var(--space-2);
        }

        .page-section + .page-section {
            margin-top: var(--space-4);
        }

        .auth-shell {
            display: grid;
            gap: 1.25rem;
        }

        .auth-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .auth-brand {
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }

        .auth-brand__logo {
            width: 3.5rem;
            height: 3.5rem;
            border-radius: 16px;
            background: var(--primary-soft) !important;
            border: 1px solid var(--border) !important;
            display: grid;
            place-items: center;
            color: var(--primary) !important;
            box-shadow: var(--shadow);
        }

        .auth-brand__title {
            display: block;
            font-family: 'Bowlby One', sans-serif;
            font-size: 1.7rem;
            line-height: 0.95;
            color: #5161E6 !important;
            letter-spacing: 0.02em;
        }

        .auth-brand__subtitle {
            display: block;
            margin-top: 0.25rem;
            font-size: 0.82rem;
            color: var(--text-muted) !important;
        }

        .auth-card {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 24px;
            box-shadow: var(--shadow);
            padding: 1.75rem;
        }

        .auth-title {
            margin: 0;
            font-family: 'Bowlby One', sans-serif;
            font-size: clamp(2rem, 4vw, 3.25rem);
            line-height: 0.98;
            letter-spacing: 0.01em;
            color: #111827 !important;
        }

        .auth-form {
            display: grid;
            gap: 1rem;
        }

        .auth-actions {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            margin-top: 0.75rem;
        }

        div[data-testid="stTextInput"] label,
        div[data-testid="stPasswordInput"] label {
            color: var(--text-main) !important;
            font-weight: 600 !important;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stPasswordInput"] input {
            border-radius: 14px !important;
            background: var(--surface-alt) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-main) !important;
        }

        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stPasswordInput"] input::placeholder {
            color: var(--text-muted) !important;
            opacity: 1;
        }

        @media (max-width: 1024px) {
            .hero-stat-grid,
            .feature-grid,
            .portal-grid,
            .portal-button-row,
            .hero-button-row {
                grid-template-columns: 1fr;
            }

            .hero-section,
            .hero-visual {
                min-height: auto;
            }

            .top-nav__actions {
                margin-left: 0;
            }
        }

        @media (max-width: 768px) {
            .hide-mobile,
            .top-nav__links {
                display: none;
            }

            .hero-title {
                font-size: clamp(2.2rem, 12vw, 3.5rem);
            }

            .section-title {
                font-size: clamp(1.5rem, 8vw, 2.2rem);
            }

            .hero-actions,
            .btn-row {
                flex-direction: column;
            }

            .top-nav {
                padding: 0.9rem 1rem;
            }

            .hero-section,
            .hero-visual,
            .feature-card,
            .portal-card,
            .metric-card {
                border-radius: 18px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
