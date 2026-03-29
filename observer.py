"""
Observer: Resource Topology Generator for Cognitive Substrate

This module implements the Observer role as defined in cognitive_substrate.json.
It reads the Composer's unified artifact and generates a topology graph showing:
- State nodes (admissible cognitive states)
- Transition edges (lawful transformations)
- Irreversible boundaries (hard reject zones)

The Observer does NOT:
- Interpret or add meaning
- Optimize or suggest improvements
- Modify Layer 0 (Constitution) or intervene in Layer 2 (exchanges)

The Observer DOES:
- Expose how existing works can be combined
- Expose irreversibility boundaries
- Expose dependency structure
- Generate machine-readable topology
"""

import json
from typing import Dict, Any, List, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import math


@dataclass
class StateNode:
    """A node in the cognitive state graph"""
    id: str
    space: str  # 'constraint', 'ethical', or 'perceptual'
    primitive: str  # Which theoretical primitive defines this state
    constraints: List[str]
    is_boundary: bool = False  # Is this an irreversible boundary?


@dataclass
class TransitionEdge:
    """An edge representing a lawful state transition"""
    from_node: str
    to_node: str
    transition_type: str  # 'reversible' or 'irreversible'
    required_conditions: List[str]
    verifier_rule: str  # Which Verifier rule governs this transition


@dataclass
class CognitiveTopology:
    """The complete topology graph"""
    nodes: Dict[str, StateNode]
    edges: List[TransitionEdge]
    irreversible_boundaries: Set[str]  # Node IDs that are boundaries
    space_partitions: Dict[str, List[str]]  # Space -> node IDs


