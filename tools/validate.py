#!/usr/bin/env python3
"""
SysMLcheap Validator v0.1
Validates YAML model files against the metamodel rules.
Reverse-engineered from SAIC DE Validation Rules v27.
"""

import yaml
import sys
import os
from pathlib import Path
from collections import defaultdict

# ── Helpers ──────────────────────────────────────────────────────────────────

class Issue:
    def __init__(self, rule, element_id, element_name, severity, message):
        self.rule = rule
        self.element_id = element_id
        self.element_name = element_name
        self.severity = severity  # error, warning, info
        self.message = message

    def __str__(self):
        icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(self.severity, "?")
        return f"  {icon} [{self.rule}] {self.element_name} ({self.element_id}): {self.message}"


def load_model(model_dir):
    """Load all YAML files from the model directory into a combined dict."""
    model = {
        "packages": [],
        "requirements": [],
        "sources": [],
        "actors": [],
        "useCases": [],
        "blocks": [],
        "interfaceBlocks": [],
        "signals": [],
        "terms": [],
        "testCases": [],
    }
    for yaml_file in sorted(Path(model_dir).glob("*.yaml")):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data:
                for key in model:
                    if key in data:
                        model[key].extend(data[key])
    return model


def build_index(model):
    """Build a lookup dict: id → element (with _kind added)."""
    index = {}
    kind_map = {
        "packages": "Package",
        "requirements": "Requirement",
        "sources": "SourceContent",
        "actors": "Actor",
        "useCases": "UseCase",
        "blocks": "Block",
        "interfaceBlocks": "InterfaceBlock",
        "signals": "Signal",
        "terms": "Term",
        "testCases": "TestCase",
    }
    for key, kind in kind_map.items():
        for elem in model.get(key, []):
            elem["_kind"] = kind
            index[elem["id"]] = elem
            # Index nested elements too
            for part in elem.get("parts", []):
                part["_kind"] = "PartProperty"
                part["_ownerBlock"] = elem["id"]
                index[part["id"]] = part
            for port in elem.get("ports", []):
                port["_kind"] = "ProxyPort"
                port["_ownerBlock"] = elem["id"]
                index[port["id"]] = port
            for fp in elem.get("flowProperties", []):
                fp["_kind"] = "FlowProperty"
                index[fp["id"]] = fp
            for op in elem.get("operations", []):
                op["_kind"] = "Operation"
                index[op["id"]] = op
    return index


def ref_exists(index, ref_id):
    return ref_id in index


def check_refs(index, refs, issues, rule, elem):
    """Check that all refs in a list resolve."""
    for ref_id in (refs or []):
        if not ref_exists(index, ref_id):
            issues.append(Issue(rule, elem["id"], elem.get("name", "?"),
                               "error", f"Unresolved reference: {ref_id}"))


# ── Validation Rules ─────────────────────────────────────────────────────────

def validate_packages(model, index, issues):
    for pkg in model.get("packages", []):
        if not pkg.get("name"):
            issues.append(Issue("PACKAGENAME", pkg["id"], "", "error", "Package must be named"))


def validate_sources(model, index, issues):
    for src in model.get("sources", []):
        if not src.get("name"):
            issues.append(Issue("ARTIFACTNAME", src["id"], "", "error", "Source content must be named"))
        if not src.get("fileOrUrl"):
            issues.append(Issue("SRCCNT", src["id"], src.get("name", ""), "error",
                               "Source content must have a file name or URL"))


def validate_requirements(model, index, issues):
    for req in model.get("requirements", []):
        if not req.get("text", "").strip():
            issues.append(Issue("REQTEXT", req["id"], req.get("name", ""), "error",
                               "Requirement must have text"))
        if not req.get("name"):
            issues.append(Issue("REQNAME", req["id"], req["id"], "info",
                               "Requirement should have a short summary name"))
        # REQTRACE: must have trace, derive, or refine
        has_trace = bool(req.get("traceRefs"))
        has_derive = bool(req.get("deriveRefs"))
        has_refine = bool(req.get("refineRefs"))
        if not (has_trace or has_derive or has_refine):
            issues.append(Issue("REQTRACE", req["id"], req.get("name", ""), "error",
                               "Requirement must have at least one trace, derive, or refine relationship"))
        # PERFORMANCEFUNCTIONREFINE
        if req.get("kind") == "performance":
            if not has_refine:
                issues.append(Issue("PERFORMANCEFUNCTIONREFINE", req["id"], req.get("name", ""), "error",
                                   "Performance requirements must refine at least one functional requirement"))
        # Check ref validity
        check_refs(index, req.get("traceRefs"), issues, "REF_INTEGRITY", req)
        check_refs(index, req.get("refineRefs"), issues, "REF_INTEGRITY", req)
        check_refs(index, req.get("deriveRefs"), issues, "REF_INTEGRITY", req)


