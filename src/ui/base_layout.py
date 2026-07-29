import streamlit as st


def style_base_layout():
    """Inject design-system CSS — Poppins + Inter, blue palette, premium dashboard feel."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        /* ══════════════════════════════════════════════════
           DESIGN TOKENS
        ══════════════════════════════════════════════════ */
        :root {
            /* Spacing */
            --sp-1:  0.25rem;
            --sp-2:  0.5rem;
            --sp-3:  0.75rem;
            --sp-4:  1rem;
            --sp-5:  1.25rem;
            --sp-6:  1.5rem;
            --sp-8:  2rem;
            --sp-10: 2.5rem;
            --sp-12: 3rem;

            /* Brand */
            --primary:       #2563EB;
            --primary-dark:  #1D4ED8;
            --primary-light: #DBEAFE;
            --primary-muted: #EFF6FF;

            /* Semantic */
            --success:       #10B981;
            --success-light: #D1FAE5;
            --success-muted: #ECFDF5;

            --warning:       #F59E0B;
            --warning-light: #FEF3C7;
            --warning-muted: #FFFBEB;

            --danger:        #EF4444;
            --danger-light:  #FEE2E2;
            --danger-muted:  #FFF5F5;

            --purple:        #8B5CF6;
            --purple-light:  #EDE9FE;
            --purple-muted:  #F5F3FF;

            --teal:          #14B8A6;
            --teal-light:    #CCFBF1;
            --teal-muted:    #F0FDFA;

            /* Neutrals */
            --bg:            #F8FAFC;
            --surface:       #FFFFFF;
            --surface-alt:   #F9FAFB;
            --border:        #E5E7EB;
            --border-light:  #F3F4F6;

            /* Text */
            --text:          #111827;
            --text-secondary:#374151;
            --text-muted:    #6B7280;
            --text-subtle:   #9CA3AF;

            /* Shadows */
            --shadow-xs:    0 1px 2px rgba(0,0,0,0.05);
            --shadow-sm:    0 1px 3px rgba(0,0,0,0.10), 0 1px 2px rgba(0,0,0,0.06);
            --shadow-md:    0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
            --shadow-lg:    0 10px 15px rgba(0,0,0,0.10), 0 4px 6px rgba(0,0,0,0.05);
            --shadow-hover: 0 20px 25px rgba(0,0,0,0.10), 0 10px 10px rgba(0,0,0,0.04);

            /* Radius */
            --r-sm:   6px;
            --r-md:   10px;
            --r-lg:   14px;
            --r-xl:   20px;
            --r-2xl:  24px;
            --r-full: 9999px;
        }

        /* ══════════════════════════════════════════════════
           RESET & BASE
        ══════════════════════════════════════════════════ */
        #MainMenu, footer, header { visibility: hidden; }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
            color: var(--text) !important;
            background: var(--bg) !important;
        }

        [data-testid="stAppViewContainer"] { background: var(--bg) !important; }
        [data-testid="stHeader"]           { display: none !important; }

        .block-container {
            padding-top:    var(--sp-8) !important;
            padding-bottom: var(--sp-8) !important;
            max-width: 1280px;
        }

        /* ══════════════════════════════════════════════════
           MATERIAL SYMBOLS
        ══════════════════════════════════════════════════ */
        .material-symbols-rounded {
            font-family: 'Material Symbols Rounded';
            font-weight: normal;
            font-style: normal;
            font-size: 1.15rem;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            -webkit-font-smoothing: antialiased;
        }

        /* ══════════════════════════════════════════════════
           SPACING UTILITIES
        ══════════════════════════════════════════════════ */
        .section-gap    { display: block; height: var(--sp-8); }
        .section-gap-sm { display: block; height: var(--sp-4); }
        .section-gap-xs { display: block; height: var(--sp-2); }

        /* ══════════════════════════════════════════════════
           TYPOGRAPHY
        ══════════════════════════════════════════════════ */
        .page-eyebrow {
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            color: var(--primary) !important;
            margin: 0 0 var(--sp-2);
        }

        .page-title {
            font-family: 'Poppins', sans-serif;
            font-size: clamp(1.5rem, 2.5vw, 1.9rem);
            font-weight: 700;
            color: var(--text) !important;
            margin: 0;
            line-height: 1.2;
        }

        .page-subtitle {
            font-size: 0.92rem;
            color: var(--text-muted) !important;
            margin: var(--sp-1) 0 0;
            font-weight: 400;
            line-height: 1.6;
        }

        .section-heading {
            font-family: 'Poppins', sans-serif;
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text) !important;
            margin: 0;
        }

        .hint-text {
            margin: var(--sp-2) 0 0;
            text-align: center;
            color: var(--text-subtle) !important;
            font-size: 0.8rem;
        }

        .dashboard-subtitle {
            margin: var(--sp-1) 0 0;
            color: var(--text-muted) !important;
            font-size: 0.92rem;
            font-weight: 500;
        }

        /* ══════════════════════════════════════════════════
           HOME — TOP NAV
        ══════════════════════════════════════════════════ */
        .top-nav {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-xl);
            padding: var(--sp-4) var(--sp-6);
            box-shadow: var(--shadow-sm);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: var(--sp-4);
            margin-bottom: var(--sp-6);
            flex-wrap: wrap;
        }

        .top-nav__brand { display: flex; align-items: center; gap: var(--sp-3); }

        .brand-mark {
            width: 2.5rem; height: 2.5rem;
            border-radius: var(--r-md);
            background: var(--primary-muted) !important;
            border: 1px solid var(--primary-light) !important;
            display: grid; place-items: center;
            color: var(--primary) !important;
            flex-shrink: 0;
        }

        .brand-title {
            display: block;
            font-family: 'Poppins', sans-serif;
            font-size: 0.95rem; font-weight: 700;
            color: var(--text) !important;
            line-height: 1.1;
        }

        .brand-subtitle {
            display: block;
            font-size: 0.73rem;
            color: var(--text-muted) !important;
            margin-top: 0.1rem;
        }

        .top-nav__links { display: flex; align-items: center; gap: 0.2rem; flex-wrap: wrap; }

        .nav-link {
            padding: 0.45rem 0.85rem;
            border-radius: var(--r-full);
            color: var(--text-muted) !important;
            font-size: 0.875rem; font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .nav-link.active {
            background: var(--primary-muted) !important;
            color: var(--primary) !important;
            font-weight: 600;
        }

        .top-nav__actions { display: flex; align-items: center; gap: 0.5rem; margin-left: auto; }

        .nav-icon {
            width: 2.25rem; height: 2.25rem;
            border-radius: var(--r-full);
            border: 1px solid var(--border) !important;
            background: var(--surface-alt) !important;
            display: grid; place-items: center;
            color: var(--text-muted) !important;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .nav-icon:hover {
            background: var(--primary-muted) !important;
            color: var(--primary) !important;
            border-color: var(--primary-light) !important;
        }

        /* ══════════════════════════════════════════════════
           DASHBOARD HEADER
        ══════════════════════════════════════════════════ */
        .dash-header {
            background: linear-gradient(135deg, var(--primary-muted) 0%, #F0F9FF 55%, var(--bg) 100%);
            border: 1px solid var(--primary-light);
            border-radius: var(--r-xl);
            padding: var(--sp-6) var(--sp-8);
            margin-bottom: var(--sp-6);
            position: relative;
            overflow: hidden;
            animation: fadeUp 0.3s ease both;
        }

        .dash-header::after {
            content: '';
            position: absolute;
            top: -40%; right: -5%;
            width: 18rem; height: 18rem;
            background: radial-gradient(circle, rgba(37,99,235,0.06) 0%, transparent 65%);
            border-radius: 50%;
            pointer-events: none;
        }

        .dash-role-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.25rem 0.65rem;
            background: var(--primary-light) !important;
            color: var(--primary) !important;
            border-radius: var(--r-full);
            font-size: 0.70rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: var(--sp-2);
        }

        .dash-name {
            font-family: 'Poppins', sans-serif;
            font-size: clamp(1.5rem, 2.5vw, 2.1rem);
            font-weight: 700;
            color: var(--text) !important;
            margin: 0;
            line-height: 1.2;
        }

        .dash-meta {
            font-size: 0.875rem;
            color: var(--text-muted) !important;
            margin: var(--sp-1) 0 0;
            font-weight: 400;
        }

        /* ══════════════════════════════════════════════════
           KPI CARDS
        ══════════════════════════════════════════════════ */
        .kpi-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--r-lg);
            padding: var(--sp-5);
            box-shadow: var(--shadow-xs);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            position: relative;
            overflow: hidden;
        }

        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: var(--kpi-accent, var(--primary));
            border-radius: var(--r-lg) var(--r-lg) 0 0;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .kpi-icon {
            width: 2.25rem; height: 2.25rem;
            border-radius: var(--r-sm);
            display: flex; align-items: center; justify-content: center;
            font-size: 1rem;
            margin-bottom: var(--sp-3);
            flex-shrink: 0;
        }

        .kpi-value {
            font-family: 'Poppins', sans-serif;
            font-size: 1.85rem;
            font-weight: 700;
            color: var(--text) !important;
            line-height: 1;
            margin: 0;
        }

        .kpi-label {
            font-size: 0.8rem;
            color: var(--text-muted) !important;
            font-weight: 500;
            margin-top: var(--sp-1);
        }

        .kpi-sub {
            font-size: 0.74rem;
            font-weight: 600;
            margin-top: var(--sp-1);
        }

        .kpi-sub.positive { color: var(--success) !important; }
        .kpi-sub.negative { color: var(--danger) !important; }
        .kpi-sub.neutral  { color: var(--text-subtle) !important; }

        /* ══════════════════════════════════════════════════
           TAB BAR
        ══════════════════════════════════════════════════ */
        .tab-bar {
            display: flex;
            gap: 0.25rem;
            background: var(--surface-alt);
            border: 1px solid var(--border);
            border-radius: var(--r-full);
            padding: 0.3rem;
            width: fit-content;
            margin-bottom: var(--sp-6);
            flex-wrap: wrap;
        }

        .tab-item {
            padding: 0.45rem 1rem;
            border-radius: var(--r-full);
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--text-muted) !important;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
            user-select: none;
        }

        .tab-item.active {
            background: var(--surface);
            color: var(--primary) !important;
            box-shadow: var(--shadow-sm);
            font-weight: 600;
        }

        /* ══════════════════════════════════════════════════
           SUBJECT CARDS
        ══════════════════════════════════════════════════ */
        .sub-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-left: 4px solid var(--primary);
            border-radius: var(--r-lg);
            padding: var(--sp-5);
            box-shadow: var(--shadow-xs);
            transition: all 0.18s ease;
            margin-bottom: var(--sp-4);
        }

        .sub-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
            border-left-color: var(--primary-dark);
        }

        .sub-card-name {
            font-family: 'Poppins', sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text) !important;
            margin: 0 0 var(--sp-2);
        }

        .sub-card-meta {
            display: flex;
            align-items: center;
            gap: var(--sp-2);
            flex-wrap: wrap;
            font-size: 0.83rem;
            color: var(--text-muted) !important;
        }

        .code-pill {
            display: inline-flex;
            align-items: center;
            background: var(--primary-light);
            color: var(--primary) !important;
            padding: 0.15rem 0.6rem;
            border-radius: var(--r-full);
            font-size: 0.73rem;
            font-weight: 700;
            font-family: ui-monospace, 'JetBrains Mono', monospace;
            letter-spacing: 0.03em;
        }

        .section-pill {
            display: inline-flex;
            align-items: center;
            background: var(--surface-alt);
            color: var(--text-secondary) !important;
            border: 1px solid var(--border);
            padding: 0.15rem 0.6rem;
            border-radius: var(--r-full);
            font-size: 0.73rem;
            font-weight: 600;
        }

        .sub-stats {
            display: flex;
            gap: var(--sp-2);
            flex-wrap: wrap;
            margin-top: var(--sp-3);
        }

        .sub-stat {
            background: var(--surface-alt);
            border: 1px solid var(--border);
            padding: 0.25rem 0.7rem;
            border-radius: var(--r-full);
            font-size: 0.78rem;
            color: var(--text-secondary) !important;
            font-weight: 500;
        }

        /* ══════════════════════════════════════════════════
           AUTH PAGE
        ══════════════════════════════════════════════════ */
        .auth-shell { display: grid; gap: var(--sp-5); }

        .auth-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: var(--sp-4);
            flex-wrap: wrap;
        }

        .auth-brand { display: flex; align-items: center; gap: var(--sp-3); }

        .auth-brand__logo {
            width: 3.25rem; height: 3.25rem;
            border-radius: var(--r-lg);
            background: var(--primary-muted) !important;
            border: 1px solid var(--primary-light) !important;
            display: grid; place-items: center;
            color: var(--primary) !important;
            box-shadow: var(--shadow-sm);
        }

        .auth-brand__title {
            display: block;
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 800;
            line-height: 1;
            color: var(--primary) !important;
            letter-spacing: 0.02em;
        }

        .auth-brand__subtitle {
            display: block;
            margin-top: 0.2rem;
            font-size: 0.78rem;
            color: var(--text-muted) !important;
        }

        .auth-card {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-2xl);
            box-shadow: var(--shadow-sm);
            padding: var(--sp-6) var(--sp-8);
            animation: fadeUp 0.3s ease both;
        }

        .auth-title {
            margin: var(--sp-2) 0 0;
            font-family: 'Poppins', sans-serif;
            font-size: clamp(1.75rem, 3.5vw, 2.6rem);
            line-height: 1.02;
            font-weight: 800;
            color: var(--text) !important;
        }

        .auth-form { display: grid; gap: var(--sp-4); }

        .auth-actions {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: var(--sp-4);
            margin-top: var(--sp-3);
        }

        /* ══════════════════════════════════════════════════
           FORM INPUTS
        ══════════════════════════════════════════════════ */
        div[data-testid="stTextInput"] label,
        div[data-testid="stPasswordInput"] label {
            color: var(--text-secondary) !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            margin-bottom: var(--sp-1);
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stPasswordInput"] input {
            border-radius: var(--r-md) !important;
            background: var(--surface) !important;
            border: 1.5px solid var(--border) !important;
            color: var(--text) !important;
            font-size: 0.9rem !important;
            transition: border-color 0.15s, box-shadow 0.15s;
        }

        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stPasswordInput"] input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
        }

        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stPasswordInput"] input::placeholder {
            color: var(--text-subtle) !important;
            opacity: 1;
        }

        div[data-testid="stSelectbox"] > div > div {
            border-radius: var(--r-md) !important;
            border: 1.5px solid var(--border) !important;
            background: var(--surface) !important;
            font-size: 0.9rem !important;
        }

        /* ══════════════════════════════════════════════════
           BUTTONS
        ══════════════════════════════════════════════════ */
        div.stButton { width: 100%; }

        div.stButton > button {
            width: 100%;
            min-height: 2.65rem;
            border-radius: var(--r-md);
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem !important;
            font-weight: 600;
            border: 1.5px solid transparent;
            transition: all 0.15s ease;
            letter-spacing: 0.01em;
        }

        div.stButton > button[kind="primary"] {
            background: var(--primary) !important;
            color: #fff !important;
            border-color: var(--primary) !important;
        }

        div.stButton > button[kind="primary"]:hover {
            background: var(--primary-dark) !important;
            border-color: var(--primary-dark) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37,99,235,0.28);
        }

        div.stButton > button[kind="secondary"] {
            background: var(--surface) !important;
            color: var(--primary) !important;
            border-color: var(--primary) !important;
        }

        div.stButton > button[kind="secondary"]:hover {
            background: var(--primary-muted) !important;
            transform: translateY(-1px);
        }

        div.stButton > button[kind="tertiary"] {
            background: transparent !important;
            color: var(--text-muted) !important;
            border-color: var(--border) !important;
        }

        div.stButton > button[kind="tertiary"]:hover {
            background: var(--surface-alt) !important;
            color: var(--text) !important;
        }

        div.stButton > button:focus-visible {
            outline: 2px solid var(--primary) !important;
            outline-offset: 2px;
        }

        /* ══════════════════════════════════════════════════
           PAGE SECTION
        ══════════════════════════════════════════════════ */
        .page-section                { display: grid; gap: var(--sp-4); }
        .page-section + .page-section { margin-top: var(--sp-8); }

        /* ══════════════════════════════════════════════════
           STATUS BADGES
        ══════════════════════════════════════════════════ */
        .status-present {
            display: inline-flex; align-items: center; gap: 0.3rem;
            background: var(--success-muted); color: var(--success) !important;
            padding: 0.2rem 0.6rem; border-radius: var(--r-full);
            font-size: 0.78rem; font-weight: 600;
        }

        .status-absent {
            display: inline-flex; align-items: center; gap: 0.3rem;
            background: var(--danger-muted); color: var(--danger) !important;
            padding: 0.2rem 0.6rem; border-radius: var(--r-full);
            font-size: 0.78rem; font-weight: 600;
        }

        /* ══════════════════════════════════════════════════
           HOME SCREEN — HERO / CARDS
        ══════════════════════════════════════════════════ */
        .hero-section,
        .hero-visual,
        .feature-card,
        .portal-card,
        .metric-card {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-xl);
            box-shadow: var(--shadow-sm);
        }

        .hero-section {
            padding: var(--sp-8);
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 100%;
        }

        .section-kicker {
            margin: 0 0 var(--sp-2);
            color: var(--primary) !important;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .section-title {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            font-size: clamp(1.6rem, 3vw, 2.5rem);
            line-height: 1.1;
            font-weight: 700;
            color: var(--text) !important;
        }

        .section-description {
            margin: var(--sp-3) 0 0;
            color: var(--text-muted) !important;
            line-height: 1.65;
            max-width: 52rem;
            font-size: 0.92rem;
        }

        .hero-title {
            margin: 0.15rem 0 0;
            font-family: 'Poppins', sans-serif;
            font-size: clamp(2.5rem, 5vw, 4.4rem);
            line-height: 1.0;
            letter-spacing: -0.03em;
            font-weight: 800;
            color: var(--text) !important;
        }

        .hero-subtitle {
            margin: var(--sp-4) 0 0;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--primary) !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .hero-description {
            margin: var(--sp-3) 0 0;
            color: var(--text-muted) !important;
            line-height: 1.75;
            max-width: 40rem;
            font-size: 0.92rem;
        }

        .hero-actions, .btn-row, .hero-meta, .hero-visual__chips {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .hero-actions, .btn-row { margin-top: var(--sp-5); }
        .hero-meta              { margin-top: var(--sp-4); }

        .hero-meta__item, .chip {
            padding: 0.45rem 0.8rem;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-full);
            background: var(--surface-alt) !important;
            color: var(--text-muted) !important;
            font-size: 0.83rem;
            font-weight: 500;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            color: var(--text) !important;
        }

        .chip.primary {
            background: var(--primary-muted) !important;
            color: var(--primary) !important;
            border-color: var(--primary-light) !important;
        }

        .hero-visual {
            padding: var(--sp-6);
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
            border-radius: var(--r-lg);
            background: var(--surface-alt) !important;
            padding: var(--sp-4);
        }

        .hero-visual__canvas { display: grid; gap: var(--sp-4); width: 100%; }

        .metric-card, .feature-card, .portal-card {
            transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        .metric-card  { padding: var(--sp-5); justify-content: center; }
        .feature-card { padding: var(--sp-6); justify-content: flex-start; }
        .portal-card  { padding: var(--sp-6); justify-content: flex-start; }

        .metric-card:hover, .feature-card:hover, .portal-card:hover {
            transform: translateY(-2px);
            border-color: var(--primary) !important;
            box-shadow: var(--shadow-md);
        }

        .metric-card__icon, .feature-card__icon, .portal-card__icon {
            width: 2.5rem; height: 2.5rem;
            border-radius: var(--r-md);
            background: var(--primary-muted) !important;
            border: 1px solid var(--primary-light) !important;
            color: var(--primary) !important;
            display: grid; place-items: center;
            margin-bottom: var(--sp-4);
            flex: 0 0 auto;
        }

        .metric-card__value {
            font-family: 'Poppins', sans-serif;
            font-size: 1.9rem;
            line-height: 1;
            color: var(--text) !important;
            font-weight: 700;
        }

        .metric-card__label {
            margin-top: var(--sp-2);
            color: var(--text-muted) !important;
            font-size: 0.83rem;
            font-weight: 500;
        }

        .feature-card__title, .portal-card__title {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            line-height: 1.2;
            font-weight: 600;
            color: var(--text) !important;
        }

        .feature-card__text, .portal-card__text, .muted-copy {
            margin: var(--sp-3) 0 0;
            color: var(--text-muted) !important;
            line-height: 1.65;
            flex: 1 1 auto;
            font-size: 0.9rem;
        }

        .feature-card__text, .portal-card__text { max-width: 34rem; }

        .portal-card__header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: var(--sp-4);
            margin-bottom: var(--sp-4);
        }

        .portal-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.3rem 0.65rem;
            border-radius: var(--r-full);
            background: var(--primary-muted) !important;
            color: var(--primary) !important;
            font-size: 0.70rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .portal-points {
            list-style: none;
            padding: 0;
            margin: var(--sp-4) 0 0;
            display: grid;
            gap: var(--sp-3);
        }

        .portal-points li {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .portal-points li .material-symbols-rounded { color: var(--success); font-size: 1rem; }

        .portal-button-row, .hero-button-row {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: var(--sp-4);
        }

        /* ══════════════════════════════════════════════════
           ANIMATIONS
        ══════════════════════════════════════════════════ */
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(10px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .kpi-card { animation: fadeUp 0.3s ease both; }
        .kpi-card:nth-child(1) { animation-delay: 0.04s; }
        .kpi-card:nth-child(2) { animation-delay: 0.08s; }
        .kpi-card:nth-child(3) { animation-delay: 0.12s; }
        .kpi-card:nth-child(4) { animation-delay: 0.16s; }

        .sub-card { animation: fadeUp 0.25s ease both; }

        /* ══════════════════════════════════════════════════
           RESPONSIVE
        ══════════════════════════════════════════════════ */
        .hide-mobile { display: block; }

        @media (max-width: 1024px) {
            .top-nav__actions { margin-left: 0; }
        }

        @media (max-width: 768px) {
            .hide-mobile, .top-nav__links { display: none; }
            .hero-title    { font-size: clamp(2rem, 10vw, 3rem); }
            .section-title { font-size: clamp(1.4rem, 7vw, 2rem); }
            .hero-actions, .btn-row { flex-direction: column; }
            .top-nav { padding: var(--sp-3) var(--sp-4); }
            .auth-card    { padding: var(--sp-5); }
            .dash-header  { padding: var(--sp-5); }
            .hero-section, .hero-visual,
            .feature-card, .portal-card, .metric-card { border-radius: var(--r-lg); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
