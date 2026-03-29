"""
Integration tests for the checked-in cognitive substrate artifact.
"""

import json
import tempfile
import unittest
from pathlib import Path

from composer import CognitiveSubstrateComposer
from observer import CognitiveSubstrateObserver
from verifier import CognitiveSubstrateVerifier, ValidationStatus


REPO_ROOT = Path(__file__).resolve().parent
CONSTITUTION_PATH = REPO_ROOT / "cognitive_substrate.json"
ARTIFACT_PATH = REPO_ROOT / "cognitive_artifact.json"


class IntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = CognitiveSubstrateVerifier(str(CONSTITUTION_PATH))
        with ARTIFACT_PATH.open("r", encoding="utf-8") as handle:
            self.artifact = json.load(handle)["cognitive_artifact"]

    def test_checked_in_artifact_has_traceable_primitives(self) -> None:
        primitives = self.artifact["primitives"]
        self.assertGreaterEqual(len(primitives), 3)
        for primitive in primitives.values():
            self.assertIn("source_file", primitive)
            self.assertTrue(primitive["source_file"])

    def test_checked_in_artifact_preserves_nonzero_invariants(self) -> None:
        invariants = self.artifact["invariants"]
        self.assertGreater(len(invariants), 0)

    def test_integration_map_keeps_expected_dependency(self) -> None:
        integration_map = self.artifact["integration_map"]
        self.assertIn("pulse_layer", integration_map)
        self.assertIn("k_threshold", integration_map["pulse_layer"])

    def test_verifier_accepts_known_good_proposal(self) -> None:
        proposal = {
            "entropy": 2.0,
            "mode": "LEAP",
            "commitment_window": 4,
            "value_protection": 0.25,
            "source_citation": "cognitive_artifact.json - commitment_window primitive",
            "invents_new_theory": False,
            "optimizes_beyond_intent": False,
            "omits_constraints": False,
        }
        result = self.verifier.validate_proposal(proposal)
        self.assertEqual(result.status, ValidationStatus.PASS)
        self.assertEqual(result.violations, [])

    def test_composer_refuses_missing_corpus_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_root = Path(temp_dir)
            with self.assertRaises(FileNotFoundError):
                CognitiveSubstrateComposer(
                    constitution_path=str(CONSTITUTION_PATH),
                    corpus_root=str(empty_root),
                )

    def test_observer_generates_consistent_topology(self) -> None:
        observer = CognitiveSubstrateObserver(
            str(CONSTITUTION_PATH),
            str(ARTIFACT_PATH),
        )
        topology = observer.generate_topology()

        self.assertIn("LEAP_boundary", topology.nodes)
        self.assertIn("AVE_boundary", topology.nodes)
        self.assertIn("LEAP_boundary", topology.irreversible_boundaries)
        self.assertIn("AVE_boundary", topology.irreversible_boundaries)
        self.assertGreaterEqual(len(topology.edges), 3)

    def test_observer_exports_json_and_svg(self) -> None:
        observer = CognitiveSubstrateObserver(
            str(CONSTITUTION_PATH),
            str(ARTIFACT_PATH),
        )
        topology = observer.generate_topology()

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            json_path = output_dir / "topology.json"
            svg_path = output_dir / "topology.svg"
            observer.export_topology(topology, str(json_path))
            observer.generate_svg_visualization(topology, str(svg_path))

            exported = json.loads(json_path.read_text(encoding="utf-8"))["cognitive_topology"]
            self.assertIn("LEAP_boundary", exported["irreversible_boundaries"])
            self.assertIn("AVE_boundary", exported["irreversible_boundaries"])
            svg_content = svg_path.read_text(encoding="utf-8")
            self.assertIn("<svg", svg_content)
            self.assertIn("LEAP_boundary", svg_content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
