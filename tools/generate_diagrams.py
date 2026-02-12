#!/usr/bin/env python3
"""
SysMLcheap Diagram Generator v0.1
Generates PlantUML diagrams from YAML model files.
"""

import yaml
import sys
import os
from pathlib import Path


def load_model(model_dir):
    """Load all YAML files from the model directory."""
    model = {}
    for yaml_file in sorted(Path(model_dir).glob("*.yaml")):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data:
                for key, val in data.items():
                    model.setdefault(key, []).extend(val if isinstance(val, list) else [val])
    return model


def build_index(model):
    index = {}
    for key in model:
        for elem in model[key]:
            index[elem["id"]] = elem
            for sub_key in ("parts", "ports", "flowProperties", "operations"):
                for sub in elem.get(sub_key, []):
                    index[sub["id"]] = sub
    return index


# ── Use Case Diagram ─────────────────────────────────────────────────────────

def generate_use_case_diagram(model, index):
    lines = [
        "@startuml Use Case Diagram",
        "left to right direction",
        'skinparam packageStyle rectangle',
        "",
    ]

    # Actors
    for actor in model.get("actors", []):
        lines.append(f'actor "{actor["name"]}" as {actor["id"]}')
    lines.append("")

    # Use cases in a rectangle
    lines.append('rectangle "Croatian Learning App" {')
    for uc in model.get("useCases", []):
        lines.append(f'  usecase "{uc["name"]}" as {uc["id"]}')
    lines.append("}")
    lines.append("")

    # Actor → UseCase associations
    for actor in model.get("actors", []):
        for uc_ref in actor.get("useCaseRefs", []):
            lines.append(f"{actor['id']} --> {uc_ref}")

    # Include relationships
    for uc in model.get("useCases", []):
        for inc_ref in uc.get("includeRefs", []):
            lines.append(f"{uc['id']} ..> {inc_ref} : <<include>>")

    # Extend relationships
    for uc in model.get("useCases", []):
        for ext_ref in uc.get("extendRefs", []):
            lines.append(f"{uc['id']} ..> {ext_ref} : <<extend>>")

    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


# ── Block Definition Diagram ─────────────────────────────────────────────────

def generate_bdd(model, index, stereotype_filter=None):
    """Generate a Block Definition Diagram for blocks of a given stereotype."""
    title = f"Block Definition Diagram"
    if stereotype_filter:
        title += f" — {stereotype_filter.title()} Architecture"

    lines = [
        f"@startuml {title}",
        "skinparam class {",
        "  BackgroundColor<<logical>> LightBlue",
        "  BackgroundColor<<physical>> Plum",
        "  BackgroundColor<<context>> LightGreen",
        "  BackgroundColor<<external>> LightGray",
        "  BackgroundColor<<software>> LightYellow",
        "}",
        "",
    ]

    blocks = model.get("blocks", [])
    if stereotype_filter:
        # Include context + filtered + external
        blocks = [b for b in blocks
                  if b.get("stereotype") in (stereotype_filter, "context", "external")]

    for blk in blocks:
        stereo = blk.get("stereotype", "")
        stereo_tag = f" <<{stereo}>>" if stereo else ""
        lines.append(f'class "{blk["name"]}"{stereo_tag} as {blk["id"]} {{')

        # Value properties
        for vp in blk.get("valueProperties", []):
            vp_type = index.get(vp.get("typeRef", ""), {}).get("name", "?")
            lines.append(f"  {vp.get('name', '?')} : {vp_type}")

        # Operations
        for op in blk.get("operations", []):
            lines.append(f"  {op.get('name', '?')}()")

        # Ports (shown as fields for BDD)
        for port in blk.get("ports", []):
            port_type = index.get(port.get("typeRef", ""), {}).get("name", "?")
            conj = "~" if port.get("conjugated") else ""
            lines.append(f"  <<port>> {conj}{port.get('name', '?')} : {port_type}")

        lines.append("}")
        lines.append("")

    # Composition relationships (owner → part type)
    for blk in blocks:
        for part in blk.get("parts", []):
            type_ref = part.get("typeRef", "")
            if type_ref in index:
                part_name = part.get("name", "")
                lines.append(f'{blk["id"]} *-- {type_ref} : {part_name}')

    # Realization relationships
    for blk in blocks:
        for real_ref in blk.get("realizationRefs", []):
            if real_ref in index:
                lines.append(f'{blk["id"]} ..|> {real_ref} : <<realize>>')

    # Generalization relationships
    for blk in blocks:
        for gen_ref in blk.get("generalizationRefs", []):
            if gen_ref in index:
                lines.append(f'{blk["id"]} --|> {gen_ref}')

    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


# ── Interface Block Diagram ──────────────────────────────────────────────────

