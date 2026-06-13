import cairosvg

VIOLET_DARK = "#2d1b69"
VIOLET_MID = "#4c1d95"
VIOLET_LIGHT = "#a78bfa"
WHITE = "#ffffff"
WA_GREEN = "#25d366"
RED = "#ef4444"
RED_DARK = "#7f1d1d"
GREEN_DARK = "#064e3b"

FONT = "Liberation Sans"

SQUARE = (1080, 1080)
STORY = (1080, 1920)


def bg_gradient(grad_id="bgGrad", c1=VIOLET_DARK, c2=VIOLET_MID, x1="0%", y1="0%", x2="100%", y2="100%"):
    return f'''<linearGradient id="{grad_id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">
        <stop offset="0%" stop-color="{c1}"/>
        <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>'''


def blobs(width, height):
    return f'''
    <circle cx="{width-150}" cy="120" r="220" fill="{VIOLET_LIGHT}" opacity="0.10"/>
    <circle cx="100" cy="{height-100}" r="260" fill="{VIOLET_LIGHT}" opacity="0.08"/>
    <circle cx="{width-120}" cy="{height-100}" r="140" fill="{WA_GREEN}" opacity="0.08"/>
    <circle cx="120" cy="{height*0.42:.0f}" r="170" fill="{VIOLET_LIGHT}" opacity="0.05"/>
    <circle cx="{width-100}" cy="{height*0.62:.0f}" r="190" fill="{WA_GREEN}" opacity="0.05"/>
    '''


def badge(cx, y):
    return f'''
    <g transform="translate({cx},{y})">
        <rect x="-150" y="-32" width="300" height="64" rx="32" fill="{WHITE}"/>
        <circle cx="-104" cy="0" r="18" fill="{VIOLET_DARK}"/>
        <text x="-104" y="7" font-family="{FONT}" font-size="20" font-weight="bold" fill="{WHITE}" text-anchor="middle">W</text>
        <text x="-72" y="7" font-family="{FONT}" font-size="24" font-weight="bold" fill="{VIOLET_DARK}">WebBot Maroc</text>
    </g>
    '''


def stars(cx, y, size=28, color="#fbbf24"):
    pts = []
    spacing = size * 1.6
    start_x = cx - spacing * 2
    for i in range(5):
        x = start_x + i * spacing
        pts.append(star_path(x, y, size, color))
    return "".join(pts)


def star_path(cx, cy, r, color):
    import math
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        radius = r if i % 2 == 0 else r * 0.42
        x = cx + radius * math.cos(angle)
        y = cy - radius * math.sin(angle)
        points.append(f"{x:.1f},{y:.1f}")
    return f'<polygon points="{" ".join(points)}" fill="{color}"/>'


def cross_icon(cx, cy, r=13, color=RED):
    d = r * 0.62
    return f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.25"/>
    <line x1="{cx-d}" y1="{cy-d}" x2="{cx+d}" y2="{cy+d}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>
    <line x1="{cx-d}" y1="{cy+d}" x2="{cx+d}" y2="{cy-d}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'''


def check_icon(cx, cy, r=13, color=WA_GREEN):
    return f'''<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.25"/>
    <polyline points="{cx-7},{cy} {cx-2},{cy+6} {cx+8},{cy-7}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'''


def render(content, size):
    """Wrap a 1080-wide content fragment (designed on a 1080-tall canvas) into
    a canvas of `size`, with the brand gradient/blobs spanning the full canvas
    and the content vertically centered."""
    width, height = size
    offset = (height - 1080) / 2
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <defs>{bg_gradient()}</defs>
    <rect width="{width}" height="{height}" fill="url(#bgGrad)"/>
    {blobs(width, height)}
    <g transform="translate(0,{offset:.0f})">
        {content}
    </g>
