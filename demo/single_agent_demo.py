"""
Minimal Demo: Single Agent Walking the Topology

This demo shows a single agent attempting various operations.
The PRIMARY EVIDENCE is the rejection logs, not the successes.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verifier import CognitiveSubstrateVerifier
import json


def run_demo():
    """Execute minimal demo with intentional violations"""
    
    print("="*70)
    print("COGNITIVE SUBSTRATE DEMO: Single Agent")
    print("="*70)
    print("\nLoading constitution...")
    
    verifier = CognitiveSubstrateVerifier('../cognitive_substrate.json')
    
    # Test cases: mix of valid and invalid proposals
    test_cases = [
        {
            'name': 'Valid LEAP Transition',
            'proposal': {
                'entropy': 2.1,
                'mode': 'LEAP',
                'source_citation': 'constraint_space.entropy_modes',
                'invents_new_theory': False,
                'optimizes_beyond_intent': False,
                'omits_constraints': False
            },
            'expected': 'PASS'
        },
        {
            'name': 'Valid AVE Transition',
            'proposal': {
                'entropy': 1.5,
                'mode': 'AVE',
                'source_citation': 'constraint_space.entropy_modes',
                'invents_new_theory': False,
                'optimizes_beyond_intent': False,
                'omits_constraints': False
            },
            'expected': 'PASS'
        },
        {
            'name': 'VIOLATION: Wrong Mode for Entropy',
            'proposal': {
                'entropy': 2.3,
                'mode': 'AVE',  # Should be LEAP
                'source_citation': 'test',
                'invents_new_theory': False,
                'optimizes_beyond_intent': False,
                'omits_constraints': False
            },
            'expected': 'REJECT'
        },
        {
            'name': 'VIOLATION: Theory Invention',
            'proposal': {
                'entropy': 1.8,
                'mode': 'AVE',
                'source_citation': 'new_theory.md',
                'invents_new_theory': True,  # Forbidden
                'optimizes_beyond_intent': False,
                'omits_constraints': False
            },
            'expected': 'REJECT'
        },
        {
            'name': 'VIOLATION: Commitment Window Too Short',
            'proposal': {
                'commitment_window': 1,  # Below optimal range [3,5]
                'source_citation': 'ethical_space.commitment_window',
                'invents_new_theory': False,
                'optimizes_beyond_intent': False,
                'omits_constraints': False
            },
            'expected': 'REJECT'
        },
        {
            'name': 'Valid Commitment Window',
            'proposal': {
                'commitment_window': 4,  # Within optimal range
                'source_citation': 'ethical_space.commitment_window',
                'invents_new_theory': False,
                'optimizes_beyond_intent': False,
                'omits_constraints': False
            },
            'expected': 'PASS'
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}/{len(test_cases)}: {test['name']}")
        print(f"{'='*70}")
        
        result = verifier.validate_proposal(test['proposal'])
        
        print(f"\nProposal: {json.dumps(test['proposal'], indent=2)}")
        print(f"\nExpected: {test['expected']}")
        print(f"Actual:   {result.status.value}")
        
        if result.violations:
            print(f"\n[!] VIOLATIONS:")
            for violation in result.violations:
                print(f"  - {violation}")
        
        if result.warnings:
            print(f"\n[!] WARNINGS:")
            for warning in result.warnings:
                print(f"  - {warning}")
        
        match = result.status.value == test['expected']
        print(f"\n{'[MATCH]' if match else '[MISMATCH]'}")
        
        results.append({
            'test': test['name'],
            'expected': test['expected'],
            'actual': result.status.value,
            'match': match,
            'violations': result.violations
        })
    
    # Summary
    print(f"\n{'='*70}")
    print("DEMO SUMMARY")
    print(f"{'='*70}")
    
    total = len(results)
    matches = sum(1 for r in results if r['match'])
    rejections = sum(1 for r in results if r['actual'] == 'REJECT')
    
    print(f"\nTotal tests: {total}")
    print(f"Matches: {matches}/{total}")
    print(f"Rejections: {rejections} (PRIMARY EVIDENCE)")
    
    print(f"\n{'='*70}")
    print("KEY INSIGHT")
    print(f"{'='*70}")
    print("\nThe system does NOT align behavior.")
    print("It defines where behavior is IMPOSSIBLE.")
    print("Agents merely walk the topology.")
    print("\nRejection logs prove the terrain is enforced mechanically,")
    print("without human judgment or interpretation.")
    print(f"{'='*70}")
    
    return results


if __name__ == "__main__":
    run_demo()
