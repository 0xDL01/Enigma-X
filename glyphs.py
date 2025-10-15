import random
from rotors import create_full_rotor, reverse_rotor, rotor_bank, apply_rotor_chain, reverse_rotor_chain
from string import ascii_lowercase, digits

charset = ascii_lowercase + digits  # Allowed characters
symbol_hint_map = {i: sym for i, sym in enumerate(['♠️','♣️','♥️','♦️','⭐','🔺','🔻','🔸','🔹','💠'])}

# === Shift Character ===
def shift_char(c, shift):
    if c in charset:
        idx = charset.index(c)
        return charset[(idx + shift) % len(charset)]
    return c

# === Show Shift Table ===
def print_shift_table(shift):
    print(f"\n📜 Shift Mapping ({'+' if shift >= 0 else ''}{shift}):")
    for c in charset:
        print(f"{c} → {shift_char(c, shift)}", end=" | ")
    print("\n")

# === Obfuscate password ===
def obfuscate_password(password, rotor_sequence, shift):
    shifted = ''.join(shift_char(c, shift) for c in password)
    return apply_rotor_chain(shifted, rotor_sequence)

# === De-obfuscate password ===
def deobfuscate_password(encoded, rotor_sequence, shift):
    raw = reverse_rotor_chain(encoded, rotor_sequence)
    return ''.join(shift_char(c, -shift) for c in raw)

# === CLI ===
if __name__ == "__main__":
    print("\n🔐 Enigma X: Vault Password Encoder")
    print("Available rotors:", ", ".join(rotor_bank.keys()))

    rotor_sequence = []
    while True:
        rotor_name = input("Choose rotor (or press Enter to finish): ").strip().lower()
        if not rotor_name:
            break
        if rotor_name not in rotor_bank:
            print("❌ Invalid rotor name. Try again.")
            continue
        start_pos = input("Enter start position (any number): ").strip()
        if not start_pos.isdigit():
            print("❌ Position must be a number.")
            continue
        rotor_sequence.append((rotor_name, int(start_pos)))

    if not rotor_sequence:
        print("❌ No rotors selected.")
        exit()

    print("\n🔧 Mode: (1) Create password, (2) Verify password — Enter 1 or 2:", end=" ")
    mode = input().strip()

    if mode == '1':
        # === Create Password Mode ===
        password = input("🧪 Enter new password to encrypt and store: ").lower()
        shift = random.randint(1, 9)
        shift_symbol = symbol_hint_map[shift]
        print(f"\n🔢 Your secret shift symbol is: {shift_symbol}")
        print_shift_table(shift)
        stored = obfuscate_password(password, rotor_sequence, shift)
        print(f"\n🔐 Stored Obfuscated Password: {stored}")
        print(f"📎 Store this shift hint: {shift_symbol} (+{shift})")

        user_input = input("\n💬 Enter any text to encrypt using same rotors: ")
        glyph_output = apply_rotor_chain(user_input, rotor_sequence)
        print("\n🧿 Encrypted Glyph Output:", glyph_output)

        if input("\n🔁 Reverse it back? (y/n): ").lower() == 'y':
           original = deobfuscate_password(glyph_output, rotor_sequence, shift)
           print("\n✅ Decoded Output:", original)


    elif mode == '2':
        # === Verify Password Mode ===
        stored = input("🔐 Enter stored obfuscated password to verify: ")

        print("\n⚙️ Re-enter the exact rotor sequence used:")
        rotor_sequence_check = []
        while True:
            rotor_name = input("Rotor (or press Enter to finish): ").strip().lower()
            if not rotor_name:
                break
            if rotor_name not in rotor_bank:
                print("❌ Invalid rotor.")
                continue
            start_pos = input("Start position (number): ").strip()
            if not start_pos.isdigit():
                print("❌ Not a number.")
                continue
            rotor_sequence_check.append((rotor_name, int(start_pos)))

        shift_guess = input("\n🔢 Enter the shift number you used (1–9): ").strip()
        if not shift_guess.isdigit() or not (1 <= int(shift_guess) <= 9):
            print("❌ Invalid shift.")
            exit()
        shift = int(shift_guess)
        print_shift_table(shift)
        print("\n📥 Use the table above to re-type your shifted password.")
        guess = input("🔑 Enter your shifted password guess: ").lower()
        re_encoded = apply_rotor_chain(guess, rotor_sequence_check)

        if re_encoded == stored:
            original = deobfuscate_password(stored, rotor_sequence_check, shift)
            print("\n✅ MATCH! Welcome to the vault.")
            print("🔓 Original password was:", original)
        else:
            print("\n❌ Incorrect. Rotor/shift/password mismatch.")

    else:
        print("❌ Invalid mode selected.")