</svg>'''


# ---------------------------------------------------------------------------
# CONTENU 1 — "Votre cabinet est-il visible sur Google ?"
# ---------------------------------------------------------------------------
def content1():
    return f'''
    <!-- Magnifying glass icon -->
    <g transform="translate(540,330)">
        <circle r="120" fill="none" stroke="{WHITE}" stroke-width="22"/>
        <circle r="120" fill="{VIOLET_LIGHT}" opacity="0.12"/>
        <text x="0" y="22" font-family="{FONT}" font-size="110" font-weight="bold" fill="{WHITE}" text-anchor="middle">G</text>
        <line x1="84" y1="84" x2="172" y2="172" stroke="{WHITE}" stroke-width="26" stroke-linecap="round"/>
    </g>

    <!-- Headline -->
    <text x="540" y="560" font-family="{FONT}" font-size="58" font-weight="bold" fill="{WHITE}" text-anchor="middle">Votre cabinet est-il</text>
    <text x="540" y="630" font-family="{FONT}" font-size="58" font-weight="bold" fill="{VIOLET_LIGHT}" text-anchor="middle">visible sur Google ?</text>

    <!-- Subtext -->
    <text x="540" y="700" font-family="{FONT}" font-size="30" fill="{WHITE}" text-anchor="middle" opacity="0.85">8 clients sur 10 cherchent un avocat</text>
    <text x="540" y="742" font-family="{FONT}" font-size="30" fill="{WHITE}" text-anchor="middle" opacity="0.85">ou un notaire en ligne avant de les contacter</text>

    <!-- CTA pill -->
    <rect x="340" y="800" width="400" height="74" rx="37" fill="{WHITE}" opacity="0.12" stroke="{VIOLET_LIGHT}" stroke-width="2"/>
    <text x="540" y="848" font-family="{FONT}" font-size="28" font-weight="bold" fill="{WHITE}" text-anchor="middle">Soyez trouvé en premier</text>

    {badge(540, 990)}
    '''


# ---------------------------------------------------------------------------
# CONTENU 2 — "Chatbot WhatsApp 24h/24"
# ---------------------------------------------------------------------------
def content2():
    return f'''
    <!-- WhatsApp icon -->
    <g transform="translate(540,250)">
        <circle r="80" fill="{WA_GREEN}"/>
        <path transform="translate(-40,-40) scale(3.3)" fill="{WHITE}" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
    </g>

    <!-- Headline -->
    <text x="540" y="400" font-family="{FONT}" font-size="56" font-weight="bold" fill="{WHITE}" text-anchor="middle">Chatbot WhatsApp</text>
    <text x="540" y="468" font-family="{FONT}" font-size="56" font-weight="bold" fill="{WA_GREEN}" text-anchor="middle">disponible 24h/24</text>

    <!-- Chat bubbles -->
    <g>
        <rect x="180" y="540" width="430" height="86" rx="24" fill="{WHITE}" opacity="0.95"/>
        <text x="210" y="595" font-family="{FONT}" font-size="26" fill="{VIOLET_DARK}">Bonjour, vous êtes ouverts ?</text>

        <rect x="470" y="650" width="430" height="86" rx="24" ry="24" fill="{WA_GREEN}"/>
        <text x="500" y="705" font-family="{FONT}" font-size="26" fill="{WHITE}">Oui ! Je réponds 24h/24, 7j/7</text>

        <rect x="180" y="760" width="400" height="86" rx="24" fill="{WHITE}" opacity="0.95"/>
        <text x="210" y="815" font-family="{FONT}" font-size="26" fill="{VIOLET_DARK}">Puis-je prendre rendez-vous ?</text>
    </g>

    <!-- Schedule strip -->
    <rect x="250" y="900" width="580" height="72" rx="36" fill="{WHITE}" opacity="0.12" stroke="{WA_GREEN}" stroke-width="2"/>
    <text x="540" y="946" font-family="{FONT}" font-size="28" font-weight="bold" fill="{WHITE}" text-anchor="middle">Toujours disponible — 7 jours sur 7</text>

    {badge(540, 1030)}
    '''


# ---------------------------------------------------------------------------
# CONTENU 3 — Avant / Après
# ---------------------------------------------------------------------------
def content3():
    col_y = 300
    col_h = 600
    col_w = 410
    left_x = 80
    right_x = 590
    row_gap = 110

    def list_items(items, x, icon_fn):
        out = []
        for i, txt in enumerate(items):
            y = col_y + 150 + i * row_gap
            out.append(icon_fn(x + 46, y - 9))
            out.append(f'<text x="{x+72}" y="{y}" font-family="{FONT}" font-size="25" fill="{WHITE}">{txt}</text>')
        return "".join(out)

    bad = ["Invisible sur Google", "Clients perdus chaque jour", "Pas de réponse le soir", "Image peu professionnelle"]
    good = ["Trouvé facilement en ligne", "Plus de prises de contact", "Réponses 24h/24 via WhatsApp", "Image moderne et rassurante"]

    return f'''
    <text x="540" y="140" font-family="{FONT}" font-size="56" font-weight="bold" fill="{WHITE}" text-anchor="middle">AVANT / APRÈS</text>
    <text x="540" y="190" font-family="{FONT}" font-size="28" fill="{WHITE}" text-anchor="middle" opacity="0.8">Avec ou sans présence digitale</text>

    <!-- Left column: SANS site -->
    <rect x="{left_x}" y="{col_y}" width="{col_w}" height="{col_h}" rx="28" fill="{RED_DARK}" opacity="0.55" stroke="{RED}" stroke-width="2"/>
    <text x="{left_x + col_w/2}" y="{col_y+66}" font-family="{FONT}" font-size="32" font-weight="bold" fill="{WHITE}" text-anchor="middle">SANS site web</text>
    {list_items(bad, left_x, cross_icon)}

    <!-- Right column: AVEC WebBot Maroc -->
    <rect x="{right_x}" y="{col_y}" width="{col_w}" height="{col_h}" rx="28" fill="{GREEN_DARK}" opacity="0.55" stroke="{WA_GREEN}" stroke-width="2"/>
    <text x="{right_x + col_w/2}" y="{col_y+66}" font-family="{FONT}" font-size="32" font-weight="bold" fill="{WHITE}" text-anchor="middle">AVEC WebBot Maroc</text>
    {list_items(good, right_x, check_icon)}

    <!-- VS badge -->
    <circle cx="540" cy="{col_y + col_h/2}" r="44" fill="{WHITE}"/>
    <text x="540" y="{col_y + col_h/2 + 11}" font-family="{FONT}" font-size="30" font-weight="bold" fill="{VIOLET_DARK}" text-anchor="middle">VS</text>

    {badge(540, 1000)}
    '''


# ---------------------------------------------------------------------------
# CONTENU témoignage (générique — visuel 4 et 4b)
# ---------------------------------------------------------------------------
def content_testimonial(initials, quote_lines, name, role):
    quote_block = "".join(
        f'<text x="540" y="{450 + i*44}" font-family="{FONT}" font-size="29" fill="{WHITE}" text-anchor="middle">{line}</text>'
        for i, line in enumerate(quote_lines)
    )
    name_y = 450 + len(quote_lines) * 44 + 70
    stats_y = max(name_y + 134, 760)
    return f'''
    <!-- Quote mark -->
    <text x="160" y="270" font-family="{FONT}" font-size="160" font-weight="bold" fill="{VIOLET_LIGHT}" opacity="0.5">“</text>

    <!-- Avatar -->
    <circle cx="540" cy="240" r="78" fill="{WHITE}"/>
    <text x="540" y="268" font-family="{FONT}" font-size="64" font-weight="bold" fill="{VIOLET_DARK}" text-anchor="middle">{initials}</text>

    <!-- Stars -->
    {stars(540, 360)}

    <!-- Testimonial text -->
    {quote_block}

    <!-- Name -->
    <text x="540" y="{name_y}" font-family="{FONT}" font-size="32" font-weight="bold" fill="{VIOLET_LIGHT}" text-anchor="middle">{name}</text>
    <text x="540" y="{name_y+36}" font-family="{FONT}" font-size="26" fill="{WHITE}" text-anchor="middle" opacity="0.8">{role}</text>

    <!-- Stats -->
    <rect x="120" y="{stats_y}" width="380" height="160" rx="24" fill="{WHITE}" opacity="0.12" stroke="{VIOLET_LIGHT}" stroke-width="2"/>
    <text x="310" y="{stats_y+70}" font-family="{FONT}" font-size="46" font-weight="bold" fill="{WA_GREEN}" text-anchor="middle">+3 clients</text>
    <text x="310" y="{stats_y+112}" font-family="{FONT}" font-size="26" fill="{WHITE}" text-anchor="middle">par semaine</text>

    <rect x="580" y="{stats_y}" width="380" height="160" rx="24" fill="{WHITE}" opacity="0.12" stroke="{VIOLET_LIGHT}" stroke-width="2"/>
    <text x="770" y="{stats_y+70}" font-family="{FONT}" font-size="46" font-weight="bold" fill="{WA_GREEN}" text-anchor="middle">24h/24</text>
    <text x="770" y="{stats_y+112}" font-family="{FONT}" font-size="26" fill="{WHITE}" text-anchor="middle">disponible sur WhatsApp</text>

    {badge(540, stats_y+250)}
    '''


def content4():
    return content_testimonial(
        initials="YB",
        quote_lines=[
            "« Depuis que WebBot Maroc a créé mon site",
            "et mon chatbot WhatsApp, je reçois des",
            "demandes même le soir et le week-end. »",
        ],
        name="Maître Youssef B.",
        role="Avocat — Casablanca",
    )


def content4b():
    return content_testimonial(
        initials="AC",
        quote_lines=[
            "« Depuis que j'ai mon site et mon",
            "chatbot, je reçois des demandes de",
            "clients même le week-end.",
            "Je recommande. »",
        ],
        name="Un avocat casablancais",
        role="Client WebBot Maroc",
    )


# ---------------------------------------------------------------------------
# CONTENU 4A — Nos résultats en chiffres
# ---------------------------------------------------------------------------
def content4a():
    stats = [
        ("7 jours", "délai de livraison du site"),
        ("24h/24", "chatbot WhatsApp disponible"),
        ("2 000 DH", "site vitrine professionnel"),
        ("600 DH/mois", "abonnement chatbot WhatsApp"),
    ]
    box_w, box_h = 420, 220
    gap = 40
    grid_w = box_w * 2 + gap
    start_x = (1080 - grid_w) / 2
    start_y = 330

    cells = []
    for i, (big, small) in enumerate(stats):
        col = i % 2
        row = i // 2
        x = start_x + col * (box_w + gap)
        y = start_y + row * (box_h + gap)
        cells.append(f'''
        <rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="26" fill="{WHITE}" opacity="0.10" stroke="{VIOLET_LIGHT}" stroke-width="2"/>
        <text x="{x+box_w/2}" y="{y+105}" font-family="{FONT}" font-size="50" font-weight="bold" fill="{WA_GREEN}" text-anchor="middle">{big}</text>
        <text x="{x+box_w/2}" y="{y+150}" font-family="{FONT}" font-size="24" fill="{WHITE}" text-anchor="middle" opacity="0.85">{small}</text>''')

    return f'''
    <text x="540" y="160" font-family="{FONT}" font-size="58" font-weight="bold" fill="{WHITE}" text-anchor="middle">Nos résultats</text>
    <text x="540" y="208" font-family="{FONT}" font-size="28" fill="{VIOLET_LIGHT}" text-anchor="middle">en chiffres</text>

    {''.join(cells)}

    <text x="540" y="{start_y + 2*box_h + gap + 60}" font-family="{FONT}" font-size="30" font-weight="bold" fill="{WHITE}" text-anchor="middle">Pour avocats et notaires à Casablanca</text>

    {badge(540, 1010)}
    '''


CONTENT_BUILDERS = {
    "visuel1-google": content1,
    "visuel2-chatbot-whatsapp": content2,
    "visuel3-avant-apres": content3,
    "visuel4-temoignage": content4,
    "visuel4a": content4a,
    "visuel4b": content4b,
}

if __name__ == "__main__":
    import os
    out_dir = os.path.dirname(os.path.abspath(__file__))
    for name, builder in CONTENT_BUILDERS.items():
        content = builder()

        square_svg = render(content, SQUARE)
        square_path = os.path.join(out_dir, f"{name}.png")
        cairosvg.svg2png(bytestring=square_svg.encode("utf-8"), write_to=square_path,
                         output_width=SQUARE[0], output_height=SQUARE[1], background_color="white")
        print("OK:", square_path)

        story_svg = render(content, STORY)
        story_path = os.path.join(out_dir, f"{name}-story.png")
        cairosvg.svg2png(bytestring=story_svg.encode("utf-8"), write_to=story_path,
                         output_width=STORY[0], output_height=STORY[1], background_color="white")
        print("OK:", story_path)
