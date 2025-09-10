import json
import sys

# Mappatura dei nomi comuni a SPDX ID
KNOWN_LICENSE_ALIASES = {
    "license :: osi approved :: apache software license": "Apache-2.0",
    "apache software license": "Apache-2.0",
    "license :: osi approved :: mit license": "MIT",
    "mit license": "MIT",
    "license :: osi approved :: bsd license": "BSD-3-Clause",
    "bsd license": "BSD-3-Clause",
    "license :: osi approved :: isc license": "ISC",
    "isc license": "ISC",
    "license :: osi approved :: mozilla public license 2.0 (mpl 2.0)": "MPL-2.0",
    "mozilla public license 2.0 (mpl 2.0)": "MPL-2.0",
    "license :: osi approved :: python software foundation license": "Python-2.0",
    "license :: osi approved :: gnu lesser general public license v2 or later (lgplv2+)": "LGPL-2.1-or-later"
}


with open("SBOM.json", "r") as f:
    bom = json.load(f)

components_without_license = []
licenses_in_use = set()
declared_packages = []

for component in bom.get("components", []):
    licenses = component.get("licenses", [])
    if not licenses:
        name = component.get("name", "UNKNOWN")
        components_without_license.append(name)
        declared_packages.append(name)
    else:
        for entry in licenses:
            lic = entry.get("license")
            if lic:
                if "id" in lic:
                    licenses_in_use.add(lic["id"])
                elif "name" in lic:
                    raw = lic["name"].strip().lower()
                    normalized = KNOWN_LICENSE_ALIASES.get(raw, lic["name"])
                    licenses_in_use.add(normalized)
            elif "expression" in entry:
                licenses_in_use.add(entry["expression"])
            else:
                # nessuna info chiara, metti nella lista di controllo manuale
                name = component.get("name", "UNKNOWN")
                declared_packages.append(name)

# Rimuovi duplicati
licenses_in_use = set(licenses_in_use)

print("=== License Report ===")
print("Licenze in uso (normalizzate):")
for license in sorted(licenses_in_use):
    print(f" - {license}")

if components_without_license:
    print("\nComponenti senza licenza dichiarata:")
    for comp in components_without_license:
        print(f" - {comp}")

if declared_packages:
    print("\n⚠️  Pacchetti da verificare manualmente su PyPI:")
    for pkg in declared_packages:
        print(f" - {pkg} → https://pypi.org/project/{pkg}/")

# Fallisce la pipeline se ci sono problemi
errors = []
if components_without_license:
    errors.append("Trovati componenti senza licenza.")

if errors:
    print("\n❌ License check FAILED:")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)

print("\n✅ License check PASSED")