def validate_actors(model, index, issues):
    for actor in model.get("actors", []):
        if not actor.get("name"):
            issues.append(Issue("ACTORNAME", actor["id"], "", "error", "Actor must be named"))
        if not actor.get("documentation", "").strip():
            issues.append(Issue("ACTORDOCUMENTATION", actor["id"], actor.get("name", ""), "error",
                               "Actor must have documentation"))
        # ACTORUSECASE: must have use cases or generalizations
        if not actor.get("useCaseRefs") and not actor.get("generalizationRefs"):
            issues.append(Issue("ACTORUSECASE", actor["id"], actor.get("name", ""), "error",
                               "Actor must be associated with at least one use case or specialize another actor"))
        check_refs(index, actor.get("useCaseRefs"), issues, "REF_INTEGRITY", actor)


def validate_usecases(model, index, issues):
    for uc in model.get("useCases", []):
        if not uc.get("name"):
            issues.append(Issue("USECASENAME", uc["id"], "", "error", "Use case must be named"))
        if not uc.get("documentation", "").strip():
            issues.append(Issue("UCDOCUMENTATION", uc["id"], uc.get("name", ""), "error",
                               "Use case must have documentation"))
        # UCACTOR: must have actor (unless connected via extend/include/generalization)
        has_actors = bool(uc.get("actorRefs"))
        has_include_from = any(
            uc["id"] in (other.get("includeRefs") or [])
            for other in model.get("useCases", [])
        )
        has_extend = bool(uc.get("extendRefs"))
        if not has_actors and not has_include_from and not has_extend:
            issues.append(Issue("UCACTOR", uc["id"], uc.get("name", ""), "error",
                               "Use case must be associated with at least one actor "
                               "(unless connected via extend/include)"))
        # UCTRACE
        has_trace = bool(uc.get("traceRefs"))
        has_extend_out = bool(uc.get("extendRefs"))
        has_include_in = any(
            uc["id"] in (other.get("includeRefs") or [])
            for other in model.get("useCases", [])
        )
        if not has_trace and not has_extend_out and not has_include_in:
            issues.append(Issue("UCTRACE", uc["id"], uc.get("name", ""), "error",
                               "Use case must have a trace, extend, refine, or incoming include relationship"))
        check_refs(index, uc.get("actorRefs"), issues, "REF_INTEGRITY", uc)
        check_refs(index, uc.get("traceRefs"), issues, "REF_INTEGRITY", uc)
        check_refs(index, uc.get("includeRefs"), issues, "REF_INTEGRITY", uc)


def validate_blocks(model, index, issues):
    for blk in model.get("blocks", []):
        if not blk.get("name"):
            issues.append(Issue("BLOCKNAME", blk["id"], "", "error", "Block must be named"))

        stereo = blk.get("stereotype")

        # LOGICALPHYSICAL: can't have both (enforced by enum, but just in case)
        # CONTEXTPORTS: context blocks may not own ports
        if stereo == "context" and blk.get("ports"):
            issues.append(Issue("CONTEXTPORTS", blk["id"], blk.get("name", ""), "error",
                               "System context blocks may not own ports"))

        # CONTEXTPARTS: context blocks must own at least one part
        if stereo == "context" and not blk.get("parts"):
            issues.append(Issue("CONTEXTPARTS", blk["id"], blk.get("name", ""), "error",
                               "System context blocks must own at least one part property"))

        # Validate parts
        for part in blk.get("parts", []):
            if not part.get("typeRef"):
                issues.append(Issue("PARTTYPE", part["id"], part.get("name", ""), "error",
                                   "Part property must be typed"))
            elif part["typeRef"] in index:
                part_type = index[part["typeRef"]]
                # LOGICALARCH: logical block parts must be typed by logical blocks
                if stereo == "logical" and part_type.get("stereotype") not in ("logical", "external"):
                    issues.append(Issue("LOGICALARCH", part["id"], part.get("name", ""), "error",
                                       f"Part in logical block must be typed by logical block "
                                       f"(found: {part_type.get('stereotype')})"))
                # PHYSICALARCH
                if stereo == "physical" and part_type.get("stereotype") not in ("physical", "external"):
                    issues.append(Issue("PHYSICALARCH", part["id"], part.get("name", ""), "error",
                                       f"Part in physical block must be typed by physical block "
                                       f"(found: {part_type.get('stereotype')})"))
            else:
                issues.append(Issue("REF_INTEGRITY", part["id"], part.get("name", ""),
                                   "error", f"Unresolved typeRef: {part['typeRef']}"))

        # Validate ports
        for port in blk.get("ports", []):
            if not port.get("typeRef"):
                issues.append(Issue("PROXYPORTTYPE", port["id"], port.get("name", ""), "error",
                                   "Proxy port must be typed by an interface block"))
            elif port["typeRef"] in index:
                port_type = index[port["typeRef"]]
                if port_type.get("_kind") != "InterfaceBlock":
                    issues.append(Issue("PROXYPORTTYPE", port["id"], port.get("name", ""), "error",
                                       f"Proxy port must be typed by an interface block "
                                       f"(found: {port_type.get('_kind')})"))
                # LOGICALPORT
                if stereo == "logical" and port_type.get("stereotype") != "logical":
                    issues.append(Issue("LOGICALPORT", port["id"], port.get("name", ""), "error",
                                       "Port on logical block must be typed by logical interface block"))
                # PHYSICALPORT
                if stereo == "physical" and port_type.get("stereotype") != "physical":
                    issues.append(Issue("PHYSICALPORT", port["id"], port.get("name", ""), "error",
                                       "Port on physical block must be typed by physical interface block"))
            else:
                issues.append(Issue("REF_INTEGRITY", port["id"], port.get("name", ""),
                                   "error", f"Unresolved typeRef: {port['typeRef']}"))

        # CONBLOCKDOCUMENTATION: blocks typing context parts must have docs
        if stereo in ("context",) and blk.get("parts"):
            for part in blk["parts"]:
                if part.get("typeRef") and part["typeRef"] in index:
                    typed_blk = index[part["typeRef"]]
                    if typed_blk.get("_kind") == "Block" and not typed_blk.get("documentation", "").strip():
                        issues.append(Issue("CONBLOCKDOCUMENTATION", typed_blk["id"],
                                           typed_blk.get("name", ""), "error",
                                           "Block typing a context part must have documentation"))


