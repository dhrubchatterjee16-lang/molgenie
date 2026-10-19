"""
Tests for Retrosynthetic Route & Commercial Catalog Accessibility
"""

import unittest
from molgenie.retrosynthesis import RetrosynthesisEngine

class TestRetrosynthesis(unittest.TestCase):
    def test_accessible_molecule(self):
        # Aspirin is readily accessible in <= 4 steps from commercial building blocks
        aspirin = "CC(=O)Oc1ccccc1C(=O)O"
        engine = RetrosynthesisEngine()
        res = engine.audit_molecule(aspirin)
        self.assertTrue(res.is_synthetically_accessible)
        self.assertLessEqual(res.estimated_step_count, 4)
        self.assertFalse(res.has_unphysical_motifs)
        self.assertGreater(res.commercial_feasibility_pct, 50.0)

    def test_unphysical_motif_rejection(self):
        # Peroxide train (molecular graffiti)
        graffiti = "CCOOCC(=O)O"
        engine = RetrosynthesisEngine()
        res = engine.audit_molecule(graffiti)
        self.assertTrue(res.has_unphysical_motifs)
        self.assertFalse(res.is_synthetically_accessible)

if __name__ == "__main__":
    unittest.main()
