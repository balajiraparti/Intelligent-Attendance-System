import streamlit as st

# Accent colours cycling through the palette so each card feels distinct
_ACCENTS = [
    ("#2563EB", "#EFF6FF"),  # blue
    ("#8B5CF6", "#F5F3FF"),  # purple
    ("#14B8A6", "#F0FDFA"),  # teal
    ("#F59E0B", "#FFFBEB"),  # amber
    ("#10B981", "#ECFDF5"),  # green
    ("#EF4444", "#FFF5F5"),  # red
]


def subject_card(name, code, section, stats=None, footer_callback=None, index: int = 0):
    """
    Renders a premium subject card.

    Parameters
    ----------
    name            : Subject name
    code            : Subject code  (shown as a monospace pill)
    section         : Section label (shown as a neutral pill)
    stats           : List of (icon_emoji, label, value) tuples
    footer_callback : Callable — rendered below the stats (e.g. action buttons)
    index           : Position in the list; drives accent colour cycling
    """
    accent_color, accent_bg = _ACCENTS[index % len(_ACCENTS)]

    # ── Stats chips ──────────────────────────────────────────────────────
    stats_html = ""
    if stats:
        chips = "".join(
            f'<span class="sub-stat">{icon} <strong>{value}</strong> {label}</span>'
            for icon, label, value in stats
        )
        stats_html = f'<div class="sub-stats">{chips}</div>'

    st.markdown(
        f"""
        <div class="sub-card" style="border-left-color: {accent_color};">
            <p class="sub-card-name">{name}</p>
            <div class="sub-card-meta">
                <span class="code-pill" style="background:{accent_bg}; color:{accent_color};">{code}</span>
                <span class="sub-card-sep" style="color:var(--border);">·</span>
                <span class="section-pill">§ {section}</span>
            </div>
            {stats_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if footer_callback:
        footer_callback()