def validate_interface_blocks(model, index, issues):
    for ib in model.get("interfaceBlocks", []):
        if not ib.get("flowProperties") and not ib.get("ports"):
            issues.append(Issue("INTBLOCKFLOW", ib["id"], ib.get("name", ""), "error",
                               "Interface block must own at least one flow property or port"))
        for fp in ib.get("flowProperties", []):
            if fp.get("direction") not in ("out", "inout"):
                issues.append(Issue("FLOWDIRECTION", fp["id"], fp.get("name", ""), "error",
                                   f"Flow property direction must be 'out' or 'inout' (found: {fp.get('direction')})"))
            if not fp.get("typeRef"):
                issues.append(Issue("FLOWTYPE", fp["id"], fp.get("name", ""), "error",
                                   "Flow property must be typed by a signal"))
            elif fp["typeRef"] in index:
                if index[fp["typeRef"]].get("_kind") != "Signal":
                    issues.append(Issue("FLOWTYPE", fp["id"], fp.get("name", ""), "error",
                                       "Flow property must be typed by a signal"))
            else:
                issues.append(Issue("REF_INTEGRITY", fp["id"], fp.get("name", ""),
                                   "error", f"Unresolved typeRef: {fp['typeRef']}"))


def validate_signals(model, index, issues):
    for sig in model.get("signals", []):
        if not sig.get("name"):
            issues.append(Issue("SIGNALNAME", sig["id"], "", "error", "Signal must be named"))
        if not sig.get("documentation", "").strip():
            issues.append(Issue("SIGNALDOCUMENTATION", sig["id"], sig.get("name", ""), "error",
                               "Signal must have documentation"))


def validate_uniqueness(model, index, issues):
    """Check for duplicate IDs across the entire model."""
    seen = {}
    for key in model:
        for elem in model[key]:
            eid = elem["id"]
            if eid in seen:
                issues.append(Issue("UNIQUE_ID", eid, elem.get("name", ""), "error",
                                   f"Duplicate ID (also in {seen[eid]})"))
            seen[eid] = key


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    model_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "model")
    model_dir = os.path.abspath(model_dir)

    print(f"🔍 SysMLcheap Validator v0.1")
    print(f"   Model directory: {model_dir}\n")

    model = load_model(model_dir)
    index = build_index(model)

    # Count elements
    total = sum(len(v) for v in model.values())
    print(f"   Loaded {total} top-level elements across {len(model)} categories\n")

    issues = []

    # Run all validators
    validate_uniqueness(model, index, issues)
    validate_packages(model, index, issues)
    validate_sources(model, index, issues)
    validate_requirements(model, index, issues)
    validate_actors(model, index, issues)
    validate_usecases(model, index, issues)
    validate_blocks(model, index, issues)
    validate_interface_blocks(model, index, issues)
    validate_signals(model, index, issues)

    # Report
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    infos = [i for i in issues if i.severity == "info"]

    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for issue in errors:
            print(issue)
        print()

    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for issue in warnings:
            print(issue)
        print()

    if infos:
        print(f"ℹ️  INFO ({len(infos)}):")
        for issue in infos:
            print(issue)
        print()

    # Summary
    print("─" * 60)
    if not issues:
        print("✅ Model is clean! No issues found.")
    else:
        print(f"   {len(errors)} errors | {len(warnings)} warnings | {len(infos)} info")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
