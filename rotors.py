# rotors.py — Enigma X Rotor Engine (letters + digits only)

from string import ascii_lowercase, digits

# === Base character set: 26 letters + 10 digits ===
base_input = ascii_lowercase + digits  # total 36 characters

# === Rotor Symbol Banks (36 unique symbols each) ===
rotor_bank = {
    "egyptian": [
        '𓂀','𓋴','𓎛','𓅱','𓆑','𓐍','𓊪','𓍯','𓈖','𓃭',
        '𓋹','𓂓','𓎼','𓏭','𓏏','𓂋','𓊃','𓅓','𓈎','𓇋',
        '𓃠','𓇓','𓎡','𓅃','𓊽','𓅮','𓂛','𓇳','𓊸','𓈂',
        '𓍿','𓆣','𓋞','𓐎','𓍇','𓋭'
    ],
    "chinese": [
        '你','我','是','龍','山','大','好','人','火','风',
        '天','口','心','水','木','金','土','雨','雪','愛',
        '神','电','空','虎','馬','魚','鸡','牛','羊','狗',
        '猪','兔','鼠','猴','蛇','龙'
    ],
    "greek": [
        'Α','Β','Γ','Δ','Ε','Ζ','Η','Θ','Ι','Κ',
        'Λ','Μ','Ν','Ξ','Ο','Π','Ρ','Σ','Τ','Υ',
        'Φ','Χ','Ψ','Ω','α','β','γ','δ','ε','ζ',
        'η','θ','ι','κ','λ','μ'
    ],
    "emoji": [
        '🧠','🗝','🔐','🦁','💀','👁','🕳','⚔','👑','🔮',
        '♾','🌒','🌞','📡','👽','🛡','🧬','📿','🌀','☣',
        '🧩','🛸','🌌','☯','♻','🪬','🧿','🫥','🦷','🧲',
        '🫧','🌘','🌑','🌔','🌚','🌜'
    ],
    "custom": [
        '⟡','✪','⚔','☥','⌬','◉','✘','⊕','⚛','⟁',
        '∇','∞','⊗','⊙','✦','⧫','⧗','🜏','🜍','🜎',
        '🜓','🜛','🜞','🜔','🜖','⊚','⊛','⧉','⧇','⨀',
        '⚕','⚚','✜','⨂','⨆','⨏'
    ]
}

# === Create full rotor mapping from symbol set and start position ===
def create_full_rotor(rotor_name: str, start_pos: int = 0):
    symbols = rotor_bank.get(rotor_name)
    if not symbols or len(symbols) < len(base_input):
        raise ValueError("Rotor must have at least 36 symbols for full mapping.")
    rotated = symbols[start_pos % len(symbols):] + symbols[:start_pos % len(symbols)]
    return dict(zip(base_input, rotated[:len(base_input)]))

# === Reverse a rotor mapping ===
def reverse_rotor(rotor_map: dict):
    return {v: k for k, v in rotor_map.items()}

# === Apply a chain of rotors ===
def apply_rotor_chain(text: str, rotor_sequence: list):
    for rotor_name, start_pos in rotor_sequence:
        rotor_map = create_full_rotor(rotor_name, start_pos)
        text = ''.join(rotor_map.get(c, c) for c in text)
    return text

# === Reverse a chain of rotors ===
def reverse_rotor_chain(text: str, rotor_sequence: list):
    for rotor_name, start_pos in reversed(rotor_sequence):
        rotor_map = create_full_rotor(rotor_name, start_pos)
        reverse_map = reverse_rotor(rotor_map)
        text = ''.join(reverse_map.get(c, c) for c in text)
    return text
