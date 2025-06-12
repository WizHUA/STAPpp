#!/usr/bin/env python3
"""
STAPpp Universal Results Visualization Script
通用STAPpp结果可视化脚本，自动解析.out文件并生成图片
Usage: python3 visualize_results.py xxx.out
"""

import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from pathlib import Path

# 确保draw目录存在
SCRIPT_DIR = Path(__file__).parent
RESULT_DIR = SCRIPT_DIR / "result"
RESULT_DIR.mkdir(parents=True, exist_ok=True)

def load_parsed_data(filepath):
    """加载解析后的数据，如果不存在则先解析"""
    
    # 生成JSON文件路径
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    dir_name = os.path.dirname(filepath)
    json_path = os.path.join(dir_name, f"{base_name}_parsed.json")
    
    if not os.path.exists(json_path):
        print(f"Parsed data not found at {json_path}")
        print("Please run get.py first to parse the output file:")
        print(f"python3 get.py {filepath}")
        return None
    
    # 加载JSON数据
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded parsed data from: {json_path}")
        return data
    except Exception as e:
        print(f"Error loading parsed data: {e}")
        return None

def create_visualization(data, output_prefix):
    """创建完整的可视化分析"""
    
    # 提取数据
    nodes = data['nodes']
    elements = data['elements']
    displacements = data['displacements']
    stresses = data['stresses']
    loads = data.get('loads', {})
    
    print(f"Processing {len(nodes)} nodes, {len(elements)} elements")
    
    # 调试信息
    print("Available nodes:", sorted([int(k) for k in nodes.keys()]))
    if elements:
        first_elem = list(elements.values())[0]
        print("Sample element nodes:", first_elem['nodes'])
    
    # 转换为numpy数组 - 修复索引问题
    node_ids = sorted([int(k) for k in nodes.keys()])  # 转换为整数列表并排序
    x = np.array([nodes[str(nid)]['x'] for nid in node_ids])
    y = np.array([nodes[str(nid)]['y'] for nid in node_ids])
    
    # 位移数据
    ux = np.array([displacements[str(nid)]['ux'] for nid in node_ids])
    uy = np.array([displacements[str(nid)]['uy'] for nid in node_ids])
    uz = np.array([displacements[str(nid)]['uz'] for nid in node_ids])
    
    # 创建三角剖分 - 修复索引转换
    triangles = []
    valid_elements = {}
    
    for elem_id, elem in elements.items():
        nodes_elem = elem['nodes']
        print(f"Processing element {elem_id} with nodes {nodes_elem}")
        
        # 检查所有节点是否存在
        valid_nodes = True
        for node in nodes_elem:
            if int(node) not in node_ids:
                print(f"Warning: Element {elem_id} references non-existent node {node}")
                valid_nodes = False
                break
        
        if valid_nodes:
            try:
                # 转换为从0开始的索引
                tri_indices = [node_ids.index(int(node)) for node in nodes_elem]
                triangles.append(tri_indices)
                valid_elements[elem_id] = elem
                print(f"✓ Element {elem_id}: nodes {nodes_elem} -> indices {tri_indices}")
            except ValueError as e:
                print(f"Error processing element {elem_id}: {e}")
        else:
            print(f"✗ Skipping invalid element {elem_id}")
    
    if not triangles:
        print("Error: No valid triangles found!")
        print("Available nodes:", node_ids)
        print("Element connectivity issues detected.")
        return
    
    print(f"✓ Created {len(triangles)} valid triangles")
    triangles = np.array(triangles)
    
    try:
        triang = tri.Triangulation(x, y, triangles)
        print("✓ Triangulation successful")
    except Exception as e:
        print(f"Error creating triangulation: {e}")
        return
    
    # 计算变形后坐标
    scale_factor = auto_scale_factor(x, y, ux, uy)
    x_def = x + ux * scale_factor
    y_def = y + uy * scale_factor
    triang_def = tri.Triangulation(x_def, y_def, triangles)
    
    # 位移幅值
    displacement_mag = np.sqrt(ux**2 + uy**2 + uz**2)
    
    # 创建可视化
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle(f'{data["title"]} - Analysis Results', fontsize=16, fontweight='bold')
    
    # 1. 原始网格
    ax1 = axes[0, 0]
    plot_original_mesh(ax1, triang, x, y, node_ids, loads)
    
    # 2. 变形对比
    ax2 = axes[0, 1]
    plot_deformation_comparison(ax2, triang, triang_def, x, y, x_def, y_def, 
                               ux, uy, displacement_mag, scale_factor)
    
    # 3. 位移矢量场
    ax3 = axes[0, 2]
    plot_displacement_vectors(ax3, triang, x, y, ux, uy, displacement_mag, scale_factor)
    
    # 4. X位移等值线
    ax4 = axes[1, 0]
    plot_displacement_contour(ax4, triang, x, y, ux*1e6, 'X-Displacement (μm)', 'RdBu_r')
    
    # 5. Y位移等值线
    ax5 = axes[1, 1]
    plot_displacement_contour(ax5, triang, x, y, uy*1e6, 'Y-Displacement (μm)', 'RdBu_r')
    
    # 6. 应力分布
    ax6 = axes[1, 2]
    plot_stress_distribution(ax6, triang, x, y, valid_elements, stresses, node_ids)
    
    plt.tight_layout()
    
    # 保存图片
    output_path = RESULT_DIR / f"{output_prefix}_analysis.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Analysis plot saved: {output_path}")
    
    output_path_pdf = RESULT_DIR / f"{output_prefix}_analysis.pdf"
    plt.savefig(output_path_pdf, bbox_inches='tight', facecolor='white')
    print(f"✓ Analysis plot saved: {output_path_pdf}")
    
    plt.show()
    
    # 创建详细应力分析
    if stresses:
        create_stress_analysis(data, output_prefix, valid_elements, node_ids)
    
    # 生成数据报告
    generate_analysis_report(data, output_prefix)

