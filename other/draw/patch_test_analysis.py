#!/usr/bin/env python3
"""
T3 Patch Test Analysis - Using actual test.dat data
Geometry Model and Results Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.patches as patches

# Fix font issues for Linux systems
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

def create_t3_patch_geometry():
    """Create geometry model with boundary conditions and loads from test.dat"""
    
    # Node coordinates from test.dat
    nodes = {
        1: {"x": 0.0, "y": 0.0, "bc": "fixed"},      # Fully fixed
        2: {"x": 2.5, "y": 0.0, "bc": "y_fixed"},    # Y-direction fixed
        3: {"x": 2.5, "y": 3.0, "bc": "free"},       # Free
        4: {"x": 0.0, "y": 2.0, "bc": "free"},       # Free
        5: {"x": 1.0, "y": 1.6, "bc": "free"}        # Internal node, free
    }
    
    # Elements connectivity from test.dat
    elements = {
        1: [1, 2, 5],  # Element 1: nodes 1-2-5
        2: [2, 3, 5],  # Element 2: nodes 2-3-5
        3: [3, 4, 5],  # Element 3: nodes 3-4-5
        4: [4, 1, 5]   # Element 4: nodes 4-1-5
    }
    
    # Loads from test.dat
    loads = {
        1: -10.0,   # Node 1: -10N in X direction
        2: 15.0,    # Node 2: 15N in X direction
        3: 10.0,    # Node 3: 10N in X direction
        4: -15.0    # Node 4: -15N in X direction
    }
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    ax.set_title('T3 Patch Test - Geometry Model (test.dat)', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Draw T3 elements
    for elem_id, node_ids in elements.items():
        x_coords = [nodes[nid]["x"] for nid in node_ids]
        y_coords = [nodes[nid]["y"] for nid in node_ids]
        x_coords.append(x_coords[0])  # Close the triangle
        y_coords.append(y_coords[0])
        
        ax.plot(x_coords, y_coords, 'b-', linewidth=2.5, alpha=0.8)
        
        # Element center for labeling
        cx = np.mean([nodes[nid]["x"] for nid in node_ids])
        cy = np.mean([nodes[nid]["y"] for nid in node_ids])
        ax.text(cx, cy, f'T3-{elem_id}', ha='center', va='center', 
               fontsize=12, fontweight='bold', 
               bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8))
    
    # Draw and label nodes
    for node_id, node in nodes.items():
        x, y = node["x"], node["y"]
        bc = node["bc"]
        
        if bc == "fixed":
            # Fixed nodes - red squares
            ax.plot(x, y, 's', markersize=14, color='red', markeredgewidth=2)
            # Draw fixed support symbols
            for i in range(5):
                ax.plot([x-0.15+i*0.06, x-0.18+i*0.06], [y-0.15, y+0.15], 
                       'k-', linewidth=2)
            ax.text(x-0.35, y, 'FIXED', fontsize=10, color='red', fontweight='bold', 
                   ha='center', rotation=90)
                   
        elif bc == "y_fixed":
            # Y-direction fixed - orange triangle
            ax.plot(x, y, '^', markersize=14, color='orange', markeredgewidth=2)
            # Draw Y-constraint symbol
            ax.plot([x-0.12, x+0.12], [y-0.12, y-0.12], 'k-', linewidth=3)
            ax.text(x+0.25, y-0.18, 'Y-FIXED', fontsize=10, color='orange', 
                   fontweight='bold', ha='left')
        else:
            # Free nodes - green circles
            ax.plot(x, y, 'o', markersize=12, color='green', markeredgewidth=2)
        
        # Load arrows
        if node_id in loads:
            load_val = loads[node_id]
            arrow_length = abs(load_val) * 0.025  # Scale arrow length
            arrow_color = 'red' if load_val < 0 else 'blue'
            arrow_start = 0.18 if load_val > 0 else -0.18 - arrow_length
            
            ax.arrow(x + arrow_start, y, arrow_length if load_val > 0 else -arrow_length, 0, 
                    head_width=0.1, head_length=0.06, fc=arrow_color, ec=arrow_color, linewidth=2.5)
            ax.text(x + arrow_start + (arrow_length/2 if load_val > 0 else -arrow_length/2), 
                   y + 0.15, f'{load_val}N', fontsize=11, color=arrow_color, 
                   fontweight='bold', ha='center')
        
        # Node labels
        ax.text(x-0.25, y+0.3, f'Node {node_id}', fontsize=12, fontweight='bold', 
               ha='center', va='center', 
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9, edgecolor='black'))
    
    # Add dimension annotations
    ax.annotate('', xy=(0, -0.4), xytext=(2.5, -0.4),
               arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(1.25, -0.6, '2.5 m', ha='center', va='center', fontsize=13, fontweight='bold')
    
    ax.annotate('', xy=(-0.5, 0), xytext=(-0.5, 2.0),
               arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(-0.7, 1.0, '2.0 m', ha='center', va='center', fontsize=13, 
           fontweight='bold', rotation=90)
    
    ax.annotate('', xy=(2.8, 0), xytext=(2.8, 3.0),
               arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(3.0, 1.5, '3.0 m', ha='center', va='center', fontsize=13, 
           fontweight='bold', rotation=90)
    
    # Material properties text box
    props_text = (
        "MATERIAL PROPERTIES:\n"
        "Young's Modulus E = 1,000 Pa\n"
        "Poisson's Ratio nu = 0.3\n"
        "Thickness t = 1.0 m\n\n"
        "LOAD EQUILIBRIUM:\n"
        "Sum Fx = -10+15+10-15 = 0 N\n"
        "System is in equilibrium"
    )
    ax.text(3.4, 2.4, props_text, fontsize=11, 
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9, edgecolor='orange'))
    
    # Boundary conditions legend
    legend_text = (
        "BOUNDARY CONDITIONS:\n"
        "Red Square: Node 1 (ux=uy=0) FIXED\n"
        "Orange Triangle: Node 2 (uy=0) Y-FIXED\n"
        "Green Circle: Nodes 3,4,5 FREE\n\n"
        "FINITE ELEMENTS:\n"
        "4 T3 triangular elements\n"
        "All elements share internal node 5\n"
        "Total DOF = 7 equations"
    )
    ax.text(3.4, 1.0, legend_text, fontsize=11,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.9, edgecolor='gray'))
    
    ax.set_xlim(-0.9, 5.2)
    ax.set_ylim(-0.9, 3.8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X Coordinate (m)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Y Coordinate (m)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # Save the figure with specific backend to avoid font warnings
    plt.savefig('t3_patch_geometry.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.savefig('t3_patch_geometry.pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()  # Close figure to free memory
    
    print("✓ Geometry model saved as:")
    print("  - t3_patch_geometry.png")
    print("  - t3_patch_geometry.pdf")

def create_t3_patch_results():
    """Create results analysis visualization using test.out data"""
    
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
    
    # Calculate deformed coordinates
    scale_factor = 60  # Increased scale for better visualization
    x_def = x + ux * scale_factor
    y_def = y + uy * scale_factor
    
    # Calculate displacement magnitude
    displacement_mag = np.sqrt(ux**2 + uy**2)
    
    # Triangulation - elements from test.dat
    triangles = np.array([[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]])  # T3 elements
    triang = tri.Triangulation(x, y, triangles)
    triang_def = tri.Triangulation(x_def, y_def, triangles)
    
    # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('T3 Patch Test - Results Analysis (CONSTANT STRESS ACHIEVED!)', 
                 fontsize=18, fontweight='bold', color='darkgreen')
    
    # Original mesh
    ax1 = axes[0, 0]
    ax1.triplot(triang, 'b-', linewidth=2.5)
    ax1.plot(x, y, 'bo', markersize=10)
    for i in range(5):
        ax1.text(x[i]+0.08, y[i]+0.08, f'{i+1}', fontsize=12, ha='left', fontweight='bold')
    ax1.set_title('Original T3 Mesh (4 Elements)', fontweight='bold', fontsize=14)
    ax1.set_xlabel('X Coordinate (m)', fontsize=12)
    ax1.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Deformation comparison
    ax2 = axes[0, 1]
    ax2.triplot(triang, 'b-', linewidth=2.5, alpha=0.7, label='Original Mesh')
    ax2.triplot(triang_def, 'r--', linewidth=2.5, alpha=0.8, label=f'Deformed x{scale_factor}')
    ax2.plot(x, y, 'bo', markersize=8)
    ax2.plot(x_def, y_def, 'ro', markersize=8)
    
    # Displacement vectors
    for i in range(5):
        if displacement_mag[i] > 1e-10:
            ax2.arrow(x[i], y[i], ux[i]*scale_factor, uy[i]*scale_factor, 
                     head_width=0.1, head_length=0.06, fc='green', ec='green', alpha=0.8, linewidth=2)
    
    ax2.set_title(f'Mesh Deformation (Scaled {scale_factor}x)', fontweight='bold', fontsize=14)
    ax2.set_xlabel('X Coordinate (m)', fontsize=12)
    ax2.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    # Displacement magnitude contour
    ax3 = axes[0, 2]
    contour3 = ax3.tricontourf(triang, displacement_mag*1000, levels=20, cmap='plasma')
    cbar3 = plt.colorbar(contour3, ax=ax3)
    cbar3.set_label('Displacement Magnitude (mm)', fontsize=12)
    ax3.triplot(triang, 'k-', alpha=0.4)
    ax3.plot(x, y, 'ko', markersize=8)
    ax3.set_title('Displacement Magnitude Distribution', fontweight='bold', fontsize=14)
    ax3.set_xlabel('X Coordinate (m)', fontsize=12)
    ax3.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax3.set_aspect('equal')
    
    # X-displacement contour
    ax4 = axes[1, 0]
    contour4 = ax4.tricontourf(triang, ux*1000, levels=20, cmap='RdBu_r')
    cbar4 = plt.colorbar(contour4, ax=ax4)
    cbar4.set_label('X-Displacement (mm)', fontsize=12)
    ax4.triplot(triang, 'k-', alpha=0.4)
    ax4.plot(x, y, 'ko', markersize=6)
    # Add displacement values at nodes
    for i in range(5):
        ax4.text(x[i], y[i]+0.12, f'{ux[i]*1000:.1f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.7))
    ax4.set_title('X-Direction Displacement', fontweight='bold', fontsize=14)
    ax4.set_xlabel('X Coordinate (m)', fontsize=12)
    ax4.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax4.set_aspect('equal')
    
    # Y-displacement contour
    ax5 = axes[1, 1]
    contour5 = ax5.tricontourf(triang, uy*1000, levels=20, cmap='RdBu_r')
    cbar5 = plt.colorbar(contour5, ax=ax5)
    cbar5.set_label('Y-Displacement (mm)', fontsize=12)
    ax5.triplot(triang, 'k-', alpha=0.4)
    ax5.plot(x, y, 'ko', markersize=6)
    # Add displacement values at nodes
    for i in range(5):
        ax5.text(x[i], y[i]+0.12, f'{uy[i]*1000:.1f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.7))
    ax5.set_title('Y-Direction Displacement (Poisson Effect)', fontweight='bold', fontsize=14)
    ax5.set_xlabel('X Coordinate (m)', fontsize=12)
    ax5.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax5.set_aspect('equal')
    
    # Stress distribution - THE KEY RESULT!
    ax6 = axes[1, 2]
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
    scatter = ax6.scatter(elem_centers[:, 0], elem_centers[:, 1], 
                         c=stress_xx, s=800, cmap='jet', alpha=0.9, vmin=9.9, vmax=10.1, edgecolors='black', linewidth=2)
    cbar6 = plt.colorbar(scatter, ax=ax6)
    cbar6.set_label('Stress_XX (Pa)', fontsize=12, fontweight='bold')
    ax6.triplot(triang, 'k-', alpha=0.6, linewidth=1.5)
    ax6.plot(x, y, 'ko', markersize=8)
    
    # Label stress values - they should all be 10.0!
    for i, (center, sxx) in enumerate(zip(elem_centers, stress_xx)):
        ax6.text(center[0], center[1], f'{sxx:.1f} Pa', ha='center', va='center', 
                fontsize=13, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8))
    
    # Add success message
    ax6.text(1.25, 0.3, 'PATCH TEST\nPASSED!\nCONSTANT STRESS\nACHIEVED', 
            ha='center', va='center', fontsize=16, fontweight='bold', color='darkgreen',
            bbox=dict(boxstyle="round,pad=0.6", facecolor='lightgreen', alpha=0.9, edgecolor='green', linewidth=2))
    
    ax6.set_title('Stress_XX Distribution (ALL = 10.0 Pa!)', fontweight='bold', fontsize=14, color='darkgreen')
    ax6.set_xlabel('X Coordinate (m)', fontsize=12)
    ax6.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax6.set_aspect('equal')
    
    plt.tight_layout()
    
    # Save figure with specific backend to avoid font warnings
    plt.savefig('t3_patch_results.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('t3_patch_results.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()  # Close figure to free memory
    
    # Print results summary
    print("\n" + "="*70)
    print("T3 PATCH TEST RESULTS ANALYSIS")
    print("="*70)
    print("Node    X-Disp(mm)      Y-Disp(mm)      Magnitude(mm)")
    print("-" * 60)
    for i in range(1, 6):
        ux_mm = nodes[i]['ux'] * 1000
        uy_mm = nodes[i]['uy'] * 1000
        mag_mm = np.sqrt(ux_mm**2 + uy_mm**2)
        print(f"{i:2d}    {ux_mm:10.1f}    {uy_mm:10.1f}    {mag_mm:10.1f}")
    
    print("\nElement Stress Results (PATCH TEST):")
    print("Elem    Stress_XX(Pa)   Stress_YY(Pa)   Stress_XY(Pa)   Status")
    print("-" * 70)
    for elem_id, elem in elements.items():
        syy_clean = "~0" if abs(elem['syy']) < 1e-10 else f"{elem['syy']:.2e}"
        sxy_clean = "~0" if abs(elem['sxy']) < 1e-10 else f"{elem['sxy']:.2e}"
        print(f"{elem_id:2d}    {elem['sxx']:10.1f}    {syy_clean:>12s}    {sxy_clean:>12s}    PASS")
    
    print(f"\nPATCH TEST RESULT: PASSED!")
    print(f"   All elements show Stress_XX = 10.0 Pa (CONSTANT STRESS)")
    print(f"   Stress_YY ~ 0, Stress_XY ~ 0 (numerical precision)")
    print(f"   T3 element implementation is CORRECT!")
    
    print("\n✓ Results analysis saved as:")
    print("  - t3_patch_results.png")
    print("  - t3_patch_results.pdf")

def main():
    """Main function to create both visualizations"""
    print("Creating T3 Patch Test Visualizations (test.dat)...")
    print("="*70)
    
    # Create geometry model
    print("\n1. Creating geometry model...")
    create_t3_patch_geometry()
    
    # Create results analysis
    print("\n2. Creating results analysis...")
    create_t3_patch_results()
    
    print("\n" + "="*70)
    print("All visualizations completed successfully!")
    print("\nGenerated files:")
    print("- t3_patch_geometry.png/pdf")
    print("- t3_patch_results.png/pdf")
    print("="*70)

if __name__ == "__main__":
    main()