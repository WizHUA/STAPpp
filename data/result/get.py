#!/usr/bin/env python3
"""
STAPpp Output File Parser
解析STAPpp输出文件，提取几何、载荷、位移和应力信息
Usage: python3 get.py xxx.out
"""

import sys
import os
import re
import json
import numpy as np

def parse_stappp_output(filepath):
    """解析STAPpp输出文件"""
    
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found!")
        return None
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'TITLE\s*:\s*(.+)', content)
    title = title_match.group(1).strip() if title_match else "Unknown"
    
    # 提取控制信息
    numnp_match = re.search(r'NUMBER OF NODAL POINTS.*?=\s*(\d+)', content)
    numeg_match = re.search(r'NUMBER OF ELEMENT GROUPS.*?=\s*(\d+)', content)
    nlcase_match = re.search(r'NUMBER OF LOAD CASES.*?=\s*(\d+)', content)
    
    num_nodes = int(numnp_match.group(1)) if numnp_match else 0
    num_element_groups = int(numeg_match.group(1)) if numeg_match else 0
    num_load_cases = int(nlcase_match.group(1)) if nlcase_match else 0
    
    # 解析节点数据
    nodes = parse_nodal_data(content, num_nodes)
    
    # 解析载荷数据
    loads = parse_load_data(content)
    
    # 解析单元数据
    elements = parse_element_data(content)
    
    # 解析位移结果
    displacements = parse_displacement_results(content, num_nodes)
    
    # 解析应力结果
    stresses = parse_stress_results(content)
    
    # 构建数据结构
    result = {
        'title': title,
        'control_info': {
            'num_nodes': num_nodes,
            'num_element_groups': num_element_groups,
            'num_load_cases': num_load_cases
        },
        'nodes': nodes,
        'loads': loads,
        'elements': elements,
        'displacements': displacements,
        'stresses': stresses
    }
    
    return result

def parse_nodal_data(content, num_nodes):
    """解析节点数据"""
    nodes = {}
    
    # 查找节点数据部分
    node_section = re.search(r'N O D A L   P O I N T   D A T A.*?NODE.*?COORDINATES(.*?)EQUATION NUMBERS', 
                            content, re.DOTALL)
    
    if node_section:
        node_lines = node_section.group(1).strip().split('\n')
        for line in node_lines:
            line = line.strip()
            if not line or 'NODE' in line or 'NUMBER' in line:
                continue
            
            # 解析节点行: NODE BC_X BC_Y BC_Z X Y Z
            parts = line.split()
            if len(parts) >= 7:
                try:
                    node_id = int(parts[0])
                    bc_x, bc_y, bc_z = int(parts[1]), int(parts[2]), int(parts[3])
                    x, y, z = float(parts[4]), float(parts[5]), float(parts[6])
                    
                    nodes[node_id] = {
                        'id': node_id,
                        'x': x, 'y': y, 'z': z,
                        'bc_x': bc_x, 'bc_y': bc_y, 'bc_z': bc_z
                    }
                except ValueError:
                    continue
    
    return nodes

def parse_load_data(content):
    """解析载荷数据"""
    loads = {}
    
    # 查找载荷数据部分
    load_section = re.search(r'L O A D   C A S E   D A T A.*?NODE.*?MAGNITUDE(.*?)E L E M E N T', 
                            content, re.DOTALL)
    
    if load_section:
        load_lines = load_section.group(1).strip().split('\n')
        for line in load_lines:
            line = line.strip()
            if not line or 'NODE' in line or 'NUMBER' in line:
                continue
            
            # 解析载荷行: NODE DIRECTION MAGNITUDE
            parts = line.split()
            if len(parts) >= 3:
                try:
                    node_id = int(parts[0])
                    direction = int(parts[1])
                    magnitude = float(parts[2])
                    
                    if node_id not in loads:
                        loads[node_id] = {}
                    loads[node_id][direction] = magnitude
                except ValueError:
                    continue
    
    return loads