def auto_scale_factor(x, y, ux, uy):
    """自动计算变形缩放因子"""
    model_size = max(np.max(x) - np.min(x), np.max(y) - np.min(y))
    max_displacement = np.max(np.sqrt(ux**2 + uy**2))
    
    if max_displacement > 0:
        scale_factor = model_size * 0.1 / max_displacement
        # 限制缩放因子范围
        scale_factor = min(max(scale_factor, 50), 100000)
    else:
        scale_factor = 1000
    
    return scale_factor

def plot_original_mesh(ax, triang, x, y, node_ids, loads):
    """绘制原始网格"""
    ax.triplot(triang, 'b-', linewidth=2, alpha=0.8)
    ax.plot(x, y, 'bo', markersize=8)
    
    # 标注节点
    for i, node_id in enumerate(node_ids):
        ax.text(x[i], y[i], f'  {node_id}', fontsize=10, ha='left', va='bottom')
    
    # 绘制载荷箭头
    for node_id_str, load_dict in loads.items():
        node_id = int(node_id_str)
        if node_id in node_ids:
            idx = node_ids.index(node_id)
            for direction, magnitude in load_dict.items():
                arrow_scale = min(0.3, abs(magnitude)/1000)  # 调整箭头大小
                if direction == 1:  # X方向
                    dx = arrow_scale * np.sign(magnitude)
                    ax.arrow(x[idx], y[idx], dx, 0, head_width=0.05, head_length=0.03,
                            fc='red', ec='red', linewidth=2)
                    ax.text(x[idx] + dx*1.5, y[idx], f'{magnitude:.0f}N', 
                           fontsize=9, color='red', fontweight='bold', ha='center')
                elif direction == 2:  # Y方向
                    dy = arrow_scale * np.sign(magnitude)
                    ax.arrow(x[idx], y[idx], 0, dy, head_width=0.05, head_length=0.03,
                            fc='green', ec='green', linewidth=2)
                    ax.text(x[idx], y[idx] + dy*1.5, f'{magnitude:.0f}N', 
                           fontsize=9, color='green', fontweight='bold', ha='center')
    
    ax.set_title('Original Mesh with Loads', fontweight='bold')
    ax.set_xlabel('X Coordinate (m)')
    ax.set_ylabel('Y Coordinate (m)')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

