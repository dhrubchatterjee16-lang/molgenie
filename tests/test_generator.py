"""
Tests for SELFIES Conversion & PAINS Screening
"""

import unittest
from molgenie.generator import smiles_to_selfies_safe, selfies_to_smiles_safe, screen_pains_and_sa_score

class TestGenerator(unittest.TestCase):
    def test_selfies_roundtrip(self):
        smiles = "CCO"
        selfies = smiles_to_selfies_safe(smiles)
        self.assertGreater(len(selfies), 0)
        reconstructed = selfies_to_smiles_safe(selfies)
        self.assertGreater(len(reconstructed), 0)

    def test_pains_detection(self):
        # Quinone toxicophore
        quinone_smiles = "O=C1C=CC(=O)C=C1"
        res = screen_pains_and_sa_score(quinone_smiles)
        self.assertIn("Quinone", res.pains_alerts)
        self.assertFalse(res.passed_filter)

if __name__ == "__main__":
    unittest.main()