def parse_element_data(content):
    """解析单元数据"""
    elements = {}
    
    # 查找单元定义部分
    element_section = re.search(r'ELEMENT.*?NUMBER.*?SET NUMBER(.*?)TOTAL SYSTEM DATA', 
                               content, re.DOTALL)
    
    if element_section:
        element_lines = element_section.group(1).strip().split('\n')
        for line in element_lines:
            line = line.strip()
            if not line or 'ELEMENT' in line or 'NUMBER' in line or 'Ele' in line:
                continue
            
            # 解析单元行: ELEMENT_ID NODE_I NODE_J NODE_K MATERIAL_SET
            parts = line.split()
            if len(parts) >= 5:
                try:
                    elem_id = int(parts[0])
                    node_i = int(parts[1])
                    node_j = int(parts[2])
                    node_k = int(parts[3])
                    material_set = int(parts[4])
                    
                    elements[elem_id] = {
                        'id': elem_id,
                        'nodes': [node_i, node_j, node_k],
                        'material_set': material_set
                    }
                except ValueError:
                    continue
    
    return elements

def parse_displacement_results(content, num_nodes):
    """解析位移结果"""
    displacements = {}
    
    # 查找位移结果部分
    disp_section = re.search(r'D I S P L A C E M E N T S.*?NODE.*?Z-DISPLACEMENT(.*?)S T R E S S', 
                            content, re.DOTALL)
    
    if disp_section:
        disp_lines = disp_section.group(1).strip().split('\n')
        for line in disp_lines:
            line = line.strip()
            if not line or 'NODE' in line:
                continue
            
            # 解析位移行: NODE UX UY UZ
            parts = line.split()
            if len(parts) >= 4:
                try:
                    node_id = int(parts[0])
                    ux = float(parts[1])
                    uy = float(parts[2])
                    uz = float(parts[3])
                    
                    displacements[node_id] = {
                        'ux': ux, 'uy': uy, 'uz': uz
                    }
                except ValueError:
                    continue
    
    return displacements

def parse_stress_results(content):
    """解析应力结果"""
    stresses = {}
    
    # 查找应力结果部分
    stress_section = re.search(r'S T R E S S  C A L C U L A T I O N S.*?ELEMENT.*?STRESS_XY(.*?)S O L U T I O N', 
                              content, re.DOTALL)
    
    if stress_section:
        stress_lines = stress_section.group(1).strip().split('\n')
        for line in stress_lines:
            line = line.strip()
            if not line or 'ELEMENT' in line or 'NUMBER' in line:
                continue
            
            # 解析应力行: ELEMENT SXX SYY SXY
            parts = line.split()
            if len(parts) >= 4:
                try:
                    elem_id = int(parts[0])
                    sxx = float(parts[1])
                    syy = float(parts[2])
                    sxy = float(parts[3])
                    
                    stresses[elem_id] = {
                        'sxx': sxx, 'syy': syy, 'sxy': sxy
                    }
                except ValueError:
                    continue
    
    return stresses

