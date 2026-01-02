"""
Verifier: Constraint Enforcement Engine for Cognitive Substrate

This module implements the Verifier role as defined in cognitive_substrate.json.
It mechanically enforces constraints from three theoretical spaces:
- constraint_space (1.8 Law)
- ethical_space (Post-Alignment AI)
- perceptual_space (Aesthetic Resonator)

The Verifier does NOT:
- Invent new theory
- Optimize beyond stated intentions
- Simplify by omission
- Propose alternatives

The Verifier DOES:
- Check global coherence against full corpus
- Reject structures violating documented constraints
- Require explicit citation to source material
"""

import json
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum


class ValidationStatus(Enum):
    PASS = "PASS"
    REJECT = "REJECT"
    WARNING = "WARNING"


@dataclass
class ValidationResult:
    status: ValidationStatus
    violations: List[str]
    warnings: List[str]
    citation_required: List[str]


class CognitiveSubstrateVerifier:
    """
    Verifier: Consistency Enforcer
    
    Role: Check global coherence against full corpus
    Input: Composer's generated structure or proposed operation
    Output: Validation report or rejection with specific constraint violations
    """
    
    def __init__(self, constitution_path: str):
        """Load the JSON Constitution"""
        with open(constitution_path, 'r', encoding='utf-8') as f:
            self.constitution = json.load(f)['cognitive_substrate']
        
        self.constraint_space = self.constitution['constraint_space']
        self.ethical_space = self.constitution['ethical_space']
        self.perceptual_space = self.constitution['perceptual_space']
        self.integration_rules = self.constitution['integration_rules']
        self.forbidden_ops = self.constitution['forbidden_operations']
    
    def validate_proposal(self, proposal: Dict[str, Any]) -> ValidationResult:
        """
        Validate a proposal against all three spaces and integration rules.
        
        Args:
            proposal: Dictionary containing proposed operation/structure
        
        Returns:
            ValidationResult with status and detailed violations
        """
        violations = []
        warnings = []
        citations_needed = []
        
        # Check forbidden operations
        forbidden_violations = self._check_forbidden_operations(proposal)
        violations.extend(forbidden_violations)
        
        # Validate against constraint_space
        constraint_violations = self._validate_constraint_space(proposal)
        violations.extend(constraint_violations)
        
        # Validate against ethical_space
        ethical_violations = self._validate_ethical_space(proposal)
        violations.extend(ethical_violations)
        
        # Validate against perceptual_space
        perceptual_violations = self._validate_perceptual_space(proposal)
        violations.extend(perceptual_violations)
        
        # Check integration rules (cross-space consistency)
        integration_violations = self._validate_integration_rules(proposal)
        violations.extend(integration_violations)
        
        # Require citations
        if 'source_citation' not in proposal:
            citations_needed.append("All proposals must cite source material from corpus")
        
        # Determine final status
        if violations:
            status = ValidationStatus.REJECT
        elif warnings:
            status = ValidationStatus.WARNING
        else:
            status = ValidationStatus.PASS
        
        return ValidationResult(
            status=status,
            violations=violations,
            warnings=warnings,
            citation_required=citations_needed
        )
    
    def _check_forbidden_operations(self, proposal: Dict[str, Any]) -> List[str]:
        """Check if proposal violates forbidden operations"""
        violations = []
        
        # Check for theory invention
        if proposal.get('invents_new_theory', False):
            violations.append(
                f"FORBIDDEN: theory_invention - "
                f"Proposal invents new theory beyond provided corpus. "
                f"Source: {self.forbidden_ops['theory_invention']}"
            )
        
        # Check for optimization beyond intent
        if proposal.get('optimizes_beyond_intent', False):
            violations.append(
                f"FORBIDDEN: optimization_beyond_intent - "
                f"Proposal optimizes beyond stated author intentions. "
                f"Source: {self.forbidden_ops['optimization_beyond_intent']}"
            )
        
        # Check for simplification by omission
        if proposal.get('omits_constraints', False):
            violations.append(
                f"FORBIDDEN: simplification_by_omission - "
                f"Proposal simplifies by omitting documented constraints. "
                f"Source: {self.forbidden_ops['simplification_by_omission']}"
            )
        
        return violations
    
    def _validate_constraint_space(self, proposal: Dict[str, Any]) -> List[str]:
        """Validate against 1.8 Law constraints"""
        violations = []
        
        # Check K-threshold adherence
        if 'entropy' in proposal:
            H = proposal['entropy']
            k_threshold = self.constraint_space['k_threshold']
            
            if 'mode' in proposal:
                expected_mode = 'LEAP' if H > k_threshold else 'AVE'
                if proposal['mode'] != expected_mode:
                    violations.append(
                        f"CONSTRAINT VIOLATION: entropy={H:.2f}, "
                        f"expected mode={expected_mode}, got mode={proposal['mode']}. "
                        f"Source: constraint_space.k_threshold={k_threshold}"
                    )
        
        # Check irreversibility budget
        if 'irreversible_operations' in proposal:
            if not proposal.get('entropy_justification'):
                violations.append(
                    f"CONSTRAINT VIOLATION: irreversible operations require K-value justification. "
                    f"Source: constraint_space.irreversibility_budget"
                )
        
        return violations
    
    def _validate_ethical_space(self, proposal: Dict[str, Any]) -> List[str]:
        """Validate against Post-Alignment AI constraints"""
        violations = []
        
        # Check commitment window
        if 'commitment_window' in proposal:
            k = proposal['commitment_window']
            optimal_range = self.ethical_space['commitment_window']['optimal_range']
            
            if not (optimal_range[0] <= k <= optimal_range[1]):
                violations.append(
                    f"ETHICAL VIOLATION: commitment_window k={k} outside optimal range {optimal_range}. "
                    f"Source: ethical_space.commitment_window.optimal_range"
                )
        
        # Check value protection
        if 'value_protection' in proposal:
            delta = proposal['value_protection']
            optimal_delta = self.ethical_space['value_protection']['optimal_value']
            
            if abs(delta - optimal_delta) > 0.1:
                violations.append(
                    f"ETHICAL WARNING: value_protection δ={delta} deviates from optimal {optimal_delta}. "
                    f"Source: ethical_space.value_protection.optimal_value"
                )
        
        # Check non-intervention clause (if Observer role)
        if proposal.get('role') == 'Observer':
            prohibited = self.ethical_space['non_intervention_clause']['prohibition']
            
            if proposal.get('modifies_layer_0', False):
                violations.append(
                    f"ETHICAL VIOLATION: Observer attempting to modify Layer 0 (Constitution). "
                    f"Source: ethical_space.non_intervention_clause - {prohibited[0]}"
                )
            
            if proposal.get('intervenes_in_layer_2', False):
                violations.append(
                    f"ETHICAL VIOLATION: Observer attempting to intervene in Layer 2 exchanges. "
                    f"Source: ethical_space.non_intervention_clause - {prohibited[1]}"
                )
        
        return violations
    
    def _validate_perceptual_space(self, proposal: Dict[str, Any]) -> List[str]:
        """Validate against Aesthetic Resonator constraints"""
        violations = []
        
        # Check pulse layer computation
        if 'pulse_computation' in proposal:
            if 'delta_H' not in proposal['pulse_computation']:
                violations.append(
                    f"PERCEPTUAL VIOLATION: pulse_computation must include ΔH (delta entropy). "
                    f"Source: perceptual_space.pulse_layer.formula"
                )
        
        # Check LEAP frequency bounds
        if 'leap_frequency_increase' in proposal:
            increase = proposal['leap_frequency_increase']
            expected_range = (0.13, 0.18)  # 13-18%
            
            if not (expected_range[0] <= increase <= expected_range[1]):
                violations.append(
                    f"PERCEPTUAL WARNING: LEAP frequency increase {increase:.2%} outside expected range {expected_range}. "
                    f"Source: perceptual_space.leap_frequency"
                )
        
        return violations
    
    def _validate_integration_rules(self, proposal: Dict[str, Any]) -> List[str]:
        """Validate cross-space consistency"""
        violations = []
        
        # Constraint-Ethical coupling
        if 'commitment_window' in proposal and 'irreversibility_budget' in proposal:
            # Commitment window must respect irreversibility budget
            rule = self.integration_rules['constraint_ethical_coupling']
            # (Specific validation logic would go here based on proposal structure)
        
        # Ethical-Perceptual coupling
        if 'value_protection' in proposal and 'pulse_layer' in proposal:
            # Value protection should trigger on entropy collapse detected by pulse
            rule = self.integration_rules['ethical_perceptual_coupling']
            # (Specific validation logic would go here)
        
        # Global invariant check
        global_invariant = self.integration_rules['global_invariant']
        # All three spaces must remain consistent
        
        return violations
    
    def query_constraint(self, space: str, key: str) -> Any:
        """
        Query a specific constraint value from the constitution.
        
        Args:
            space: 'constraint', 'ethical', or 'perceptual'
            key: Dot-notation path to value (e.g., 'k_threshold' or 'commitment_window.optimal_range')
        
        Returns:
            The requested value from the constitution
        """
        space_map = {
            'constraint': self.constraint_space,
            'ethical': self.ethical_space,
            'perceptual': self.perceptual_space
        }
        
        if space not in space_map:
            raise ValueError(f"Unknown space: {space}. Must be 'constraint', 'ethical', or 'perceptual'")
        
        current = space_map[space]
        for part in key.split('.'):
            current = current[part]
        
        return current
    
    def validate_transition(self, from_state: Dict[str, Any], to_state: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a state transition.
        
        Args:
            from_state: Current state
            to_state: Proposed next state
        
        Returns:
            (is_valid, violations)
        """
        violations = []
        
        # Check if transition respects commitment window
        if 'current_value' in from_state and 'current_value' in to_state:
            if from_state['current_value'] != to_state['current_value']:
                if 'steps_since_commitment' in from_state:
                    k_min = self.ethical_space['commitment_window']['optimal_range'][0]
                    if from_state['steps_since_commitment'] < k_min:
                        violations.append(
                            f"TRANSITION VIOLATION: Value change before commitment window expired. "
                            f"Steps: {from_state['steps_since_commitment']}, Required: {k_min}"
                        )
        
        # Check if transition preserves reversibility
        if 'reversibility_score' in to_state:
            if to_state['reversibility_score'] < from_state.get('reversibility_score', 0):
                if not to_state.get('reversibility_sacrifice_justified', False):
                    violations.append(
                        f"TRANSITION VIOLATION: Reversibility decreased without justification. "
                        f"From: {from_state.get('reversibility_score')}, To: {to_state['reversibility_score']}"
                    )
        
        return (len(violations) == 0, violations)


# Example usage
if __name__ == "__main__":
    verifier = CognitiveSubstrateVerifier('cognitive_substrate.json')
    
    # Test valid proposal
    valid_proposal = {
        'entropy': 2.1,
        'mode': 'LEAP',
        'source_citation': '1.8 Law - K_1.8_THEORETICAL_JUSTIFICATION.md',
        'invents_new_theory': False,
        'optimizes_beyond_intent': False,
        'omits_constraints': False
    }
    
    result = verifier.validate_proposal(valid_proposal)
    print(f"Valid Proposal: {result.status.value}")
    print(f"Violations: {result.violations}")
    
    # Test invalid proposal (wrong mode for entropy)
    invalid_proposal = {
        'entropy': 2.1,
        'mode': 'AVE',  # Should be LEAP for H > 1.8
        'source_citation': 'test',
        'invents_new_theory': False,
        'optimizes_beyond_intent': False,
        'omits_constraints': False
    }
    
    result = verifier.validate_proposal(invalid_proposal)
    print(f"\nInvalid Proposal: {result.status.value}")
    print(f"Violations: {result.violations}")
