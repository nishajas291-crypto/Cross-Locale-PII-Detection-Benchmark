"""Generate a synthetic PII benchmark (no real personal data) with US and Indian formats.
Every sentence has gold entity spans (character offsets), so detectors can be scored exactly.
Run: python generate_data.py  -> data/synthetic_pii.jsonl
"""
import json, random, string
from faker import Faker

SEED = 42
N_PER_LOCALE = 600          # sentences with PII per locale
N_HARD_NEG = 300            # sentences with NO PII but PII-looking strings
random.seed(SEED); Faker.seed(SEED)
fk = {"US": Faker("en_US"), "IN": Faker("en_IN")}

# ---------- format generators ----------
def phone(loc):
    if loc == "US":
        a = f"{random.randint(2,9)}{random.randint(0,9)}{random.randint(0,9)}"
        b = f"{random.randint(2,9)}{random.randint(0,9)}{random.randint(0,9)}"
        c = f"{random.randint(0,9999):04d}"
        return random.choice([f"({a}) {b}-{c}", f"{a}-{b}-{c}", f"+1 {a} {b} {c}", f"{a}.{b}.{c}"])
    d = f"{random.randint(6,9)}{''.join(random.choices(string.digits, k=9))}"
    return random.choice([f"+91 {d[:5]} {d[5:]}", f"+91-{d}", f"{d[:5]} {d[5:]}", f"0{d}", d])

# Verhoeff checksum so generated Aadhaar numbers are structurally valid
_d = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],[4,0,1,2,3,9,5,6,7,8],
      [5,9,8,7,6,0,4,3,2,1],[6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],[8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]]
_p = [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],
      [9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],[2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]]
_inv = [0,4,3,2,1,5,6,7,8,9]
def verhoeff_check(num):
    c = 0
    for i, ch in enumerate(reversed(num)):
        c = _d[c][_p[(i + 1) % 8][int(ch)]]
    return str(_inv[c])
def aadhaar():
    base = str(random.randint(2, 9)) + "".join(random.choices(string.digits, k=10))
    n = base + verhoeff_check(base)
    return random.choice([f"{n[:4]} {n[4:8]} {n[8:]}", n, f"{n[:4]}-{n[4:8]}-{n[8:]}"])
def pan():
    return ("".join(random.choices(string.ascii_uppercase, k=3)) + random.choice("PCHFATBLJG") +
            random.choice(string.ascii_uppercase) + f"{random.randint(0,9999):04d}" + random.choice(string.ascii_uppercase))

GEN = {
    "PERSON": lambda loc: fk[loc].name(),
    "EMAIL_ADDRESS": lambda loc: fk[loc].email(),
    "PHONE_NUMBER": phone,
    "CREDIT_CARD": lambda loc: fk[loc].credit_card_number(card_type=random.choice(["visa", "mastercard"])),
    "US_SSN": lambda loc: fk["US"].ssn(),
    "IN_AADHAAR": lambda loc: aadhaar(),
    "IN_PAN": lambda loc: pan(),
}
LOCALE_ENTITIES = {"US": ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN"],
                   "IN": ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "IN_AADHAAR", "IN_PAN"]}

# ---------- sentence templates: {E0} {E1} are slots ----------
TEMPLATES = {
    "PERSON": ["Meeting notes: {E0} will lead the review on Friday.", "Please forward this ticket to {E0}.", "{E0} joined the support call late."],
    "EMAIL_ADDRESS": ["You can reach the team at {E0} for any questions.", "Send the invoice to {E0} by Monday.", "Contact: {E0}"],
    "PHONE_NUMBER": ["Call me back on {E0} when you are free.", "Customer phone: {E0}", "Our helpline number is {E0}, open 9 to 5."],
    "CREDIT_CARD": ["The payment failed for card {E0}.", "Card on file: {E0}", "Please charge {E0} for the renewal."],
    "US_SSN": ["Applicant SSN: {E0}", "My social security number is {E0}, please verify.", "Tax form lists SSN {E0}."],
    "IN_AADHAAR": ["Aadhaar number: {E0}", "KYC failed for Aadhaar {E0}.", "Please verify my Aadhaar {E0} at the branch."],
    "IN_PAN": ["PAN card number: {E0}", "Submit PAN {E0} for the tax declaration.", "Income tax portal rejected PAN {E0}."],
}
MULTI = [("PERSON", "PHONE_NUMBER", "{E0} can be contacted on {E1}."),
         ("PERSON", "EMAIL_ADDRESS", "Hi, this is {E0}, my email is {E1}."),
         ("PERSON", "CREDIT_CARD", "{E0} paid using card {E1} yesterday.")]

def build(template, ents, loc):
    text, spans, pos = "", [], 0
    parts = template.replace("{E1}", "{E0}").split("{E0}") if False else None
    # fill slots left to right
    out, i, k = "", 0, 0
    while i < len(template):
        if template.startswith("{E", i):
            slot = int(template[i + 2]); etype = ents[slot]
            val = GEN[etype](loc)
            spans.append({"type": etype, "start": len(out), "end": len(out) + len(val), "text": val})
            out += val; i += 4
        else:
            out += template[i]; i += 1
    return out, spans

def hard_negative():
    d = lambda n: "".join(random.choices(string.digits, k=n))
    L = lambda n: "".join(random.choices(string.ascii_uppercase, k=n))
    cands = [f"Order ID {d(12)} has shipped.", f"Ticket reference {L(5)}{d(4)}{L(1)} was closed.",
             f"ISBN {d(3)}-{d(1)}-{d(2)}-{d(6)}-{d(1)} is out of print.", f"Build number {d(4)}-{d(4)}-{d(4)} passed all tests.",
             f"Product code {L(5)}{d(4)}{L(1)} is back in stock.", f"The meeting is on {random.randint(1,28)}/{random.randint(1,12)}/2026.",
             f"Server 10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)} restarted at noon.",
             f"Invoice total was {d(3)}.{d(2)} dollars for {random.randint(2,9)} items.", f"Tracking number {d(16)} is in transit.",
             f"The reference {d(4)} {d(4)} {d(4)} belongs to the warehouse system.", "Please review the quarterly report before the meeting.",
             f"Version {random.randint(1,9)}.{random.randint(0,20)}.{random.randint(0,99)} was released today."]
    return random.choice(cands)

def main():
    rows = []
    for loc in ("US", "IN"):
        for _ in range(N_PER_LOCALE):
            if random.random() < 0.25:
                a, b, t = random.choice(MULTI); ents = [a, b]; tmpl = t
            else:
                e = random.choice(LOCALE_ENTITIES[loc]); ents = [e]; tmpl = random.choice(TEMPLATES[e])
            text, spans = build(tmpl, ents, loc)
            rows.append({"locale": loc, "text": text, "entities": spans})
    for _ in range(N_HARD_NEG):
        rows.append({"locale": "NONE", "text": hard_negative(), "entities": []})
    random.shuffle(rows)
    with open("data/synthetic_pii.jsonl", "w") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows)} sentences, {sum(len(r['entities']) for r in rows)} gold entities")

if __name__ == "__main__":
    main()
