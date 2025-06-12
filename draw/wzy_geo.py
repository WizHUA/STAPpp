#!/usr/bin/env python3
"""
WZY Trapezoidal Structure - Geometry Model Only
Based on STAPpp input file: wzy.dat
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_wzy_geometry():
    """Create WZY trapezoidal structure geometry model with boundary conditions and loads"""
    
    # Node coordinates from wzy.dat input file
    nodes = {
        1: {"x": 0.0, "y": 0.0, "bc": "fixed"},     # Fixed support
        2: {"x": 2.0, "y": 0.5, "bc": "free"},     # Free node
        3: {"x": 2.0, "y": 1.0, "bc": "load"},     # Load application (-20N)
        4: {"x": 0.0, "y": 1.0, "bc": "load"}      # Load application (-20N)
    }
    
    # Elements connectivity from wzy.dat
    elements = {
        1: [1, 2, 4],  # Element 1: nodes 1-2-4
        2: [2, 3, 4]   # Element 2: nodes 2-3-4
    }
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # !name
    # ax.set_title('WZY Trapezoidal Structure - Geometry Model & Load Distribution', 
    #             fontsize=14, fontweight='bold', pad=20)
    ax.set_title('Trapezoidal Structure - Geometry Model & Load Distribution', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Draw the trapezoidal region (filled background)
    trap_vertices = np.array([[0.0, 0.0], [2.0, 0.5], [2.0, 1.0], [0.0, 1.0], [0.0, 0.0]])
    trapezoid = patches.Polygon(trap_vertices[:-1], closed=True, 
                               facecolor='lightblue', alpha=0.3, edgecolor='none')
    ax.add_patch(trapezoid)
    
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
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    # Draw and label nodes
    for node_id, node in nodes.items():
        x, y = node["x"], node["y"]
        bc = node["bc"]
        
        if bc == "fixed":
            # Fixed nodes - red triangular supports
            ax.plot(x, y, '^', markersize=15, color='red', markeredgewidth=2)
            # Draw fixed support symbols (hatching pattern)
            for i in range(5):
                ax.plot([x-0.1+i*0.05, x-0.15+i*0.05], [y-0.1, y+0.1], 
                       'k-', linewidth=2)
            ax.text(x, y-0.2, 'Fixed', ha='center', va='center', 
                   fontsize=10, fontweight='bold', color='red')
        elif bc == "load":
            # Load nodes - green circles
            ax.plot(x, y, 'o', markersize=12, color='green', markeredgewidth=2)
            # Force arrows pointing downward (negative Y direction)
            ax.arrow(x, y+0.05, 0, -0.15, head_width=0.05, head_length=0.03, 
                    fc='green', ec='green', linewidth=3)
            ax.text(x+0.15, y+0.05, '20N', fontsize=11, color='green', fontweight='bold')
        else:
            # Free nodes - blue circles
            ax.plot(x, y, 'o', markersize=12, color='blue', markeredgewidth=2)
        
        # Node labels with coordinates
        ax.text(x-0.2, y+0.15, f'{node_id}', fontsize=12, fontweight='bold', 
               ha='center', va='center', 
               bbox=dict(boxstyle="circle,pad=0.2", facecolor='yellow', alpha=0.8))
        ax.text(x-0.05, y-0.15, f'({x:.1f},{y:.1f})', fontsize=9, 
               ha='center', va='center', style='italic')
    
    # Add dimension annotations
    # Bottom edge
    ax.annotate('', xy=(0, -0.15), xytext=(2, -0.15),
               arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(1.0, -0.25, '2.0 m', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Top edge
    ax.annotate('', xy=(0, 1.15), xytext=(2, 1.15),
               arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(1.0, 1.25, '2.0 m', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Left height
    ax.annotate('', xy=(-0.2, 0), xytext=(-0.2, 1),
               arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(-0.3, 0.5, '1.0 m', ha='center', va='center', fontsize=12, 
           fontweight='bold', rotation=90)
    
    # Right height (with offset)
    ax.annotate('', xy=(2.2, 0.5), xytext=(2.2, 1.0),
               arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(2.3, 0.75, '0.5 m', ha='center', va='center', fontsize=12, 
           fontweight='bold', rotation=90)
    
    # Material properties text box
    props_text = (
        "Material Properties:\n"
        "E = 3.0×10⁷ Pa\n"
        "ν = 0.3\n"
        "Thickness = 1.0 m"
    )
    ax.text(2.7, 0.8, props_text, fontsize=10, 
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
    
    # # Boundary conditions and loads legend
    # legend_text = (
    #     "Boundary Conditions:\n"
    #     "△ Fixed support (Nodes 1,4)\n"
    #     "○ Free node (Node 2)\n"
    #     "● Load application\n"
    #     "   20N downward (Nodes 3,4)\n\n"
    #     "Element Information:\n"
    #     "• T3-1: Nodes 1-2-4\n"
    #     "• T3-2: Nodes 2-3-4"
    # )
    # ax.text(2.7, 0.3, legend_text, fontsize=10,
    #        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.9))
    
    # Load resultant
    total_load_text = "Total Load: 40N downward"
    ax.text(1.0, 0.2, total_load_text, fontsize=12, fontweight='bold',
           ha='center', va='center',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8))
    
    # Add coordinate system
    ax.arrow(-0.6, -0.4, 0.15, 0, head_width=0.03, head_length=0.03, 
             fc='black', ec='black', linewidth=2)
    ax.arrow(-0.6, -0.4, 0, 0.15, head_width=0.03, head_length=0.03, 
             fc='black', ec='black', linewidth=2)
    ax.text(-0.55, -0.5, 'X', fontsize=12, fontweight='bold')
    ax.text(-0.7, -0.35, 'Y', fontsize=12, fontweight='bold')
    
    # Structural type annotation
    ax.text(1.0, -0.5, 'Trapezoidal Structure under Top Loading', 
           ha='center', va='center', fontsize=14, fontweight='bold', style='italic',
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightcyan', alpha=0.8))
    
    # Set axis properties
    ax.set_xlim(-0.8, 3.5)
    ax.set_ylim(-0.7, 1.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X Coordinate (m)', fontsize=12)
    ax.set_ylabel('Y Coordinate (m)', fontsize=12)
    
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('wzy_geometry_model.png', dpi=300, bbox_inches='tight')
    plt.savefig('wzy_geometry_model.pdf', bbox_inches='tight')
    
    print("WZY geometry model saved as:")
    print("- wzy_geometry_model.png")
    print("- wzy_geometry_model.pdf")
    
    # Print model summary
    print("\n" + "="*60)
    print("WZY TRAPEZOIDAL STRUCTURE - MODEL SUMMARY")
    print("="*60)
    print("Geometry:")
    print("- Shape: Trapezoidal structure")
    print("- Bottom width: 2.0 m")
    print("- Top width: 2.0 m") 
    print("- Height: 1.0 m (left), 0.5 m offset (right)")
    print("\nFinite Element Discretization:")
    print("- Element type: T3 (3-node triangle)")
    print("- Number of elements: 2")
    print("- Number of nodes: 4")
    print("\nBoundary Conditions:")
    print("- Node 1 (0.0, 0.0): Fixed support (Ux=Uy=0)")
    print("- Node 4 (0.0, 1.0): Fixed support (Ux=Uy=0)")
    print("- Node 2 (2.0, 0.5): Free")
    print("- Node 3 (2.0, 1.0): Free")
    print("\nLoading:")
    print("- Node 3: 20N downward (-Y direction)")
    print("- Node 4: 20N downward (-Y direction)")
    print("- Total load: 40N downward")
    print("\nMaterial Properties:")
    print("- Young's modulus: E = 3.0×10⁷ Pa")
    print("- Poisson's ratio: ν = 0.3")
    print("- Thickness: t = 1.0 m")
    print("="*60)

def main():
    """Main function to create WZY geometry visualization"""
    print("Creating WZY Trapezoidal Structure Geometry Model...")
    print("="*60)
    
    create_wzy_geometry()
    
    print("\nGeometry model creation completed!")
    print("Move the generated file to your img/ directory:")
    print("mv wzy_geometry_model.png ../writing/img/")
    print("="*60)

if __name__ == "__main__":
    main()