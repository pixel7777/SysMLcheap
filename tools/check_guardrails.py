#!/usr/bin/env python3
"""
Guardrail checks for source-of-truth consistency across:
- model/behavioral.yaml (use cases)
- specs/use-cases/*.lds.yaml
- specs/physical/*.physical.md
- docs/architecture/physical-index.md
"""

from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent


def norm_uc(value: str) -> str:
    v = (value or "").strip().lower()
    v = v.replace("-", "_")
    if not v.startswith("uc_"):
        v = f"uc_{v}"
    return v


def load_behavioral_use_cases() -> set[str]:
    behavioral = ROOT / "model" / "behavioral.yaml"
    data = yaml.safe_load(behavioral.read_text()) or {}
    return {norm_uc(uc.get("id", "")) for uc in data.get("useCases", []) if uc.get("id")}


def load_lds_refs() -> tuple[set[str], list[str]]:
    errors = []
    refs = set()
    for p in sorted((ROOT / "specs" / "use-cases").glob("*.lds.yaml")):
        data = yaml.safe_load(p.read_text()) or {}
        ref = data.get("useCaseRef")
        if not ref:
            errors.append(f"{p}: missing useCaseRef")
            continue
        refs.add(norm_uc(ref))
    return refs, errors


def load_physical_refs() -> tuple[set[str], list[str]]:
    errors = []
    refs = set()
    pattern = re.compile(r"^\*\*Use Case Ref:\*\*\s*`([^`]+)`", re.MULTILINE)

    for p in sorted((ROOT / "specs" / "physical").glob("*.physical.md")):
        text = p.read_text()
        m = pattern.search(text)
        if not m:
            errors.append(f"{p}: missing '**Use Case Ref:** `uc_...`' line")
            continue
        refs.add(norm_uc(m.group(1)))
    return refs, errors


def load_index_refs() -> tuple[set[str], list[str]]:
    errors = []
    refs = set()
    index = ROOT / "docs" / "architecture" / "physical-index.md"
    if not index.exists():
        return refs, ["docs/architecture/physical-index.md is missing"]

    text = index.read_text()
    for m in re.finditer(r"`(uc[_-][^`]+)`", text):
        refs.add(norm_uc(m.group(1)))

    if not refs:
        errors.append("docs/architecture/physical-index.md: no use case refs found")

    return refs, errors


def main() -> int:
    errors: list[str] = []

    behavioral_ucs = load_behavioral_use_cases()
    lds_refs, lds_errors = load_lds_refs()
    physical_refs, phys_errors = load_physical_refs()
    index_refs, index_errors = load_index_refs()

    errors.extend(lds_errors)
    errors.extend(phys_errors)
    errors.extend(index_errors)

    for ref in sorted(lds_refs):
        if ref not in behavioral_ucs:
            errors.append(f"LDS ref not found in behavioral useCases: {ref}")

    for ref in sorted(physical_refs):
        if ref not in behavioral_ucs:
            errors.append(f"Physical spec ref not found in behavioral useCases: {ref}")

    missing_in_index = (lds_refs | physical_refs) - index_refs
    if missing_in_index:
        errors.append(
            "physical-index missing refs: " + ", ".join(sorted(missing_in_index))
        )

    if errors:
        print("❌ Guardrail check failed:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("✅ Guardrail check passed")
    print(f"  Behavioral use cases: {len(behavioral_ucs)}")
    print(f"  LDS refs: {len(lds_refs)}")
    print(f"  Physical refs: {len(physical_refs)}")
    print(f"  Indexed refs: {len(index_refs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