def plot_deformation_comparison(ax, triang, triang_def, x, y, x_def, y_def, 
                               ux, uy, displacement_mag, scale_factor):
    """绘制变形对比"""
    ax.triplot(triang, 'b-', linewidth=2, alpha=0.6, label='Original')
    ax.triplot(triang_def, 'r--', linewidth=2, alpha=0.8, 
              label=f'Deformed (×{scale_factor:.0f})')
    ax.plot(x, y, 'bo', markersize=6)
    ax.plot(x_def, y_def, 'ro', markersize=6)
    
    # 绘制位移矢量
    for i in range(len(x)):
        if displacement_mag[i] > 1e-12:
            ax.arrow(x[i], y[i], ux[i]*scale_factor, uy[i]*scale_factor,
                    head_width=0.03, head_length=0.02, fc='purple', 
                    ec='purple', alpha=0.8)
    
    ax.set_title('Deformation Comparison', fontweight='bold')
    ax.set_xlabel('X Coordinate (m)')
    ax.set_ylabel('Y Coordinate (m)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

def plot_displacement_vectors(ax, triang, x, y, ux, uy, displacement_mag, scale_factor):
    """绘制位移矢量场"""
    ax.triplot(triang, 'k-', alpha=0.4)
    
    if np.max(displacement_mag) > 0:
        quiver = ax.quiver(x, y, ux*scale_factor, uy*scale_factor,
                          displacement_mag*1e6, scale=1, scale_units='xy',
                          angles='xy', cmap='viridis', alpha=0.8, width=0.003)
        cbar = plt.colorbar(quiver, ax=ax)
        cbar.set_label('Displacement Magnitude (μm)')
    
    ax.plot(x, y, 'ko', markersize=6)
    ax.set_title('Displacement Vector Field', fontweight='bold')
    ax.set_xlabel('X Coordinate (m)')
    ax.set_ylabel('Y Coordinate (m)')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')

def plot_displacement_contour(ax, triang, x, y, displacement, title, cmap):
    """绘制位移等值线"""
    if np.max(np.abs(displacement)) > 1e-10:
        try:
            contour = ax.tricontourf(triang, displacement, levels=20, cmap=cmap)
            cbar = plt.colorbar(contour, ax=ax)
            cbar.set_label(title)
        except:
            pass  # 如果等值线绘制失败，继续其他部分
    
    ax.triplot(triang, 'k-', alpha=0.3)
    ax.plot(x, y, 'ko', markersize=4)
    
    # 添加数值标注
    for i in range(len(x)):
        if abs(displacement[i]) < 1e6:  # 避免标注过大的数字
            ax.text(x[i], y[i]+0.05, f'{displacement[i]:.1f}', 
                   ha='center', va='bottom', fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('X Coordinate (m)')
    ax.set_ylabel('Y Coordinate (m)')
    ax.set_aspect('equal')

def plot_stress_distribution(ax, triang, x, y, elements, stresses, node_ids):
    """绘制应力分布"""
    # 计算单元中心和von Mises应力
    elem_centers = []
    von_mises = []
    
    for elem_id, elem in elements.items():
        nodes_elem = elem['nodes']
        # 获取节点在数组中的索引
        try:
            node_indices = [node_ids.index(int(node)) for node in nodes_elem]
            cx = np.mean([x[i] for i in node_indices])
            cy = np.mean([y[i] for i in node_indices])
            elem_centers.append([cx, cy])
            
            if str(elem_id) in stresses:
                stress = stresses[str(elem_id)]
                sxx, syy, sxy = stress['sxx'], stress['syy'], stress['sxy']
                vm = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
                von_mises.append(vm)
            else:
                von_mises.append(0.0)
        except ValueError:
            continue  # 跳过无效的单元
    
    if not elem_centers:
        ax.text(0.5, 0.5, 'No valid stress data', ha='center', va='center', 
                transform=ax.transAxes, fontsize=14)
        ax.triplot(triang, 'k-', alpha=0.5)
        ax.plot(x, y, 'ko', markersize=6)
        ax.set_title('von Mises Stress Distribution', fontweight='bold')
        ax.set_xlabel('X Coordinate (m)')
        ax.set_ylabel('Y Coordinate (m)')
        ax.set_aspect('equal')
        return
    
    elem_centers = np.array(elem_centers)
    
    # 绘制应力分布
    if len(von_mises) > 0 and np.max(von_mises) > 0:
        scatter = ax.scatter(elem_centers[:, 0], elem_centers[:, 1],
                           c=von_mises, s=300, cmap='jet', alpha=0.8)
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('von Mises Stress (Pa)')
        
        # 标注应力值
        for i, (center, vm) in enumerate(zip(elem_centers, von_mises)):
            ax.text(center[0], center[1], f'{vm:.1f}', ha='center', va='center',
                   fontsize=10, fontweight='bold', color='white')
    
    ax.triplot(triang, 'k-', alpha=0.5)
    ax.plot(x, y, 'ko', markersize=6)
    ax.set_title('von Mises Stress Distribution', fontweight='bold')
    ax.set_xlabel('X Coordinate (m)')
    ax.set_ylabel('Y Coordinate (m)')
    ax.set_aspect('equal')

def create_stress_analysis(data, output_prefix, elements, node_ids):
    """创建详细应力分析"""
    
    nodes = data['nodes']
    stresses = data['stresses']
    
    if not stresses:
        print("No stress data available for detailed analysis")
        return
    
    x = np.array([nodes[str(nid)]['x'] for nid in node_ids])
    y = np.array([nodes[str(nid)]['y'] for nid in node_ids])
    
    # 创建三角剖分
    triangles = []
    for elem_id, elem in elements.items():
        nodes_elem = elem['nodes']
        try:
            tri_indices = [node_ids.index(int(node)) for node in nodes_elem]
            triangles.append(tri_indices)
        except ValueError:
            continue
    
    if not triangles:
        print("No valid triangles for stress analysis")
        return
    
    triangles = np.array(triangles)
    triang = tri.Triangulation(x, y, triangles)
    
    # 计算单元中心和应力分量
    elem_centers = []
    stress_xx = []
    stress_yy = []
    stress_xy = []
    von_mises = []
    
    for elem_id, elem in elements.items():
        nodes_elem = elem['nodes']
        try:
            node_indices = [node_ids.index(int(node)) for node in nodes_elem]
            cx = np.mean([x[i] for i in node_indices])
            cy = np.mean([y[i] for i in node_indices])
            elem_centers.append([cx, cy])
            
            if str(elem_id) in stresses:
                stress = stresses[str(elem_id)]
                sxx, syy, sxy = stress['sxx'], stress['syy'], stress['sxy']
                stress_xx.append(sxx)
                stress_yy.append(syy)
                stress_xy.append(sxy)
                vm = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
                von_mises.append(vm)
            else:
                stress_xx.append(0.0)
                stress_yy.append(0.0)
                stress_xy.append(0.0)
                von_mises.append(0.0)
        except ValueError:
            continue
    
    elem_centers = np.array(elem_centers)
    
    # 创建应力分析图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'{data["title"]} - Detailed Stress Analysis', 
                 fontsize=16, fontweight='bold')
    
    stress_components = [
        (stress_xx, 'Sxx Stress (Pa)', 'RdBu_r'),
        (stress_yy, 'Syy Stress (Pa)', 'RdBu_r'),
        (stress_xy, 'Sxy Stress (Pa)', 'RdBu_r'),
        (von_mises, 'von Mises Stress (Pa)', 'jet')
    ]
    
    for i, (stress_data, title, cmap) in enumerate(stress_components):
        ax = axes[i//2, i%2]
        
        if len(stress_data) > 0 and np.max(np.abs(stress_data)) > 1e-10:
            scatter = ax.scatter(elem_centers[:, 0], elem_centers[:, 1],
                               c=stress_data, s=300, cmap=cmap, alpha=0.8)
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label(title)
            
            # 标注数值
            for j, (center, stress_val) in enumerate(zip(elem_centers, stress_data)):
                ax.text(center[0], center[1], f'{stress_val:.1f}', 
                       ha='center', va='center', fontsize=10, fontweight='bold', 
                       color='white')
        
        ax.triplot(triang, 'k-', alpha=0.5)
        ax.plot(x, y, 'ko', markersize=6)
        ax.set_title(title, fontweight='bold')
        ax.set_xlabel('X Coordinate (m)')
        ax.set_ylabel('Y Coordinate (m)')
        ax.set_aspect('equal')
    
    plt.tight_layout()
    
    # 保存应力分析图
    output_path = RESULT_DIR / f"{output_prefix}_stress_analysis.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Stress analysis plot saved: {output_path}")
    
    output_path_pdf = RESULT_DIR / f"{output_prefix}_stress_analysis.pdf"
    plt.savefig(output_path_pdf, bbox_inches='tight', facecolor='white')
    print(f"✓ Stress analysis plot saved: {output_path_pdf}")
    
    plt.show()

def generate_analysis_report(data, output_prefix):
    """生成分析报告"""
    
    report_path = RESULT_DIR / f"{output_prefix}_report.txt"
    
    nodes = data['nodes']
    elements = data['elements']
    displacements = data['displacements']
    stresses = data['stresses']
    loads = data.get('loads', {})
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(f"STAPpp Analysis Results Report\n")
        f.write("="*80 + "\n")
        f.write(f"Analysis Title: {data['title']}\n")
        f.write(f"Generated by: STAPpp Universal Visualization Script\n\n")
        
        f.write("PROBLEM CONFIGURATION:\n")
        f.write("-"*50 + "\n")
        f.write(f"Number of Nodes: {len(nodes)}\n")
        f.write(f"Number of Elements: {len(elements)}\n")
        f.write(f"Number of Load Cases: {data['control_info']['num_load_cases']}\n")
        f.write(f"Element Type: T3 Triangle\n\n")
        
        f.write("DISPLACEMENT RESULTS SUMMARY:\n")
        f.write("-"*50 + "\n")
        node_ids = sorted([int(k) for k in nodes.keys()])
        
        # 计算最大位移
        max_ux = max_uy = max_mag = 0
        for node_id in node_ids:
            if str(node_id) in displacements:
                disp = displacements[str(node_id)]
                ux_mm = abs(disp['ux'] * 1000)
                uy_mm = abs(disp['uy'] * 1000)
                mag_mm = np.sqrt((disp['ux']*1000)**2 + (disp['uy']*1000)**2)
                max_ux = max(max_ux, ux_mm)
                max_uy = max(max_uy, uy_mm)
                max_mag = max(max_mag, mag_mm)
        
        f.write(f"Maximum X-Displacement: {max_ux:.3f} mm\n")
        f.write(f"Maximum Y-Displacement: {max_uy:.3f} mm\n")
        f.write(f"Maximum Total Displacement: {max_mag:.3f} mm\n\n")
        
        f.write("STRESS RESULTS SUMMARY:\n")
        f.write("-"*50 + "\n")
        if stresses:
            stress_values = []
            for elem_id, stress in stresses.items():
                sxx, syy, sxy = stress['sxx'], stress['syy'], stress['sxy']
                vm = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
                stress_values.append({'sxx': sxx, 'syy': syy, 'sxy': sxy, 'vm': vm})
            
            if stress_values:
                max_sxx = max([abs(s['sxx']) for s in stress_values])
                max_syy = max([abs(s['syy']) for s in stress_values])
                max_sxy = max([abs(s['sxy']) for s in stress_values])
                max_vm = max([s['vm'] for s in stress_values])
                
                f.write(f"Maximum |Sxx|: {max_sxx:.2f} Pa\n")
                f.write(f"Maximum |Syy|: {max_syy:.2f} Pa\n")
                f.write(f"Maximum |Sxy|: {max_sxy:.2f} Pa\n")
                f.write(f"Maximum von Mises: {max_vm:.2f} Pa\n\n")
        
        f.write("DETAILED RESULTS:\n")
        f.write("-"*50 + "\n")
        f.write("Node Displacements:\n")
        f.write(f"{'Node':<4} {'UX(μm)':<12} {'UY(μm)':<12} {'Magnitude(μm)':<15}\n")
        f.write("-"*45 + "\n")
        for node_id in node_ids:
            if str(node_id) in displacements:
                disp = displacements[str(node_id)]
                ux_um = disp['ux'] * 1e6
                uy_um = disp['uy'] * 1e6
                mag_um = np.sqrt(ux_um**2 + uy_um**2)
                f.write(f"{node_id:<4} {ux_um:<12.3f} {uy_um:<12.3f} {mag_um:<15.3f}\n")
        
        f.write("\nElement Stresses:\n")
        f.write(f"{'Elem':<4} {'Sxx(Pa)':<12} {'Syy(Pa)':<12} {'Sxy(Pa)':<12} {'von Mises(Pa)':<15}\n")
        f.write("-"*60 + "\n")
        for elem_id in sorted([int(k) for k in elements.keys()]):
            if str(elem_id) in stresses:
                stress = stresses[str(elem_id)]
                sxx, syy, sxy = stress['sxx'], stress['syy'], stress['sxy']
                vm = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
                f.write(f"{elem_id:<4} {sxx:<12.2f} {syy:<12.2f} {sxy:<12.2f} {vm:<15.2f}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("End of Report\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Analysis report saved: {report_path}")

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("Usage: python3 visualize_results.py xxx.out")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not input_file.endswith('.out'):
        print("Error: Input file must be a .out file")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found!")
        sys.exit(1)
    
    # 获取输出前缀
    output_prefix = os.path.splitext(os.path.basename(input_file))[0]
    
    print(f"Processing STAPpp output file: {input_file}")
    print(f"Output directory: {RESULT_DIR}")
    print("="*60)
    
    # 加载数据
    data = load_parsed_data(input_file)
    
    if data is None:
        print("Failed to load parsed data!")
        sys.exit(1)
    
    # 创建可视化
    create_visualization(data, output_prefix)
    
    print("\n" + "="*60)
    print("Visualization completed successfully!")
    print(f"All results saved in: {RESULT_DIR}")
    print("Generated files:")
    print(f"  - {output_prefix}_analysis.png/pdf")
    if data.get('stresses'):
        print(f"  - {output_prefix}_stress_analysis.png/pdf")
    print(f"  - {output_prefix}_report.txt")
    print("="*60)

if __name__ == "__main__":
    main()