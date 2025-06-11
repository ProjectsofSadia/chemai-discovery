"""
Advanced Molecular Visualization Components
Professional 3D molecular rendering and property visualization
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional
import json

class MolecularVisualizer:
    """Advanced 3D molecular visualization with professional rendering"""
    
    def __init__(self):
        self.default_colors = {
            'C': '#909090',  # Carbon - gray
            'N': '#3050F8',  # Nitrogen - blue
            'O': '#FF0D0D',  # Oxygen - red
            'H': '#FFFFFF',  # Hydrogen - white
            'S': '#FFFF30',  # Sulfur - yellow
            'P': '#FF8000',  # Phosphorus - orange
            'F': '#90E050',  # Fluorine - green
            'Cl': '#1FF01F', # Chlorine - green
            'Br': '#A62929', # Bromine - brown
            'I': '#940094'   # Iodine - purple
        }
    
    def create_3d_molecule(self, smiles: str, properties: Dict[str, Any] = None) -> go.Figure:
        """Create professional 3D molecular visualization"""
        
        # Generate 3D coordinates (simplified - in production use RDKit)
        coords, atoms, bonds = self._generate_3d_structure(smiles)
        
        fig = go.Figure()
        
        # Add atoms as spheres
        for i, (coord, atom_type) in enumerate(zip(coords, atoms)):
            fig.add_trace(go.Scatter3d(
                x=[coord[0]],
                y=[coord[1]],
                z=[coord[2]],
                mode='markers',
                marker=dict(
                    size=self._get_atomic_radius(atom_type) * 20,
                    color=self.default_colors.get(atom_type, '#808080'),
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                text=f"{atom_type}{i+1}",
                name=f"{atom_type} atoms",
                showlegend=False,
                hovertemplate=f"<b>{atom_type}</b><br>Position: (%{{x:.2f}}, %{{y:.2f}}, %{{z:.2f}})<extra></extra>"
            ))
        
        # Add bonds as lines
        for bond in bonds:
            atom1, atom2 = bond
            coord1, coord2 = coords[atom1], coords[atom2]
            
            fig.add_trace(go.Scatter3d(
                x=[coord1[0], coord2[0]],
                y=[coord1[1], coord2[1]],
                z=[coord1[2], coord2[2]],
                mode='lines',
                line=dict(color='gray', width=8),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Professional layout
        fig.update_layout(
            title=dict(
                text=f"3D Molecular Structure: {smiles}",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                bgcolor='rgba(0,0,0,0)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=50, b=0),
            width=800,
            height=600
        )
        
        return fig
    
    def create_property_radar(self, properties: Dict[str, Any]) -> go.Figure:
        """Create radar chart for molecular properties"""
        
        # Normalize properties for radar chart
        normalized_props = self._normalize_properties(properties)
        
        categories = list(normalized_props.keys())
        values = list(normalized_props.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Molecular Properties',
            line=dict(color='rgb(79, 172, 254)', width=3),
            fillcolor='rgba(79, 172, 254, 0.3)',
            marker=dict(size=8, color='rgb(79, 172, 254)')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color='white'),
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                angularaxis=dict(
                    tickfont=dict(color='white', size=12),
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            title=dict(
                text="Molecular Property Profile",
                x=0.5,
                font=dict(size=18, color='white')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            width=500,
            height=500
        )
        
        return fig
    
    def create_property_comparison(self, molecules: List[Dict]) -> go.Figure:
        """Create comparison chart for multiple molecules"""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Solubility', 'Toxicity', 'Bioavailability', 'Drug-likeness'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        properties = ['solubility', 'toxicity', 'bioavailability', 'drug_likeness']
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        colors = ['#4facfe', '#f5576c', '#43e97b', '#fa709a']
        
        for i, prop in enumerate(properties):
            row, col = positions[i]
            
            names = [mol['name'] for mol in molecules]
            values = [mol['predicted_properties'].get(prop, 0) for mol in molecules]
            
            fig.add_trace(
                go.Bar(
                    x=names,
                    y=values,
                    name=prop.replace('_', ' ').title(),
                    marker_color=colors[i],
                    showlegend=False
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            title=dict(
                text="Molecular Property Comparison",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600
        )
        
        return fig
    
    def _generate_3d_structure(self, smiles: str):
        """Generate 3D coordinates for molecular structure"""
        # Simplified 3D structure generation
        # In production, use RDKit for accurate 3D coordinates
        
        np.random.seed(hash(smiles) % 2**32)
        
        # Estimate number of atoms from SMILES
        num_atoms = len([c for c in smiles if c.isupper() or c in 'cnos'])
        
        # Generate random 3D coordinates
        coords = np.random.uniform(-5, 5, (num_atoms, 3))
        
        # Generate atom types
        atoms = []
        for char in smiles:
            if char.isupper():
                atoms.append(char)
            elif char in 'cnos':
                atoms.append(char.upper())
        
        # Pad with carbon if needed
        while len(atoms) < num_atoms:
            atoms.append('C')
        atoms = atoms[:num_atoms]
        
        # Generate bonds (simplified)
        bonds = []
        for i in range(num_atoms - 1):
            bonds.append((i, i + 1))
        
        # Add some random bonds for rings
        if '1' in smiles or 'c' in smiles:
            for _ in range(min(3, num_atoms // 3)):
                i, j = np.random.choice(num_atoms, 2, replace=False)
                if (i, j) not in bonds and (j, i) not in bonds:
                    bonds.append((i, j))
        
        return coords, atoms, bonds
    
    def _get_atomic_radius(self, atom_type: str) -> float:
        """Get atomic radius for visualization"""
        radii = {
            'H': 0.31, 'C': 0.76, 'N': 0.71, 'O': 0.66,
            'F': 0.57, 'P': 1.07, 'S': 1.05, 'Cl': 1.02,
            'Br': 1.20, 'I': 1.39
        }
        return radii.get(atom_type, 0.8)
    
    def _normalize_properties(self, properties: Dict[str, Any]) -> Dict[str, float]:
        """Normalize properties for radar chart (0-100 scale)"""
        normalized = {}
        
        for prop_name, prop_data in properties.items():
            if isinstance(prop_data, dict) and 'value' in prop_data:
                value = prop_data['value']
                confidence = prop_data.get('confidence', 1.0)
                
                # Normalize based on property type
                if prop_name == 'solubility':
                    # LogS: -8 to 1 -> 0 to 100
                    norm_value = max(0, min(100, (value + 8) / 9 * 100))
                elif prop_name == 'toxicity':
                    # 0 to 1 -> 100 to 0 (lower toxicity is better)
                    norm_value = max(0, min(100, (1 - value) * 100))
                elif prop_name == 'bioavailability':
                    # 0 to 100 -> 0 to 100
                    norm_value = max(0, min(100, value))
                elif prop_name == 'drug_likeness':
                    # 0 to 1 -> 0 to 100
                    norm_value = max(0, min(100, value * 100))
                elif prop_name == 'binding_affinity':
                    # 3 to 12 -> 0 to 100
                    norm_value = max(0, min(100, (value - 3) / 9 * 100))
                else:
                    norm_value = 50  # Default to middle
                
                # Apply confidence weighting
                normalized[prop_name.replace('_', ' ').title()] = norm_value * confidence
        
        return normalized

class PropertyTrendAnalyzer:
    """Analyze and visualize property trends across molecular series"""
    
    def __init__(self):
        self.trend_data = {}
    
    def analyze_sar_trends(self, molecules: List[Dict], property_name: str) -> go.Figure:
        """Structure-Activity Relationship trend analysis"""
        
        # Extract molecular weights and target property
        mol_weights = []
        property_values = []
        names = []
        
        for mol in molecules:
            # Estimate molecular weight from SMILES length (simplified)
            mw = len(mol['smiles']) * 12
            mol_weights.append(mw)
            
            prop_val = mol['predicted_properties'].get(property_name, 0)
            if isinstance(prop_val, dict):
                prop_val = prop_val.get('value', 0)
            property_values.append(prop_val)
            names.append(mol['name'])
        
        # Create scatter plot with trend line
        fig = go.Figure()
        
        # Add scatter points
        fig.add_trace(go.Scatter(
            x=mol_weights,
            y=property_values,
            mode='markers+text',
            text=names,
            textposition='top center',
            marker=dict(
                size=12,
                color=property_values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title=property_name.replace('_', ' ').title())
            ),
            name='Molecules',
            hovertemplate='<b>%{text}</b><br>MW: %{x:.0f}<br>' + 
                         f'{property_name}: %{{y:.2f}}<extra></extra>'
        ))
        
        # Add trend line
        if len(mol_weights) > 1:
            z = np.polyfit(mol_weights, property_values, 1)
            trend_line = np.poly1d(z)
            x_trend = np.linspace(min(mol_weights), max(mol_weights), 100)
            y_trend = trend_line(x_trend)
            
            fig.add_trace(go.Scatter(
                x=x_trend,
                y=y_trend,
                mode='lines',
                name='Trend',
                line=dict(color='red', dash='dash', width=2),
                hoverinfo='skip'
            ))
        
        fig.update_layout(
            title=f'SAR Analysis: {property_name.replace("_", " ").title()} vs Molecular Weight',
            xaxis_title='Molecular Weight (Da)',
            yaxis_title=property_name.replace('_', ' ').title(),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            width=800,
            height=500
        )
        
        return fig
    
    def create_optimization_landscape(self, molecules: List[Dict]) -> go.Figure:
        """Create 3D optimization landscape"""
        
        # Extract three key properties for 3D visualization
        solubility = []
        bioavailability = []
        drug_likeness = []
        names = []
        
        for mol in molecules:
            props = mol['predicted_properties']
            
            sol = props.get('solubility', {})
            if isinstance(sol, dict):
                sol = sol.get('value', -3)
            solubility.append(sol)
            
            bio = props.get('bioavailability', {})
            if isinstance(bio, dict):
                bio = bio.get('value', 50)
            bioavailability.append(bio)
            
            drug = props.get('drug_likeness', {})
            if isinstance(drug, dict):
                drug = drug.get('value', 0.5)
            drug_likeness.append(drug)
            
            names.append(mol['name'])
        
        fig = go.Figure(data=go.Scatter3d(
            x=solubility,
            y=bioavailability,
            z=drug_likeness,
            mode='markers+text',
            text=names,
            marker=dict(
                size=8,
                color=drug_likeness,
                colorscale='RdYlBu',
                showscale=True,
                colorbar=dict(title='Drug-likeness'),
                opacity=0.8
            ),
            hovertemplate='<b>%{text}</b><br>' +
                         'Solubility: %{x:.2f}<br>' +
                         'Bioavailability: %{y:.1f}%<br>' +
                         'Drug-likeness: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='3D Optimization Landscape',
            scene=dict(
                xaxis_title='Solubility (LogS)',
                yaxis_title='Bioavailability (%)',
                zaxis_title='Drug-likeness',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            width=800,
            height=600
        )
        
        return fig

# Export functions for easy use
def create_molecule_3d(smiles: str, properties: Dict = None):
    """Quick function to create 3D molecule visualization"""
    viz = MolecularVisualizer()
    return viz.create_3d_molecule(smiles, properties)

def create_property_radar(properties: Dict):
    """Quick function to create property radar chart"""
    viz = MolecularVisualizer()
    return viz.create_property_radar(properties)

def analyze_molecular_trends(molecules: List[Dict], property_name: str):
    """Quick function to analyze molecular trends"""
    analyzer = PropertyTrendAnalyzer()
    return analyzer.analyze_sar_trends(molecules, property_name)
