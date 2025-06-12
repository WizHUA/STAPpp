#!/usr/bin/env python3
"""
Constant Strain Patch Test - Simple Visualization
Geometry Model and Results Analysis (Separate Files)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.patches as patches

def create_constant_strain_geometry():
    """Create geometry model with boundary conditions and loads"""
    
    # Node coordinates from input file
    nodes = {
        1: {"x": 0.0, "y": 0.0, "bc": "fixed"},
        2: {"x": 1.0, "y": 0.0, "bc": "force"},
        3: {"x": 1.0, "y": 1.0, "bc": "force"},
        4: {"x": 0.0, "y": 1.0, "bc": "fixed"}
    }
    
    # Elements connectivity  
    elements = {
        1: [1, 2, 3],  # Element 1: nodes 1-2-3
        2: [1, 3, 4]   # Element 2: nodes 1-3-4
    }
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    ax.set_title('Constant Strain Patch Test - Geometry Model', 
                fontsize=14, fontweight='bold', pad=20)
    
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
            # Fixed nodes - red triangles
            ax.plot(x, y, '^', markersize=15, color='red', markeredgewidth=2)
            # Draw fixed support symbols
            for i in range(4):
                ax.plot([x-0.08+i*0.04, x-0.12+i*0.04], [y-0.08, y+0.08], 
                       'k-', linewidth=2)
        else:
            # Force nodes - green circles
            ax.plot(x, y, 'o', markersize=12, color='green', markeredgewidth=2)
            # Force arrows pointing in positive X direction
            ax.arrow(x+0.05, y, 0.15, 0, head_width=0.05, head_length=0.03, 
                    fc='green', ec='green', linewidth=3)
            ax.text(x+0.25, y+0.05, '100N', fontsize=11, color='green', fontweight='bold')
        
        # Node labels
        ax.text(x-0.15, y+0.15, f'{node_id}', fontsize=12, fontweight='bold', 
               ha='center', va='center')
    
    # Add dimension annotations
    ax.annotate('', xy=(0, -0.2), xytext=(1, -0.2),
               arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(0.5, -0.3, '1.0 m', ha='center', va='center', fontsize=12, fontweight='bold')
    
    ax.annotate('', xy=(-0.3, 0), xytext=(-0.3, 1),
               arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(-0.4, 0.5, '1.0 m', ha='center', va='center', fontsize=12, 
           fontweight='bold', rotation=90)
    
    # Material properties text box
    props_text = (
        "Material Properties:\n"
        "E = 2.1×10⁵ Pa\n"
        "ν = 0.3\n"
        "t = 0.01 m"
    )
    ax.text(1.5, 0.8, props_text, fontsize=10, 
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
    
    # Boundary conditions legend
    legend_text = (
        "Boundary Conditions:\n"
        "△ Fixed support\n"
        "● Load application (100N each)"
    )
    ax.text(1.5, 0.3, legend_text, fontsize=10,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.9))
    
    ax.set_xlim(-0.6, 2.5)
    ax.set_ylim(-0.5, 1.4)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X Coordinate (m)', fontsize=12)
    ax.set_ylabel('Y Coordinate (m)', fontsize=12)
    
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('constant_strain_geometry.png', dpi=300, bbox_inches='tight')
    plt.savefig('constant_strain_geometry.pdf', bbox_inches='tight')
    
    print("Geometry model saved as:")
    print("- constant_strain_geometry.png")
    print("- constant_strain_geometry.pdf")

def create_constant_strain_results():
    """Create results analysis visualization"""
    
    # Exact data from STAPpp output
    nodes = {
        1: {"x": 0.0, "y": 0.0, "ux": 0.0, "uy": 0.0},
        2: {"x": 1.0, "y": 0.0, "ux": 9.52381e-02, "uy": 0.0},
        3: {"x": 1.0, "y": 1.0, "ux": 9.52381e-02, "uy": -2.85714e-02},
        4: {"x": 0.0, "y": 1.0, "ux": 0.0, "uy": -2.85714e-02}
    }
    
    elements = {
        1: {"nodes": [1, 2, 3], "sxx": 2.00000e+04, "syy": -9.09495e-13, "sxy": 0.0},
        2: {"nodes": [1, 3, 4], "sxx": 2.00000e+04, "syy": -9.09495e-13, "sxy": 2.80225e-13}
    }
    
    # Extract coordinates and displacements
    x = np.array([nodes[i]["x"] for i in range(1, 5)])
    y = np.array([nodes[i]["y"] for i in range(1, 5)])
    ux = np.array([nodes[i]["ux"] for i in range(1, 5)])
    uy = np.array([nodes[i]["uy"] for i in range(1, 5)])
    
    # Calculate deformed coordinates
    scale_factor = 10
    x_def = x + ux * scale_factor
    y_def = y + uy * scale_factor
    
    # Calculate displacement magnitude
    displacement_mag = np.sqrt(ux**2 + uy**2)
    
    # Triangulation
    triangles = np.array([[0, 1, 2], [0, 2, 3]])  # T3 elements
    triang = tri.Triangulation(x, y, triangles)
    triang_def = tri.Triangulation(x_def, y_def, triangles)
    
    # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Constant Strain Patch Test - Results Analysis', 
                 fontsize=16, fontweight='bold')
    
    # Original mesh
    ax1 = axes[0, 0]
    ax1.triplot(triang, 'b-', linewidth=2)
    ax1.plot(x, y, 'bo', markersize=8)
    for i in range(4):
        ax1.text(x[i]+0.05, y[i]+0.05, f'{i+1}', fontsize=12, ha='left', fontweight='bold')
    ax1.set_title('Original T3 Mesh', fontweight='bold')
    ax1.set_xlabel('X Coordinate (m)')
    ax1.set_ylabel('Y Coordinate (m)')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Deformation comparison
    ax2 = axes[0, 1]
    ax2.triplot(triang, 'b-', linewidth=2, alpha=0.7, label='Original')
    ax2.triplot(triang_def, 'r--', linewidth=2, alpha=0.7, label=f'Deformed x{scale_factor}')
    ax2.plot(x, y, 'bo', markersize=6)
    ax2.plot(x_def, y_def, 'ro', markersize=6)
    
    # Displacement vectors
    for i in range(4):
        if displacement_mag[i] > 1e-10:
            ax2.arrow(x[i], y[i], ux[i]*scale_factor, uy[i]*scale_factor, 
                     head_width=0.03, head_length=0.02, fc='green', ec='green', alpha=0.8)
    
    ax2.set_title('Mesh Deformation (Scaled 10x)', fontweight='bold')
    ax2.set_xlabel('X Coordinate (m)')
    ax2.set_ylabel('Y Coordinate (m)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    # Displacement magnitude contour
    ax3 = axes[0, 2]
    contour3 = ax3.tricontourf(triang, displacement_mag*1000, levels=20, cmap='viridis')
    cbar3 = plt.colorbar(contour3, ax=ax3)
    cbar3.set_label('Displacement Magnitude (mm)')
    ax3.triplot(triang, 'k-', alpha=0.3)
    ax3.plot(x, y, 'ko', markersize=6)
    ax3.set_title('Displacement Magnitude', fontweight='bold')
    ax3.set_xlabel('X Coordinate (m)')
    ax3.set_ylabel('Y Coordinate (m)')
    ax3.set_aspect('equal')
    
    # X-displacement contour
    ax4 = axes[1, 0]
    contour4 = ax4.tricontourf(triang, ux*1000, levels=20, cmap='RdBu_r')
    cbar4 = plt.colorbar(contour4, ax=ax4)
    cbar4.set_label('X-Displacement (mm)')
    ax4.triplot(triang, 'k-', alpha=0.3)
    ax4.plot(x, y, 'ko', markersize=4)
    # Add displacement values at nodes
    for i in range(4):
        ax4.text(x[i], y[i]+0.05, f'{ux[i]*1000:.1f}', ha='center', va='bottom', 
                fontsize=9, fontweight='bold')
    ax4.set_title('X-Direction Displacement', fontweight='bold')
    ax4.set_xlabel('X Coordinate (m)')
    ax4.set_ylabel('Y Coordinate (m)')
    ax4.set_aspect('equal')
    
    # Y-displacement contour
    ax5 = axes[1, 1]
    contour5 = ax5.tricontourf(triang, uy*1000, levels=20, cmap='RdBu_r')
    cbar5 = plt.colorbar(contour5, ax=ax5)
    cbar5.set_label('Y-Displacement (mm)')
    ax5.triplot(triang, 'k-', alpha=0.3)
    ax5.plot(x, y, 'ko', markersize=4)
    # Add displacement values at nodes
    for i in range(4):
        ax5.text(x[i], y[i]+0.05, f'{uy[i]*1000:.1f}', ha='center', va='bottom', 
                fontsize=9, fontweight='bold')
    ax5.set_title('Y-Direction Displacement', fontweight='bold')
    ax5.set_xlabel('X Coordinate (m)')
    ax5.set_ylabel('Y Coordinate (m)')
    ax5.set_aspect('equal')
    
    # Stress distribution
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
    scatter = ax6.scatter(elem_centers[:, 0], elem_centers[:, 1], 
                         c=stress_xx, s=400, cmap='jet', alpha=0.8)
    cbar6 = plt.colorbar(scatter, ax=ax6)
    cbar6.set_label('σxx Stress (Pa)')
    ax6.triplot(triang, 'k-', alpha=0.5)
    ax6.plot(x, y, 'ko', markersize=6)
    
    # Label stress values
    for i, (center, sxx) in enumerate(zip(elem_centers, stress_xx)):
        ax6.text(center[0], center[1], f'{sxx:.0f}', ha='center', va='center', 
                fontsize=10, fontweight='bold', color='white')
    
    ax6.set_title('σxx Stress Distribution', fontweight='bold')
    ax6.set_xlabel('X Coordinate (m)')
    ax6.set_ylabel('Y Coordinate (m)')
    ax6.set_aspect('equal')
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig('constant_strain_results.png', dpi=300, bbox_inches='tight')
    plt.savefig('constant_strain_results.pdf', bbox_inches='tight')
    
    # Print results summary
    print("\nResults Summary:")
    print("Node    X-Disp(mm)      Y-Disp(mm)      Magnitude(mm)")
    print("-" * 55)
    for i in range(1, 5):
        ux_mm = nodes[i]['ux'] * 1000
        uy_mm = nodes[i]['uy'] * 1000
        mag_mm = np.sqrt(ux_mm**2 + uy_mm**2)
        print(f"{i:2d}    {ux_mm:10.1f}    {uy_mm:10.1f}    {mag_mm:10.1f}")
    
    print("\nElement Stress Results:")
    print("Elem    σxx(Pa)       σyy(Pa)       τxy(Pa)")
    print("-" * 50)
    for elem_id, elem in elements.items():
        print(f"{elem_id:2d}    {elem['sxx']:10.0f}    {elem['syy']:10.2e}    {elem['sxy']:10.2e}")
    
    print("\nResults analysis saved as:")
    print("- constant_strain_results.png")
    print("- constant_strain_results.pdf")

def main():
    """Main function to create both visualizations"""
    print("Creating Constant Strain Patch Test Visualizations...")
    print("="*60)
    
    # Create geometry model
    print("\n1. Creating geometry model...")
    create_constant_strain_geometry()
    
    # Create results analysis
    print("\n2. Creating results analysis...")
    create_constant_strain_results()
    
    print("\n" + "="*60)
    print("All visualizations completed!")
    print("\nMove generated files to your img/ directory:")
    print("mv constant_strain_geometry.png ../writing/img/")
    print("mv constant_strain_results.png ../writing/img/")
    print("="*60)

if __name__ == "__main__":
    main()