def save_parsed_data(data, output_path):
    """保存解析后的数据到JSON文件"""
    
    # 转换为可序列化的格式
    serializable_data = convert_to_serializable(data)
    
    # 保存为JSON
    json_path = output_path.replace('.out', '_parsed.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(serializable_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Parsed data saved to: {json_path}")
    
    # 生成配置摘要
    summary_path = output_path.replace('.out', '_summary.txt')
    generate_summary(data, summary_path)
    
    return json_path

def convert_to_serializable(obj):
    """转换数据为JSON可序列化格式"""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    else:
        return obj

def generate_summary(data, summary_path):
    """生成解析摘要"""
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(f"STAPpp Output Analysis Summary\n")
        f.write("="*70 + "\n")
        f.write(f"Title: {data['title']}\n\n")
        
        f.write("GEOMETRY INFORMATION:\n")
        f.write("-"*40 + "\n")
        f.write(f"Number of Nodes: {data['control_info']['num_nodes']}\n")
        f.write(f"Number of Elements: {len(data['elements'])}\n")
        f.write(f"Number of Load Cases: {data['control_info']['num_load_cases']}\n\n")
        
        f.write("NODE COORDINATES:\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Node':<4} {'X':<10} {'Y':<10} {'Z':<10} {'BC':<8}\n")
        for node_id, node in sorted(data['nodes'].items()):
            bc_str = f"{node['bc_x']}{node['bc_y']}{node['bc_z']}"
            f.write(f"{node_id:<4} {node['x']:<10.3f} {node['y']:<10.3f} {node['z']:<10.3f} {bc_str:<8}\n")
        
        f.write("\nLOAD CONFIGURATION:\n")
        f.write("-"*40 + "\n")
        if data['loads']:
            f.write(f"{'Node':<4} {'Dir':<3} {'Magnitude':<12}\n")
            for node_id, load_dict in sorted(data['loads'].items()):
                for direction, magnitude in load_dict.items():
                    f.write(f"{node_id:<4} {direction:<3} {magnitude:<12.3f}\n")
        else:
            f.write("No loads applied\n")
        
        f.write("\nELEMENT CONNECTIVITY:\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Elem':<4} {'Node_I':<6} {'Node_J':<6} {'Node_K':<6}\n")
        for elem_id, elem in sorted(data['elements'].items()):
            nodes = elem['nodes']
            f.write(f"{elem_id:<4} {nodes[0]:<6} {nodes[1]:<6} {nodes[2]:<6}\n")
        
        f.write("\nDISPLACEMENT RESULTS:\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Node':<4} {'UX(mm)':<12} {'UY(mm)':<12} {'UZ(mm)':<12} {'Mag(mm)':<12}\n")
        for node_id, disp in sorted(data['displacements'].items()):
            ux_mm = disp['ux'] * 1000
            uy_mm = disp['uy'] * 1000
            uz_mm = disp['uz'] * 1000
            mag_mm = np.sqrt(ux_mm**2 + uy_mm**2 + uz_mm**2)
            f.write(f"{node_id:<4} {ux_mm:<12.3f} {uy_mm:<12.3f} {uz_mm:<12.3f} {mag_mm:<12.3f}\n")
        
        f.write("\nSTRESS RESULTS:\n")
        f.write("-"*40 + "\n")
        f.write(f"{'Elem':<4} {'SXX(Pa)':<12} {'SYY(Pa)':<12} {'SXY(Pa)':<12} {'Mises(Pa)':<12}\n")
        for elem_id, stress in sorted(data['stresses'].items()):
            sxx, syy, sxy = stress['sxx'], stress['syy'], stress['sxy']
            mises = np.sqrt(sxx**2 + syy**2 - sxx*syy + 3*sxy**2)
            f.write(f"{elem_id:<4} {sxx:<12.2f} {syy:<12.2f} {sxy:<12.2f} {mises:<12.2f}\n")
    
    print(f"✓ Summary saved to: {summary_path}")

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("Usage: python3 get.py xxx.out")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not input_file.endswith('.out'):
        print("Error: Input file must be a .out file")
        sys.exit(1)
    
    print(f"Parsing STAPpp output file: {input_file}")
    print("="*50)
    
    # 解析输出文件
    parsed_data = parse_stappp_output(input_file)
    
    if parsed_data is None:
        print("Failed to parse the output file!")
        sys.exit(1)
    
    # 保存解析结果
    json_path = save_parsed_data(parsed_data, input_file)
    
    print("\n" + "="*50)
    print("Parsing completed successfully!")
    print(f"Title: {parsed_data['title']}")
    print(f"Nodes: {len(parsed_data['nodes'])}")
    print(f"Elements: {len(parsed_data['elements'])}")
    print(f"Loads: {len(parsed_data['loads'])}")
    print("="*50)

if __name__ == "__main__":
    main()