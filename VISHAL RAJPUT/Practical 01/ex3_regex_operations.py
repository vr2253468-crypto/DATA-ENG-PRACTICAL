import re

text = """
Log:
- Alice: alice@work.com, Phone: 555-0199
- Bob: bad-email@domain, Phone: 555-0200
"""


emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
print("Valid Emails:", emails)


line = "Item1; 29.99 | InStock , Category-A"
print("Tokens:", [t.strip() for t in re.split(r"[;,|]", line)])


masked = re.sub(r"\b([A-Za-z0-9._%+-]+)(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b", r"****\2", text)
print("\nMasked Log:\n", masked)