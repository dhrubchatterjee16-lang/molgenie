"""
Command-Line Interface for MolGenie
"""

import argparse
from .generator import screen_pains_and_sa_score, smiles_to_selfies_safe
from .retrosynthesis import RetrosynthesisEngine

def main():
    parser = argparse.ArgumentParser(
        prog="molgenie",
        description="MolGenie: Generative AI, Retrosynthetic Feasibility & Medicinal Chemistry Filter"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    audit_parser = subparsers.add_parser("audit", help="Audit molecular candidate for synthesizability & PAINS")
    audit_parser.add_argument("--smiles", type=str, default="CC(=O)Oc1ccccc1C(=O)O", help="SMILES string (e.g., Aspirin)")

    args = parser.parse_args()

    if args.command == "audit":
        med = screen_pains_and_sa_score(args.smiles)
        retro = RetrosynthesisEngine().audit_molecule(args.smiles)

        print("\n--- MolGenie Generative & Retrosynthesis Audit ---")
        print(f"SMILES:               {args.smiles}")
        print(f"SELFIES:              {med.selfies}")
        print(f"Synthetically Viable: {'YES (<= 4 steps)' if retro.is_synthetically_accessible else 'NO (High Complexity/Unphysical)'}")
        print(f"Estimated Steps:      {retro.estimated_step_count}")
        print(f"SA Score (1-10):      {retro.synthetic_accessibility_score}")
        print(f"Commercial Feas %:    {retro.commercial_feasibility_pct}%")
        print(f"PAINS Alerts:         {med.pains_alerts if med.pains_alerts else 'None (Clean)'}")
        print(f"Reaction Classes:     {', '.join(retro.reaction_classes)}")
        if retro.matched_precursors:
            print("Matched Precursors:")
            for p in retro.matched_precursors:
                print(f"  * {p}")
        print(f"Recommendation:       {med.recommendation}\n")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