def generate_interface_diagram(model, index, stereotype_filter=None):
    title = "Interface Blocks"
    if stereotype_filter:
        title += f" — {stereotype_filter.title()}"

    lines = [
        f"@startuml {title}",
        "skinparam class {",
        "  BackgroundColor<<logical>> LightBlue",
        "  BackgroundColor<<physical>> Plum",
        "}",
        "",
    ]

    ibs = model.get("interfaceBlocks", [])
    if stereotype_filter:
        ibs = [ib for ib in ibs if ib.get("stereotype") == stereotype_filter]

    for ib in ibs:
        stereo = ib.get("stereotype", "")
        stereo_tag = f" <<{stereo}>>" if stereo else ""
        lines.append(f'class "{ib["name"]}"{stereo_tag} as {ib["id"]} {{')
        for fp in ib.get("flowProperties", []):
            sig_name = index.get(fp.get("typeRef", ""), {}).get("name", "?")
            direction = fp.get("direction", "?")
            lines.append(f"  {direction} {fp.get('name', '?')} : {sig_name}")
        lines.append("}")
        lines.append("")

    # Signal taxonomy
    signals = model.get("signals", [])
    if stereotype_filter:
        signals = [s for s in signals if s.get("stereotype") == stereotype_filter
                   or not s.get("stereotype")]

    for sig in signals:
        lines.append(f'class "{sig["name"]}" <<signal>> as {sig["id"]}')

    lines.append("")

    # Flow property → signal dependencies
    for ib in ibs:
        for fp in ib.get("flowProperties", []):
            type_ref = fp.get("typeRef", "")
            if type_ref in index:
                lines.append(f'{ib["id"]} ..> {type_ref} : <<conveys>>')

    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


# ── Requirements Diagram ─────────────────────────────────────────────────────

def generate_requirements_diagram(model, index):
    lines = [
        "@startuml Requirements Diagram",
        "skinparam class {",
        "  BackgroundColor<<functional>> LightBlue",
        "  BackgroundColor<<performance>> Wheat",
        "  BackgroundColor<<interface>> LightGreen",
        "  BackgroundColor<<constraint>> LightCoral",
        "  BackgroundColor<<business>> Lavender",
        "}",
        "",
    ]

    for req in model.get("requirements", []):
        kind = req.get("kind", "functional")
        # Truncate text for display
        text = req.get("text", "").strip()[:80].replace('"', "'")
        if len(req.get("text", "").strip()) > 80:
            text += "..."
        lines.append(f'class "{req.get("name", req["id"])}" <<{kind}>> as {req["id"]} {{')
        lines.append(f'  {text}')
        lines.append("}")
        lines.append("")

    # Derive relationships
    for req in model.get("requirements", []):
        for ref in req.get("deriveRefs", []):
            lines.append(f'{req["id"]} ..> {ref} : <<deriveReqt>>')
        for ref in req.get("refineRefs", []):
            lines.append(f'{req["id"]} ..> {ref} : <<refine>>')
        for ref in req.get("traceRefs", []):
            if ref in index and index[ref].get("_kind") == "SourceContent":
                pass  # Skip source traces to reduce clutter

    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


# ── Package Diagram ──────────────────────────────────────────────────────────

def generate_package_diagram(model, index):
    lines = [
        "@startuml Package Structure",
        "",
    ]

    # Build tree
    root_pkgs = [p for p in model.get("packages", []) if not p.get("ownerRef")]
    child_map = {}
    for p in model.get("packages", []):
        owner = p.get("ownerRef")
        if owner:
            child_map.setdefault(owner, []).append(p)

    def render_package(pkg, indent=0):
        prefix = "  " * indent
        children = child_map.get(pkg["id"], [])
        if children:
            lines.append(f'{prefix}package "{pkg["name"]}" as {pkg["id"]} {{')
            for child in children:
                render_package(child, indent + 1)
            lines.append(f"{prefix}}}")
        else:
            lines.append(f'{prefix}package "{pkg["name"]}" as {pkg["id"]}')

    for pkg in root_pkgs:
        render_package(pkg)

    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    model_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "model")
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "..", "diagrams")

    model_dir = os.path.abspath(model_dir)
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print(f"📊 SysMLcheap Diagram Generator v0.1")
    print(f"   Model: {model_dir}")
    print(f"   Output: {output_dir}\n")

    model = load_model(model_dir)
    index = build_index(model)

    diagrams = {
        "use-case-diagram.puml": generate_use_case_diagram(model, index),
        "bdd-logical.puml": generate_bdd(model, index, "logical"),
        "interface-blocks-logical.puml": generate_interface_diagram(model, index, "logical"),
        "requirements-diagram.puml": generate_requirements_diagram(model, index),
        "package-structure.puml": generate_package_diagram(model, index),
    }

    for filename, content in diagrams.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  ✅ {filename}")

    print(f"\n   Generated {len(diagrams)} diagrams.")
    print(f"   View them at: https://www.plantuml.com/plantuml/uml/")
    print(f"   Or install PlantUML locally: apt install plantuml")


if __name__ == "__main__":
    main()
