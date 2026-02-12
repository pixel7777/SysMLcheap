# Metamodel

This directory contains the YAML schema definitions for our lightweight MBSE toolchain.

## Files

- `metamodel.yaml` — The core metamodel: all element types, their properties, allowed relationships, and stereotypes
- `validation-rules.yaml` — Validation rules (inspired by SAIC DE v27) adapted for our YAML-based model
- `diagram-mappings.yaml` — Mapping from model elements to PlantUML diagram types (future)

## Design Philosophy

This metamodel is reverse-engineered from the SAIC DE Validation Rules v27 and Style Guide Process 1-pager v27.
It captures the *semantic intent* of SysML/Cameo modeling in a format that:

1. Can be authored and reviewed in any text editor
2. Can be validated by scripts for completeness and consistency
3. Can generate PlantUML diagrams for visualization
4. Can generate tables and reports (traceability matrices, etc.)

We deliberately exclude Cameo-specific concepts (customizations, profile development rules, model federation)
and focus on the core modeling constructs needed for a single-team project.
