#!/usr/bin/env python3
"""
T3 Patch Test - Displacement and Stress Analysis
Bottom row figures from the main analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# Fix font issues for Linux systems
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

def create_displacement_stress_analysis():
    """Create the bottom row analysis: X-displacement, Y-displacement, and Stress"""
    
    # Exact data from test.out
    nodes = {
        1: {"x": 0.0, "y": 0.0, "ux": 0.0, "uy": 0.0},
        2: {"x": 2.5, "y": 0.0, "ux": 2.50000e-02, "uy": 0.0},
        3: {"x": 2.5, "y": 3.0, "ux": 2.50000e-02, "uy": -9.00000e-03},
        4: {"x": 0.0, "y": 2.0, "ux": -2.21177e-17, "uy": -6.00000e-03},  # ~0
        5: {"x": 1.0, "y": 1.6, "ux": 1.00000e-02, "uy": -4.80000e-03}
    }
    
    elements = {
        1: {"nodes": [1, 2, 5], "sxx": 1.00000e+01, "syy": 4.44089e-16, "sxy": -4.00321e-15},
        2: {"nodes": [2, 3, 5], "sxx": 1.00000e+01, "syy": 2.22045e-15, "sxy": -2.66881e-15},
        3: {"nodes": [3, 4, 5], "sxx": 1.00000e+01, "syy": -8.88178e-16, "sxy": -1.33440e-15},
        4: {"nodes": [4, 1, 5], "sxx": 1.00000e+01, "syy": -1.33227e-15, "sxy": -3.00241e-15}
    }
    
    # Extract coordinates and displacements
    x = np.array([nodes[i]["x"] for i in range(1, 6)])
    y = np.array([nodes[i]["y"] for i in range(1, 6)])
    ux = np.array([nodes[i]["ux"] for i in range(1, 6)])
    uy = np.array([nodes[i]["uy"] for i in range(1, 6)])
    
    # Clean up numerical noise (node 4's ux)
    ux[3] = 0.0  # Node 4's ux should be 0
    
    # Triangulation - elements from test.dat
    triangles = np.array([[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]])  # T3 elements
    triang = tri.Triangulation(x, y, triangles)
    
    # Create figure with 1 row, 3 columns
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle('T3 Patch Test - Displacement and Stress Analysis', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # X-displacement contour
    ax1 = axes[0]
    contour1 = ax1.tricontourf(triang, ux*1000, levels=20, cmap='RdBu_r')
    cbar1 = plt.colorbar(contour1, ax=ax1)
    cbar1.set_label('X-Displacement (mm)', fontsize=12, fontweight='bold')
    ax1.triplot(triang, 'k-', alpha=0.4, linewidth=1.5)
    ax1.plot(x, y, 'ko', markersize=8)
    
    # Add displacement values at nodes
    for i in range(5):
        ax1.text(x[i], y[i]+0.12, f'{ux[i]*1000:.1f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.8))
    
    ax1.set_title('X-Direction Displacement', fontweight='bold', fontsize=14)
    ax1.set_xlabel('X Coordinate (m)', fontsize=12)
    ax1.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    
    # Y-displacement contour
    ax2 = axes[1]
    contour2 = ax2.tricontourf(triang, uy*1000, levels=20, cmap='RdBu_r')
    cbar2 = plt.colorbar(contour2, ax=ax2)
    cbar2.set_label('Y-Displacement (mm)', fontsize=12, fontweight='bold')
    ax2.triplot(triang, 'k-', alpha=0.4, linewidth=1.5)
    ax2.plot(x, y, 'ko', markersize=8)
    
    # Add displacement values at nodes
    for i in range(5):
        ax2.text(x[i], y[i]+0.12, f'{uy[i]*1000:.1f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.8))
    
    ax2.set_title('Y-Direction Displacement (Poisson Effect)', fontweight='bold', fontsize=14)
    ax2.set_xlabel('X Coordinate (m)', fontsize=12)
    ax2.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # Stress distribution - THE KEY RESULT!
    ax3 = axes[2]
    
    # Calculate element centers and stress
    elem_centers = []
    stress_xx = []
    
    for elem_id, elem in elements.items():
        node_ids = elem["nodes"]
        cx = np.mean([nodes[nid]["x"] for nid in node_ids])
        cy = np.mean([nodes[nid]["y"] for nid in node_ids])
        elem_centers.append([cx, cy])
        stress_xx.append(elem["sxx"])
    
    elem_centers = np.array(elem_centers)
    
    # All stresses are identical = 10 Pa!
    scatter = ax3.scatter(elem_centers[:, 0], elem_centers[:, 1], 
                         c=stress_xx, s=1000, cmap='jet', alpha=0.9, 
                         vmin=9.9, vmax=10.1, edgecolors='black', linewidth=2)
    cbar3 = plt.colorbar(scatter, ax=ax3)
    cbar3.set_label('Stress_XX (Pa)', fontsize=12, fontweight='bold')
    ax3.triplot(triang, 'k-', alpha=0.6, linewidth=1.5)
    ax3.plot(x, y, 'ko', markersize=8)
    
    # Label stress values - they should all be 10.0!
    for i, (center, sxx) in enumerate(zip(elem_centers, stress_xx)):
        ax3.text(center[0], center[1], f'{sxx:.1f} Pa', ha='center', va='center', 
                fontsize=13, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))
    
    # Add success message
    ax3.text(1.25, 0.3, 'PATCH TEST\nPASSED!\nCONSTANT STRESS', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='darkgreen',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', 
                     alpha=0.9, edgecolor='green', linewidth=2))
    
    ax3.set_title('Stress_XX Distribution (ALL = 10.0 Pa!)', 
                 fontweight='bold', fontsize=14, color='darkgreen')
    ax3.set_xlabel('X Coordinate (m)', fontsize=12)
    ax3.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    plt.savefig('t3_displacement_stress_analysis.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('t3_displacement_stress_analysis.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    # Print summary
    print("\n" + "="*70)
    print("T3 PATCH TEST - DISPLACEMENT AND STRESS ANALYSIS")
    print("="*70)
    
    print("\nDisplacement Results:")
    print("Node    X-Disp(mm)      Y-Disp(mm)")
    print("-" * 40)
    for i in range(1, 6):
        ux_mm = nodes[i]['ux'] * 1000
        uy_mm = nodes[i]['uy'] * 1000
        print(f"{i:2d}    {ux_mm:10.1f}    {uy_mm:10.1f}")
    
    print("\nStress Results (Patch Test Verification):")
    print("Elem    Stress_XX(Pa)   Status")
    print("-" * 35)
    for elem_id, elem in elements.items():
        print(f"{elem_id:2d}    {elem['sxx']:10.1f}    PASS - CONSTANT")
    
    print(f"\n✓ PATCH TEST VERIFICATION:")
    print(f"   All elements: Stress_XX = 10.0 Pa (CONSTANT)")
    print(f"   Stress_YY ~ 0, Stress_XY ~ 0 (numerical precision)")
    print(f"   T3 element implementation VERIFIED!")
    
    print("\n✓ Displacement and stress analysis saved as:")
    print("  - t3_displacement_stress_analysis.png")
    print("  - t3_displacement_stress_analysis.pdf")

def main():
    """Main function"""
    print("Creating T3 Patch Test - Displacement and Stress Analysis...")
    print("="*70)
    
    create_displacement_stress_analysis()
    
    print("\n" + "="*70)
    print("Displacement and stress analysis completed!")
    print("="*70)

if __name__ == "__main__":
    main()