#!/usr/bin/env python3
"""
WZY T3 Element Visualization Script - Pure English Version
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.patches import Polygon
import json

def create_wzy_visualization():
    """Create WZY case visualization with pure English labels"""
    
    # Exact data extracted from STAPpp output
    nodes = {
        1: {"x": 0.0, "y": 0.0, "ux": 0.0, "uy": 0.0},
        2: {"x": 2.0, "y": 0.5, "ux": -3.87101e-07, "uy": -6.65683e-06},
        3: {"x": 2.0, "y": 1.0, "ux": 1.23482e-06, "uy": -7.04068e-06},
        4: {"x": 0.0, "y": 1.0, "ux": 0.0, "uy": 0.0}
    }
    
    elements = {
        1: {"nodes": [1, 2, 4], "sxx": -6.38078, "syy": -1.91423, "sxy": -38.4048},
        2: {"nodes": [2, 3, 4], "sxx": 12.7616, "syy": -19.2024, "sxy": -3.19039}
    }
    
    # Extract coordinates and displacements
    x = np.array([nodes[i]["x"] for i in range(1, 5)])
    y = np.array([nodes[i]["y"] for i in range(1, 5)])
    ux = np.array([nodes[i]["ux"] for i in range(1, 5)])
    uy = np.array([nodes[i]["uy"] for i in range(1, 5)])
    
    # Calculate deformed coordinates
    scale_factor = 1000000
    x_def = x + ux * scale_factor
    y_def = y + uy * scale_factor
    
    # Calculate displacement magnitude
    displacement_mag = np.sqrt(ux**2 + uy**2)
    
    # Triangulation
    triangles = np.array([[0, 1, 3], [1, 2, 3]])  # T3 elements
    triang = tri.Triangulation(x, y, triangles)
    triang_def = tri.Triangulation(x_def, y_def, triangles)
    
    # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('WZY Case T3 Element Analysis Results (Based on STAPpp Output)', 
                 fontsize=16, fontweight='bold')
    
    # Original mesh
    ax1 = axes[0, 0]
    ax1.triplot(triang, 'b-', linewidth=2)
    ax1.plot(x, y, 'bo', markersize=8)
    for i in range(4):
        ax1.text(x[i], y[i], f'  {i+1}', fontsize=12, ha='left')
    ax1.set_title('Original T3 Mesh', fontweight='bold')
    ax1.set_xlabel('X Coordinate (m)')
    ax1.set_ylabel('Y Coordinate (m)')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Deformation comparison
    ax2 = axes[0, 1]
    ax2.triplot(triang, 'b-', linewidth=2, alpha=0.7, label='Original')
    ax2.triplot(triang_def, 'r--', linewidth=2, alpha=0.7, label=f'Deformed x{scale_factor:g}')
    ax2.plot(x, y, 'bo', markersize=6)
    ax2.plot(x_def, y_def, 'ro', markersize=6)
    
    # Load arrows
    ax2.arrow(x[2], y[2], 0, -0.2, head_width=0.05, head_length=0.02, 
             fc='green', ec='green', linewidth=2)
    ax2.arrow(x[3], y[3], 0, -0.2, head_width=0.05, head_length=0.02, 
             fc='green', ec='green', linewidth=2)
    ax2.text(x[2]+0.1, y[2], '20N', fontsize=10, color='green', fontweight='bold')
    ax2.text(x[3]+0.1, y[3], '20N', fontsize=10, color='green', fontweight='bold')
    
    ax2.set_title('Mesh Deformation Comparison', fontweight='bold')
    ax2.set_xlabel('X Coordinate (m)')
    ax2.set_ylabel('Y Coordinate (m)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    # Displacement vectors
    ax3 = axes[0, 2]
    ax3.triplot(triang, 'k-', alpha=0.5)
    quiver = ax3.quiver(x, y, ux*scale_factor, uy*scale_factor, 
                       displacement_mag*1e6, scale=1, scale_units='xy', 
                       angles='xy', cmap='viridis', alpha=0.8, width=0.01)
    ax3.plot(x, y, 'ko', markersize=6)
    cbar3 = plt.colorbar(quiver, ax=ax3)
    cbar3.set_label('Displacement Magnitude (um)')
    ax3.set_title('Displacement Vector Field', fontweight='bold')
    ax3.set_xlabel('X Coordinate (m)')
    ax3.set_ylabel('Y Coordinate (m)')
    ax3.grid(True, alpha=0.3)
    ax3.set_aspect('equal')
    
    # X-displacement contour
    ax4 = axes[1, 0]
    contour4 = ax4.tricontourf(triang, ux*1e6, levels=20, cmap='RdBu_r')
    cbar4 = plt.colorbar(contour4, ax=ax4)
    cbar4.set_label('X-Displacement (um)')
    ax4.triplot(triang, 'k-', alpha=0.3)
    ax4.plot(x, y, 'ko', markersize=4)
    ax4.set_title('X-Direction Displacement', fontweight='bold')
    ax4.set_xlabel('X Coordinate (m)')
    ax4.set_ylabel('Y Coordinate (m)')
    ax4.set_aspect('equal')
    
    # Y-displacement contour
    ax5 = axes[1, 1]
    contour5 = ax5.tricontourf(triang, uy*1e6, levels=20, cmap='RdBu_r')
    cbar5 = plt.colorbar(contour5, ax=ax5)
    cbar5.set_label('Y-Displacement (um)')
    ax5.triplot(triang, 'k-', alpha=0.3)
    ax5.plot(x, y, 'ko', markersize=4)
    ax5.set_title('Y-Direction Displacement', fontweight='bold')
    ax5.set_xlabel('X Coordinate (m)')
    ax5.set_ylabel('Y Coordinate (m)')
    ax5.set_aspect('equal')
    
    # Stress distribution
    ax6 = axes[1, 2]
    # Calculate element centers
    elem_centers = []
    von_mises = []
    for elem_id, elem in elements.items():
        node_ids = elem["nodes"]
        cx = np.mean([nodes[nid]["x"] for nid in node_ids])
        cy = np.mean([nodes[nid]["y"] for nid in node_ids])
        elem_centers.append([cx, cy])
        
        # von Mises stress
        sxx, syy, sxy = elem["sxx"], elem["syy"], elem["sxy"]
        vm = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
        von_mises.append(vm)
    
    elem_centers = np.array(elem_centers)
    scatter = ax6.scatter(elem_centers[:, 0], elem_centers[:, 1], 
                         c=von_mises, s=300, cmap='jet', alpha=0.8)
    cbar6 = plt.colorbar(scatter, ax=ax6)
    cbar6.set_label('von Mises Stress (Pa)')
    ax6.triplot(triang, 'k-', alpha=0.5)
    ax6.plot(x, y, 'ko', markersize=6)
    
    # Label stress values
    for i, (center, vm) in enumerate(zip(elem_centers, von_mises)):
        ax6.text(center[0], center[1], f'{vm:.1f}', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
    
    ax6.set_title('von Mises Stress Distribution', fontweight='bold')
    ax6.set_xlabel('X Coordinate (m)')
    ax6.set_ylabel('Y Coordinate (m)')
    ax6.set_aspect('equal')
    
    plt.tight_layout()
    
    # Save figures
    plt.savefig('wzy_t3_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('wzy_t3_analysis.pdf', bbox_inches='tight')
    
    # Show figure
    plt.show()
    
    # Print data report
    print("\n" + "="*70)
    print("WZY Case T3 Element Analysis Report (Based on STAPpp Results)")
    print("="*70)
    
    print("\nNode Displacement Results:")
    print("Node    X-Disp(um)      Y-Disp(um)      Magnitude(um)")
    print("-" * 55)
    for i in range(1, 5):
        ux_um = nodes[i]['ux'] * 1e6
        uy_um = nodes[i]['uy'] * 1e6
        mag_um = np.sqrt(ux_um**2 + uy_um**2)
        print(f"{i:2d}    {ux_um:10.3f}    {uy_um:10.3f}    {mag_um:10.3f}")
    
    print("\nElement Stress Results:")
    print("Elem    Sxx(Pa)       Syy(Pa)       Sxy(Pa)       von Mises(Pa)")
    print("-" * 70)
    for elem_id, elem in elements.items():
        sxx, syy, sxy = elem["sxx"], elem["syy"], elem["sxy"]
        vm = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
        print(f"{elem_id:2d}    {sxx:10.2f}    {syy:10.2f}    {sxy:10.2f}    {vm:10.2f}")
    
    print("\nGeometry Information:")
    print("- Element Type: T3 Triangle")
    print("- Nodes: 4, Elements: 2")
    print("- Material: E=3e7 Pa, nu=0.3")
    print("- Boundary: Nodes 1,4 fixed")
    print("- Loading: 20N downward on nodes 3,4")
    print("="*70)

def create_stress_analysis():
    """Create detailed stress analysis visualization"""
    
    # Stress data from STAPpp
    elements = {
        1: {"nodes": [1, 2, 4], "sxx": -6.38078, "syy": -1.91423, "sxy": -38.4048},
        2: {"nodes": [2, 3, 4], "sxx": 12.7616, "syy": -19.2024, "sxy": -3.19039}
    }
    
    nodes = {
        1: {"x": 0.0, "y": 0.0},
        2: {"x": 2.0, "y": 0.5},
        3: {"x": 2.0, "y": 1.0},
        4: {"x": 0.0, "y": 1.0}
    }
    
    # Extract coordinates
    x = np.array([nodes[i]["x"] for i in range(1, 5)])
    y = np.array([nodes[i]["y"] for i in range(1, 5)])
    triangles = np.array([[0, 1, 3], [1, 2, 3]])
    triang = tri.Triangulation(x, y, triangles)
    
    # Calculate element centers and stress components
    elem_centers = []
    stress_xx = []
    stress_yy = []
    stress_xy = []
    von_mises = []
    
    for elem_id, elem in elements.items():
        node_ids = elem["nodes"]
        cx = np.mean([nodes[nid]["x"] for nid in node_ids])
        cy = np.mean([nodes[nid]["y"] for nid in node_ids])
        elem_centers.append([cx, cy])
        
        sxx, syy, sxy = elem["sxx"], elem["syy"], elem["sxy"]
        stress_xx.append(sxx)
        stress_yy.append(syy)
        stress_xy.append(sxy)
        
        # von Mises stress
        vm = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
        von_mises.append(vm)
    
    elem_centers = np.array(elem_centers)
    
    # Create stress analysis figure
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('WZY Case T3 Element Stress Analysis', fontsize=16, fontweight='bold')
    
    # Sxx stress
    ax1 = axes[0, 0]
    scatter1 = ax1.scatter(elem_centers[:, 0], elem_centers[:, 1], c=stress_xx, 
                          s=300, cmap='RdBu_r', alpha=0.8)
    ax1.triplot(triang, 'k-', alpha=0.5, linewidth=1)
    ax1.plot(x, y, 'ko', markersize=6)
    for i, (cx, cy, sxx) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], stress_xx)):
        ax1.text(cx, cy, f'{sxx:.1f}', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label('Sxx Stress (Pa)')
    ax1.set_title('Sxx Stress Distribution', fontweight='bold')
    ax1.set_xlabel('X Coordinate (m)')
    ax1.set_ylabel('Y Coordinate (m)')
    ax1.set_aspect('equal')
    
    # Syy stress
    ax2 = axes[0, 1]
    scatter2 = ax2.scatter(elem_centers[:, 0], elem_centers[:, 1], c=stress_yy, 
                          s=300, cmap='RdBu_r', alpha=0.8)
    ax2.triplot(triang, 'k-', alpha=0.5, linewidth=1)
    ax2.plot(x, y, 'ko', markersize=6)
    for i, (cx, cy, syy) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], stress_yy)):
        ax2.text(cx, cy, f'{syy:.1f}', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
    cbar2 = plt.colorbar(scatter2, ax=ax2)
    cbar2.set_label('Syy Stress (Pa)')
    ax2.set_title('Syy Stress Distribution', fontweight='bold')
    ax2.set_xlabel('X Coordinate (m)')
    ax2.set_ylabel('Y Coordinate (m)')
    ax2.set_aspect('equal')
    
    # Sxy stress
    ax3 = axes[1, 0]
    scatter3 = ax3.scatter(elem_centers[:, 0], elem_centers[:, 1], c=stress_xy, 
                          s=300, cmap='RdBu_r', alpha=0.8)
    ax3.triplot(triang, 'k-', alpha=0.5, linewidth=1)
    ax3.plot(x, y, 'ko', markersize=6)
    for i, (cx, cy, sxy) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], stress_xy)):
        ax3.text(cx, cy, f'{sxy:.1f}', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
    cbar3 = plt.colorbar(scatter3, ax=ax3)
    cbar3.set_label('Sxy Stress (Pa)')
    ax3.set_title('Sxy Stress Distribution', fontweight='bold')
    ax3.set_xlabel('X Coordinate (m)')
    ax3.set_ylabel('Y Coordinate (m)')
    ax3.set_aspect('equal')
    
    # von Mises stress
    ax4 = axes[1, 1]
    scatter4 = ax4.scatter(elem_centers[:, 0], elem_centers[:, 1], c=von_mises, 
                          s=300, cmap='jet', alpha=0.8)
    ax4.triplot(triang, 'k-', alpha=0.5, linewidth=1)
    ax4.plot(x, y, 'ko', markersize=6)
    for i, (cx, cy, vm) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], von_mises)):
        ax4.text(cx, cy, f'{vm:.1f}', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
    cbar4 = plt.colorbar(scatter4, ax=ax4)
    cbar4.set_label('von Mises Stress (Pa)')
    ax4.set_title('von Mises Stress Distribution', fontweight='bold')
    ax4.set_xlabel('X Coordinate (m)')
    ax4.set_ylabel('Y Coordinate (m)')
    ax4.set_aspect('equal')
    
    plt.tight_layout()
    
    # Save stress analysis
    plt.savefig('wzy_stress_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('wzy_stress_analysis.pdf', bbox_inches='tight')
    
    plt.show()

def main():
    """Main function to run all visualizations"""
    print("Creating WZY T3 Element Visualization...")
    
    # Create displacement visualization
    print("1. Generating displacement analysis...")
    create_wzy_visualization()
    
    # Create stress visualization
    print("2. Generating stress analysis...")
    create_stress_analysis()
    
    print("\nVisualization Complete!")
    print("Output files:")
    print("- wzy_t3_analysis.png/pdf")
    print("- wzy_stress_analysis.png/pdf")

if __name__ == "__main__":
    main()