class CognitiveSubstrateObserver:
    """
    Observer: Resource Topology Generator
    
    Role: Expose how existing works can be combined, irreversibility boundaries, dependency structure
    Input: Composer's unified artifact
    Output: Topology graph (machine-readable, AI-consumable)
    Constraint: Non-intervention - no modification of Layer 0, no interpretation
    """
    
    def __init__(self, constitution_path: str, artifact_path: str):
        """
        Initialize Observer with Constitution and Composer's artifact.
        
        Args:
            constitution_path: Path to cognitive_substrate.json
            artifact_path: Path to cognitive_artifact.json
        """
        # Load Constitution
        with open(constitution_path, 'r', encoding='utf-8') as f:
            self.constitution = json.load(f)['cognitive_substrate']
        
        # Load Composer's artifact
        with open(artifact_path, 'r', encoding='utf-8') as f:
            self.artifact = json.load(f)['cognitive_artifact']
        
        self.nodes: Dict[str, StateNode] = {}
        self.edges: List[TransitionEdge] = []
        self.irreversible_boundaries: Set[str] = set()
    
    def generate_topology(self) -> CognitiveTopology:
        """
        Generate the complete cognitive topology from the artifact.
        
        Returns:
            CognitiveTopology with nodes, edges, and boundaries
        """
        print("[Observer] Generating cognitive topology...")
        
        # Step 1: Generate state nodes from primitives
        self._generate_state_nodes()
        
        # Step 2: Generate transition edges based on dependencies and constraints
        self._generate_transition_edges()
        
        # Step 3: Identify irreversible boundaries
        self._identify_irreversible_boundaries()
        
        # Step 4: Partition nodes by theoretical space
        space_partitions = self._partition_by_space()
        
        topology = CognitiveTopology(
            nodes=self.nodes,
            edges=self.edges,
            irreversible_boundaries=self.irreversible_boundaries,
            space_partitions=space_partitions
        )
        
        print(f"[Observer] Topology generated:")
        print(f"  - {len(topology.nodes)} state nodes")
        print(f"  - {len(topology.edges)} transition edges")
        print(f"  - {len(topology.irreversible_boundaries)} irreversible boundaries")
        
        return topology
    
    def _generate_state_nodes(self) -> None:
        """Generate state nodes from theoretical primitives"""
        print("[Observer] Generating state nodes from primitives...")
        
        primitives = self.artifact['primitives']
        
        for name, primitive in primitives.items():
            # Each primitive defines a cognitive state
            node = StateNode(
                id=name,
                space=primitive['source_space'],
                primitive=name,
                constraints=primitive['constraints']
            )
            self.nodes[name] = node
        
        # Add special boundary nodes based on constraints
        # Example: K=1.8 threshold creates two boundary states (LEAP/AVE)
        if 'k_threshold' in self.constitution['constraint_space']:
            k_val = self.constitution['constraint_space']['k_threshold']
            
            # LEAP boundary (H > 1.8)
            leap_node = StateNode(
                id='LEAP_boundary',
                space='constraint',
                primitive='entropy_modes',
                constraints=[f'H > {k_val}'],
                is_boundary=True
            )
            self.nodes['LEAP_boundary'] = leap_node
            self.irreversible_boundaries.add('LEAP_boundary')
            
            # AVE boundary (H ≤ 1.8)
            ave_node = StateNode(
                id='AVE_boundary',
                space='constraint',
                primitive='entropy_modes',
                constraints=[f'H ≤ {k_val}'],
                is_boundary=True
            )
            self.nodes['AVE_boundary'] = ave_node
            self.irreversible_boundaries.add('AVE_boundary')
    
    def _generate_transition_edges(self) -> None:
        """Generate transition edges based on dependencies and integration rules"""
        print("[Observer] Generating transition edges...")
        
        integration_map = self.artifact['integration_map']
        
        # For each primitive, create edges to its dependencies
        for primitive, dependencies in integration_map.items():
            if primitive not in self.nodes:
                continue
            
            for dep in dependencies:
                if dep not in self.nodes:
                    # Dependency not in current artifact (e.g., k_threshold, entropy_modes)
                    # Create placeholder or skip
                    continue
                
                # Create edge: primitive depends on dep
                edge = TransitionEdge(
                    from_node=dep,
                    to_node=primitive,
                    transition_type='reversible',  # Default to reversible
                    required_conditions=[f'{primitive} requires {dep}'],
                    verifier_rule=f'integration_rules.{primitive}_coupling'
                )
                self.edges.append(edge)
        
        # Add edges for commitment window transitions (ethical space)
        if 'commitment_window' in self.nodes:
            # Transition from uncommitted to committed state
            commit_edge = TransitionEdge(
                from_node='commitment_window',
                to_node='commitment_window',
                transition_type='irreversible',  # Once committed, must wait k steps
                required_conditions=['k steps must elapse before value change'],
                verifier_rule='ethical_space.commitment_window.enforcement'
            )
            self.edges.append(commit_edge)
        
        # Add edges for entropy mode transitions (constraint space)
        if 'LEAP_boundary' in self.nodes and 'AVE_boundary' in self.nodes:
            # Transition from AVE to LEAP when entropy increases
            ave_to_leap = TransitionEdge(
                from_node='AVE_boundary',
                to_node='LEAP_boundary',
                transition_type='reversible',
                required_conditions=['H increases above 1.8'],
                verifier_rule='constraint_space.entropy_modes.LEAP.condition'
            )
            self.edges.append(ave_to_leap)
            
            # Transition from LEAP to AVE when entropy decreases
            leap_to_ave = TransitionEdge(
                from_node='LEAP_boundary',
                to_node='AVE_boundary',
                transition_type='reversible',
                required_conditions=['H decreases to ≤ 1.8'],
                verifier_rule='constraint_space.entropy_modes.AVE.condition'
            )
            self.edges.append(leap_to_ave)
    
    def _identify_irreversible_boundaries(self) -> None:
        """Identify nodes that represent irreversible boundaries"""
        print("[Observer] Identifying irreversible boundaries...")

        # Preserve nodes that were created as explicit constitutional boundaries.
        for node_id in self.irreversible_boundaries:
            if node_id in self.nodes:
                self.nodes[node_id].is_boundary = True

        # Mark nodes as irreversible boundaries based on constraints
        for node_id, node in self.nodes.items():
            # Check if any constraint mentions irreversibility
            for constraint in node.constraints:
                if 'irreversib' in constraint.lower():
                    self.irreversible_boundaries.add(node_id)
                    node.is_boundary = True
        
        # Mark edges as irreversible if they cross boundaries
        for edge in self.edges:
            if edge.to_node in self.irreversible_boundaries:
                edge.transition_type = 'irreversible'
    
    def _partition_by_space(self) -> Dict[str, List[str]]:
        """Partition nodes by their theoretical space"""
        partitions = {
            'constraint': [],
            'ethical': [],
            'perceptual': []
        }
        
        for node_id, node in self.nodes.items():
            partitions[node.space].append(node_id)
        
        return partitions
    
    def export_topology(self, topology: CognitiveTopology, output_path: str) -> None:
        """
        Export topology to JSON format.
        
        Args:
            topology: The generated topology
            output_path: Where to save the topology
        """
        output = {
            'cognitive_topology': {
                'version': '1.0.0',
                'generated_by': 'Observer (Resource Topology Generator)',
                'source_artifact': 'cognitive_artifact.json',
                
                'nodes': {
                    node_id: {
                        'space': node.space,
                        'primitive': node.primitive,
                        'constraints': node.constraints,
                        'is_boundary': node.is_boundary
                    }
                    for node_id, node in topology.nodes.items()
                },
                
                'edges': [
                    {
                        'from': edge.from_node,
                        'to': edge.to_node,
                        'type': edge.transition_type,
                        'conditions': edge.required_conditions,
                        'verifier_rule': edge.verifier_rule
                    }
                    for edge in topology.edges
                ],
                
                'irreversible_boundaries': list(topology.irreversible_boundaries),
                
                'space_partitions': topology.space_partitions,
                
                'interpretation': {
                    'note': 'This topology is AI-consumable terrain, not human narrative',
                    'usage': 'Nodes = admissible states, Edges = lawful transitions, Boundaries = hard reject zones',
                    'non_intervention_clause': 'Observer did not modify Layer 0 or interpret meaning'
                }
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"[Observer] Topology exported to {output_path}")
    
    def generate_svg_visualization(self, topology: CognitiveTopology, output_path: str) -> None:
        """
        Generate SVG visualization of the topology.
        
        Args:
            topology: The topology to visualize
            output_path: Where to save the SVG
        """
        print("[Observer] Generating SVG visualization...")
        
        # Simple force-directed layout
        width, height = 800, 600
        
        # Partition nodes by space for layout
        partitions = topology.space_partitions
        
        # Calculate positions
        positions = {}
        y_offset = height / 4
        
        for i, (space, node_ids) in enumerate(partitions.items()):
            x_base = (i + 1) * width / 4
            for j, node_id in enumerate(node_ids):
                y = y_offset + (j * 80)
                positions[node_id] = (x_base, y)
        
        # Generate SVG
        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            '<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
            '<polygon points="0 0, 10 3.5, 0 7" fill="#666" />',
            '</marker>',
            '</defs>',
            '<rect width="100%" height="100%" fill="#0a0a0a"/>',
        ]
        
        # Draw edges
        for edge in topology.edges:
            if edge.from_node in positions and edge.to_node in positions:
                x1, y1 = positions[edge.from_node]
                x2, y2 = positions[edge.to_node]
                
                color = '#ff4444' if edge.transition_type == 'irreversible' else '#666'
                stroke_width = 2 if edge.transition_type == 'irreversible' else 1
                
                svg_lines.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{color}" stroke-width="{stroke_width}" marker-end="url(#arrowhead)"/>'
                )
        
        # Draw nodes
        for node_id, node in topology.nodes.items():
            if node_id not in positions:
                continue
            
            x, y = positions[node_id]
            
            # Color by space
            colors = {
                'constraint': '#c5a059',
                'ethical': '#4a9eff',
                'perceptual': '#ff4a9e'
            }
            fill = colors.get(node.space, '#666')
            
            # Boundary nodes are larger
            radius = 25 if node.is_boundary else 15
            
            svg_lines.append(
                f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="#fff" stroke-width="2"/>'
            )
            svg_lines.append(
                f'<text x="{x}" y="{y + 40}" text-anchor="middle" fill="#fff" font-size="12">{node_id}</text>'
            )
        
        # Add legend
        legend_y = height - 100
        svg_lines.extend([
            f'<text x="20" y="{legend_y}" fill="#c5a059" font-size="14">■ Constraint Space</text>',
            f'<text x="20" y="{legend_y + 20}" fill="#4a9eff" font-size="14">■ Ethical Space</text>',
            f'<text x="20" y="{legend_y + 40}" fill="#ff4a9e" font-size="14">■ Perceptual Space</text>',
            f'<text x="20" y="{legend_y + 60}" fill="#ff4444" font-size="14">━ Irreversible Boundary</text>',
        ])
        
        svg_lines.append('</svg>')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg_lines))
        
        print(f"[Observer] SVG visualization exported to {output_path}")


# Example usage
if __name__ == "__main__":
    # Initialize Observer
    observer = CognitiveSubstrateObserver(
        constitution_path='cognitive_substrate.json',
        artifact_path='cognitive_artifact.json'
    )
    
    # Generate topology
    topology = observer.generate_topology()
    
    # Export topology
    observer.export_topology(topology, 'cognitive_topology.json')
    
    # Generate SVG visualization
    observer.generate_svg_visualization(topology, 'cognitive_topology.svg')
    
    print("\n[Observer] Topology generation complete.")
    print("[Observer] Non-intervention clause: No Layer 0 modification, no interpretation added.")
