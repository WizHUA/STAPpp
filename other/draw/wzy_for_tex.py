#!/usr/bin/env python3
"""
WZY Case Results Visualization - Displacement and Stress Analysis
Generate specific figures for LaTeX document (English Version)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.patches import Polygon
import matplotlib.patches as patches

def create_wzy_displacement_analysis():
    """Create displacement field visualization for WZY case"""
    
    # Exact data from STAPpp output
    nodes = {
        1: {"x": 0.0, "y": 0.0, "ux": 0.0, "uy": 0.0},
        2: {"x": 2.0, "y": 0.5, "ux": -3.87101e-07, "uy": -6.65683e-06},
        3: {"x": 2.0, "y": 1.0, "ux": 1.23482e-06, "uy": -7.04068e-06},
        4: {"x": 0.0, "y": 1.0, "ux": 0.0, "uy": 0.0}
    }
    
    # Extract coordinates and displacements
    x = np.array([nodes[i]["x"] for i in range(1, 5)])
    y = np.array([nodes[i]["y"] for i in range(1, 5)])
    ux = np.array([nodes[i]["ux"] for i in range(1, 5)])
    uy = np.array([nodes[i]["uy"] for i in range(1, 5)])
    
    # Calculate displacement magnitude
    displacement_mag = np.sqrt(ux**2 + uy**2)
    
    # Deformation scale factors
    scale_factor = 100000  # For deformation visualization
    x_def = x + ux * scale_factor
    y_def = y + uy * scale_factor
    
    # Triangulation
    triangles = np.array([[0, 1, 3], [1, 2, 3]])  # T3 elements
    triang = tri.Triangulation(x, y, triangles)
    triang_def = tri.Triangulation(x_def, y_def, triangles)
    
    # Create figure with 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Problem 4-4 Trapezoidal Structure - Displacement Analysis', fontsize=16, fontweight='bold')
    
    # Original vs Deformed mesh
    ax1 = axes[0, 0]
    # Draw trapezoidal background
    trap_vertices = np.array([[0.0, 0.0], [2.0, 0.5], [2.0, 1.0], [0.0, 1.0]])
    trapezoid = patches.Polygon(trap_vertices, closed=True, 
                               facecolor='lightblue', alpha=0.2, edgecolor='none')
    ax1.add_patch(trapezoid)
    
    # Original mesh
    ax1.triplot(triang, 'b-', linewidth=2.5, alpha=0.8, label='Original Mesh')
    ax1.plot(x, y, 'bo', markersize=8)
    
    # Deformed mesh
    ax1.triplot(triang_def, 'r--', linewidth=2.5, alpha=0.8, label=f'Deformed Mesh (x{scale_factor:g})')
    ax1.plot(x_def, y_def, 'ro', markersize=8)
    
    # Node labels
    for i in range(4):
        ax1.text(x[i]-0.1, y[i]+0.08, f'{i+1}', fontsize=12, fontweight='bold', 
                ha='center', va='center', 
                bbox=dict(boxstyle="circle,pad=0.2", facecolor='yellow', alpha=0.8))
    
    # Load arrows
    ax1.arrow(x[2], y[2]+0.1, 0, -0.15, head_width=0.05, head_length=0.03, 
             fc='green', ec='green', linewidth=3)
    ax1.arrow(x[3], y[3]+0.1, 0, -0.15, head_width=0.05, head_length=0.03, 
             fc='green', ec='green', linewidth=3)
    ax1.text(x[2]+0.15, y[2], '20N', fontsize=11, color='green', fontweight='bold')
    ax1.text(x[3]+0.15, y[3], '20N', fontsize=11, color='green', fontweight='bold')
    
    # Fixed supports
    for node_id in [1, 4]:
        node_x, node_y = x[node_id-1], y[node_id-1]
        for i in range(4):
            ax1.plot([node_x-0.08+i*0.04, node_x-0.12+i*0.04], 
                    [node_y-0.08, node_y+0.08], 'k-', linewidth=2)
    
    ax1.set_title('Original vs Deformed Mesh', fontweight='bold', fontsize=14)
    ax1.set_xlabel('X Coordinate (m)', fontsize=12)
    ax1.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    ax1.set_xlim(-0.3, 2.5)
    ax1.set_ylim(-0.2, 1.3)
    
    # Displacement magnitude contour
    ax2 = axes[0, 1]
    contour2 = ax2.tricontourf(triang, displacement_mag*1e6, levels=20, cmap='viridis')
    cbar2 = plt.colorbar(contour2, ax=ax2)
    cbar2.set_label('Displacement Magnitude (μm)', fontsize=12)
    ax2.triplot(triang, 'k-', alpha=0.4, linewidth=1)
    ax2.plot(x, y, 'ko', markersize=6)
    
    # Add displacement values at nodes
    for i in range(4):
        disp_mag = displacement_mag[i] * 1e6
        if disp_mag > 0.001:  # Only show non-zero displacements
            ax2.text(x[i], y[i]+0.05, f'{disp_mag:.2f}', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold', 
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    ax2.set_title('Displacement Magnitude', fontweight='bold', fontsize=14)
    ax2.set_xlabel('X Coordinate (m)', fontsize=12)
    ax2.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax2.set_aspect('equal')
    
    # X-displacement contour
    ax3 = axes[1, 0]
    contour3 = ax3.tricontourf(triang, ux*1e6, levels=20, cmap='RdBu_r')
    cbar3 = plt.colorbar(contour3, ax=ax3)
    cbar3.set_label('X-Displacement (μm)', fontsize=12)
    ax3.triplot(triang, 'k-', alpha=0.4, linewidth=1)
    ax3.plot(x, y, 'ko', markersize=6)
    
    # Add X-displacement values at nodes
    for i in range(4):
        ux_val = ux[i] * 1e6
        if abs(ux_val) > 0.001:
            ax3.text(x[i], y[i]+0.05, f'{ux_val:.2f}', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    ax3.set_title('X-Direction Displacement', fontweight='bold', fontsize=14)
    ax3.set_xlabel('X Coordinate (m)', fontsize=12)
    ax3.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax3.set_aspect('equal')
    
    # Y-displacement contour
    ax4 = axes[1, 1]
    contour4 = ax4.tricontourf(triang, uy*1e6, levels=20, cmap='RdBu_r')
    cbar4 = plt.colorbar(contour4, ax=ax4)
    cbar4.set_label('Y-Displacement (μm)', fontsize=12)
    ax4.triplot(triang, 'k-', alpha=0.4, linewidth=1)
    ax4.plot(x, y, 'ko', markersize=6)
    
    # Add Y-displacement values at nodes
    for i in range(4):
        uy_val = uy[i] * 1e6
        if abs(uy_val) > 0.001:
            ax4.text(x[i], y[i]+0.05, f'{uy_val:.2f}', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    ax4.set_title('Y-Direction Displacement', fontweight='bold', fontsize=14)
    ax4.set_xlabel('X Coordinate (m)', fontsize=12)
    ax4.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax4.set_aspect('equal')
    
    plt.tight_layout()
    
    # Save displacement analysis
    plt.savefig('wzy_displacement_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('wzy_displacement_analysis.pdf', bbox_inches='tight')
    
    print("Displacement analysis saved as:")
    print("- wzy_displacement_analysis.png")
    print("- wzy_displacement_analysis.pdf")

def create_wzy_stress_analysis():
    """Create stress field visualization for WZY case"""
    
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
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Problem 4-4 Trapezoidal Structure - Stress Analysis', fontsize=16, fontweight='bold')
    
    # Function to get contrasting text color based on background color
    def get_text_color(value, vmin, vmax, cmap_name):
        # Normalize value to [0, 1]
        norm_val = (value - vmin) / (vmax - vmin) if vmax != vmin else 0.5
        
        if cmap_name == 'RdBu_r':
            # For RdBu_r: red for positive, blue for negative, white for zero
            if norm_val > 0.7 or norm_val < 0.3:  # Strong red or blue
                return 'white'
            else:  # Light colors or white in middle
                return 'black'
        elif cmap_name == 'jet':
            # For jet: dark blue at low values, red at high values
            if norm_val < 0.15 or norm_val > 0.85:  # Very dark blue or red
                return 'white'
            else:
                return 'black'
    
    # Sxx stress distribution
    ax1 = axes[0, 0]
    # Draw trapezoidal background
    trap_vertices = np.array([[0.0, 0.0], [2.0, 0.5], [2.0, 1.0], [0.0, 1.0]])
    trapezoid = patches.Polygon(trap_vertices, closed=True, 
                               facecolor='lightgray', alpha=0.2, edgecolor='black')
    ax1.add_patch(trapezoid)
    
    # Larger scatter points
    scatter1 = ax1.scatter(elem_centers[:, 0], elem_centers[:, 1], c=stress_xx, 
                          s=1200, cmap='RdBu_r', alpha=0.9, edgecolors='black', linewidth=2)
    ax1.triplot(triang, 'k-', alpha=0.6, linewidth=1.5)
    ax1.plot(x, y, 'ko', markersize=8)
    
    # Element labels directly on scatter points
    vmin, vmax = min(stress_xx), max(stress_xx)
    for i, (cx, cy, sxx) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], stress_xx)):
        text_color = get_text_color(sxx, vmin, vmax, 'RdBu_r')
        ax1.text(cx, cy, f'E{i+1}\n{sxx:.1f}', ha='center', va='center', 
                fontsize=11, fontweight='bold', color=text_color)
    
    # Node labels
    for i in range(4):
        ax1.text(x[i]-0.1, y[i]+0.08, f'{i+1}', fontsize=12, fontweight='bold', 
                ha='center', va='center', 
                bbox=dict(boxstyle="circle,pad=0.2", facecolor='yellow', alpha=0.8))
    
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label('σxx Stress (Pa)', fontsize=12)
    ax1.set_title('σxx Stress Distribution', fontweight='bold', fontsize=14)
    ax1.set_xlabel('X Coordinate (m)', fontsize=12)
    ax1.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    
    # Syy stress distribution
    ax2 = axes[0, 1]
    trapezoid2 = patches.Polygon(trap_vertices, closed=True, 
                                facecolor='lightgray', alpha=0.2, edgecolor='black')
    ax2.add_patch(trapezoid2)
    
    scatter2 = ax2.scatter(elem_centers[:, 0], elem_centers[:, 1], c=stress_yy, 
                          s=1200, cmap='RdBu_r', alpha=0.9, edgecolors='black', linewidth=2)
    ax2.triplot(triang, 'k-', alpha=0.6, linewidth=1.5)
    ax2.plot(x, y, 'ko', markersize=8)
    
    # Element labels directly on scatter points
    vmin, vmax = min(stress_yy), max(stress_yy)
    for i, (cx, cy, syy) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], stress_yy)):
        text_color = get_text_color(syy, vmin, vmax, 'RdBu_r')
        ax2.text(cx, cy, f'E{i+1}\n{syy:.1f}', ha='center', va='center', 
                fontsize=11, fontweight='bold', color=text_color)
    
    # Node labels
    for i in range(4):
        ax2.text(x[i]-0.1, y[i]+0.08, f'{i+1}', fontsize=12, fontweight='bold', 
                ha='center', va='center', 
                bbox=dict(boxstyle="circle,pad=0.2", facecolor='yellow', alpha=0.8))
    
    cbar2 = plt.colorbar(scatter2, ax=ax2)
    cbar2.set_label('σyy Stress (Pa)', fontsize=12)
    ax2.set_title('σyy Stress Distribution', fontweight='bold', fontsize=14)
    ax2.set_xlabel('X Coordinate (m)', fontsize=12)
    ax2.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # Sxy stress distribution
    ax3 = axes[1, 0]
    trapezoid3 = patches.Polygon(trap_vertices, closed=True, 
                                facecolor='lightgray', alpha=0.2, edgecolor='black')
    ax3.add_patch(trapezoid3)
    
    scatter3 = ax3.scatter(elem_centers[:, 0], elem_centers[:, 1], c=stress_xy, 
                          s=1200, cmap='RdBu_r', alpha=0.9, edgecolors='black', linewidth=2)
    ax3.triplot(triang, 'k-', alpha=0.6, linewidth=1.5)
    ax3.plot(x, y, 'ko', markersize=8)
    
    # Element labels directly on scatter points
    vmin, vmax = min(stress_xy), max(stress_xy)
    for i, (cx, cy, sxy) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], stress_xy)):
        text_color = get_text_color(sxy, vmin, vmax, 'RdBu_r')
        ax3.text(cx, cy, f'E{i+1}\n{sxy:.1f}', ha='center', va='center', 
                fontsize=11, fontweight='bold', color=text_color)
    
    # Node labels
    for i in range(4):
        ax3.text(x[i]-0.1, y[i]+0.08, f'{i+1}', fontsize=12, fontweight='bold', 
                ha='center', va='center', 
                bbox=dict(boxstyle="circle,pad=0.2", facecolor='yellow', alpha=0.8))
    
    cbar3 = plt.colorbar(scatter3, ax=ax3)
    cbar3.set_label('τxy Stress (Pa)', fontsize=12)
    ax3.set_title('τxy Shear Stress Distribution', fontweight='bold', fontsize=14)
    ax3.set_xlabel('X Coordinate (m)', fontsize=12)
    ax3.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)
    
    # von Mises stress distribution
    ax4 = axes[1, 1]
    trapezoid4 = patches.Polygon(trap_vertices, closed=True, 
                                facecolor='lightgray', alpha=0.2, edgecolor='black')
    ax4.add_patch(trapezoid4)
    
    scatter4 = ax4.scatter(elem_centers[:, 0], elem_centers[:, 1], c=von_mises, 
                          s=1200, cmap='jet', alpha=0.9, edgecolors='black', linewidth=2)
    ax4.triplot(triang, 'k-', alpha=0.6, linewidth=1.5)
    ax4.plot(x, y, 'ko', markersize=8)
    
    # Element labels directly on scatter points
    vmin, vmax = min(von_mises), max(von_mises)
    for i, (cx, cy, vm) in enumerate(zip(elem_centers[:, 0], elem_centers[:, 1], von_mises)):
        text_color = get_text_color(vm, vmin, vmax, 'jet')
        ax4.text(cx, cy, f'E{i+1}\n{vm:.1f}', ha='center', va='center', 
                fontsize=11, fontweight='bold', color=text_color)
    
    # Node labels
    for i in range(4):
        ax4.text(x[i]-0.1, y[i]+0.08, f'{i+1}', fontsize=12, fontweight='bold', 
                ha='center', va='center', 
                bbox=dict(boxstyle="circle,pad=0.2", facecolor='yellow', alpha=0.8))
    
    # Load arrows
    ax4.arrow(x[2], y[2]+0.1, 0, -0.12, head_width=0.04, head_length=0.025, 
             fc='green', ec='green', linewidth=2.5)
    ax4.arrow(x[3], y[3]+0.1, 0, -0.12, head_width=0.04, head_length=0.025, 
             fc='green', ec='green', linewidth=2.5)
    ax4.text(x[2]+0.12, y[2], '20N', fontsize=10, color='green', fontweight='bold')
    ax4.text(x[3]+0.12, y[3], '20N', fontsize=10, color='green', fontweight='bold')
    
    cbar4 = plt.colorbar(scatter4, ax=ax4)
    cbar4.set_label('von Mises Stress (Pa)', fontsize=12)
    ax4.set_title('von Mises Stress Distribution', fontweight='bold', fontsize=14)
    ax4.set_xlabel('X Coordinate (m)', fontsize=12)
    ax4.set_ylabel('Y Coordinate (m)', fontsize=12)
    ax4.set_aspect('equal')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save stress analysis
    plt.savefig('wzy_stress_analysis.png', dpi=300, bbox_inches='tight')
    plt.savefig('wzy_stress_analysis.pdf', bbox_inches='tight')
    
    print("Stress analysis saved as:")
    print("- wzy_stress_analysis.png")
    print("- wzy_stress_analysis.pdf")

def main():
    """Main function to create both visualizations"""
    print("Creating Problem 4-4 Trapezoidal Structure Analysis...")
    print("="*60)
    
    # Create displacement visualization
    print("\n1. Generating displacement analysis...")
    create_wzy_displacement_analysis()
    
    # Create stress visualization
    print("\n2. Generating stress analysis...")
    create_wzy_stress_analysis()
    
    print("\n" + "="*60)
    print("All visualizations completed!")
    print("\nMove generated files to img/ directory:")
    print("mv wzy_displacement_analysis.png ../writing/img/")
    print("mv wzy_stress_analysis.png ../writing/img/")
    print("="*60)

if __name__ == "__main__":
    main()