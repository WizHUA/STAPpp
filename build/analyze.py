#!/usr/bin/env python3
"""T3单元验证结果分析工具 - 修复版"""

import numpy as np
import re
import os

def parse_stap_output_fixed(filename):
    """修复的STAPpp输出文件解析"""
    displacements = {}
    stresses = {}
    
    if not os.path.exists(filename):
        print(f"   ❌ 文件不存在: {filename}")
        return displacements, stresses
    
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"   ❌ 读取文件失败: {e}")
        return displacements, stresses
    
    print(f"   📁 分析文件: {os.path.basename(filename)} ({len(content)} 字符)")
    
    # 检查程序是否正常完成
    if "SOLUTION   TIME" in content:
        print(f"   ✅ 程序正常完成")
    else:
        print(f"   ⚠️  程序可能未正常完成")
        # 查找错误信息
        if "Error" in content:
            error_lines = [line.strip() for line in content.split('\n') 
                          if 'Error' in line]
            for error_line in error_lines[:3]:
                print(f"      错误: {error_line}")
    
    # 解析位移数据 - 使用更精确的模式
    disp_pattern = r'D I S P L A C E M E N T S\s*\n.*?\n.*?\n(.*?)(?=\n\s*\n|\n\s*S T R E S S|$)'
    disp_match = re.search(disp_pattern, content, re.DOTALL)
    
    if disp_match:
        disp_text = disp_match.group(1)
        print(f"   📊 找到位移数据段")
        
        displacement_count = 0
        for line in disp_text.split('\n'):
            line = line.strip()
            if line and not line.startswith('NODE'):
                # 匹配格式: NODE X-DISPLACEMENT Y-DISPLACEMENT Z-DISPLACEMENT
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        node = int(parts[0])
                        ux = float(parts[1])
                        uy = float(parts[2])
                        displacements[node] = {'ux': ux, 'uy': uy}
                        displacement_count += 1
                    except (ValueError, IndexError):
                        continue
        
        print(f"   📊 成功解析 {displacement_count} 个节点的位移")
        if displacement_count > 0:
            # 显示前几个位移值
            sample_nodes = list(displacements.keys())[:3]
            for node in sample_nodes:
                ux, uy = displacements[node]['ux'], displacements[node]['uy']
                print(f"      节点 {node}: ux={ux:.6e}, uy={uy:.6e}")
    else:
        print(f"   ❌ 未找到位移数据段")
    
    # 解析应力数据 - 使用更精确的模式
    stress_pattern = r'S T R E S S  C A L C U L A T I O N S.*?\n.*?\n.*?\n.*?\n(.*?)(?=\n\s*\n|$)'
    stress_match = re.search(stress_pattern, content, re.DOTALL)
    
    if stress_match:
        stress_text = stress_match.group(1)
        print(f"   📊 找到应力数据段")
        
        stress_count = 0
        for line in stress_text.split('\n'):
            line = line.strip()
            if line and not line.startswith('ELEMENT'):
                # 匹配格式: ELEMENT STRESS_XX STRESS_YY STRESS_XY
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        element = int(parts[0])
                        sxx = float(parts[1])
                        syy = float(parts[2])
                        sxy = float(parts[3])
                        stresses[element] = {'sxx': sxx, 'syy': syy, 'sxy': sxy}
                        stress_count += 1
                    except (ValueError, IndexError):
                        continue
        
        print(f"   📊 成功解析 {stress_count} 个单元的应力")
        if stress_count > 0:
            # 显示前几个应力值
            sample_elements = list(stresses.keys())[:3]
            for elem in sample_elements:
                sxx, syy, sxy = stresses[elem]['sxx'], stresses[elem]['syy'], stresses[elem]['sxy']
                print(f"      单元 {elem}: σxx={sxx:.2e}, σyy={syy:.2e}, τxy={sxy:.2e}")
    else:
        print(f"   ❌ 未找到应力数据段")
    
    return displacements, stresses

def comprehensive_analysis():
    """综合分析所有测试结果"""
    print("T3单元验证结果综合分析")
    print("="*60)
    
    test_cases = {
        'patch_constant_strain': {
            'file': '../data/results_t3_patch_constant_strain.out',
            'description': '常应变拉伸试验'
        },
        'patch_pure_shear': {
            'file': '../data/results_t3_patch_pure_shear.out',
            'description': '纯剪切试验'
        },
        'cantilever_coarse': {
            'file': '../data/results_t3_cantilever_coarse.out',
            'description': '粗网格悬臂梁'
        },
        'cook_membrane': {
            'file': '../data/results_t3_cook_membrane.out',
            'description': 'Cook膜问题'
        }
    }
    
    results = {}
    
    # 解析所有测试文件
    for test_name, test_info in test_cases.items():
        print(f"\n{test_info['description']}:")
        print("-" * 40)
        
        disp, stress = parse_stap_output_fixed(test_info['file'])
        results[test_name] = {'displacements': disp, 'stresses': stress}
    
    print("\n验证分析:")
    print("="*60)
    
    # 1. 分片试验分析
    print("\n1. 分片试验验证:")
    
    # 常应变试验
    if results['patch_constant_strain']['stresses']:
        stress_data = results['patch_constant_strain']['stresses']
        print(f"   常应变试验 - 应力分布:")
        
        sxx_values = [s['sxx'] for s in stress_data.values()]
        syy_values = [s['syy'] for s in stress_data.values()]
        sxy_values = [s['sxy'] for s in stress_data.values()]
        
        for elem, s in stress_data.items():
            print(f"   单元 {elem}: σxx={s['sxx']:.2f}, σyy={s['syy']:.2f}, τxy={s['sxy']:.2f}")
        
        # 检查应力一致性
        if len(sxx_values) > 1:
            sxx_std = np.std(sxx_values)
            syy_std = np.std(syy_values)
            sxy_std = np.std(sxy_values)
            print(f"   应力标准差: σxx={sxx_std:.2e}, σyy={syy_std:.2e}, τxy={sxy_std:.2e}")
            
            tolerance = 1e-6
            if sxx_std < tolerance and syy_std < tolerance and sxy_std < tolerance:
                print("   ✅ 常应变试验通过：所有单元应力一致")
            else:
                print("   ❌ 常应变试验未通过：单元间应力不一致")
    else:
        print("   ❌ 常应变试验：无有效应力数据")
    
    # 纯剪切试验
    if results['patch_pure_shear']['stresses']:
        stress_data = results['patch_pure_shear']['stresses']
        print(f"\n   纯剪切试验 - 应力分布:")
        
        for elem, s in stress_data.items():
            print(f"   单元 {elem}: σxx={s['sxx']:.2f}, σyy={s['syy']:.2f}, τxy={s['sxy']:.2f}")
        
        # 检查正应力是否接近零
        normal_stress_max = max([abs(s['sxx']) for s in stress_data.values()] + 
                              [abs(s['syy']) for s in stress_data.values()])
        if normal_stress_max < 1e-3:
            print("   ✅ 纯剪切试验通过：正应力接近零")
        else:
            print("   ❌ 纯剪切试验未通过：存在较大正应力")
    else:
        print("   ❌ 纯剪切试验：无有效应力数据")
    
    # 2. 收敛性分析
    print("\n2. 收敛性分析:")
    
    if results['cantilever_coarse']['displacements']:
        disp_data = results['cantilever_coarse']['displacements']
        
        # 理论解
        L, h, t = 2.0, 2.0, 0.1
        P = 1000.0
        E = 2.1e5
        I = t * h**3 / 12
        theoretical_disp = P * L**3 / (3 * E * I)
        
        print(f"   理论解（Euler-Bernoulli梁）: {theoretical_disp:.6f} m")
        
        # 找到最大Y位移（末端位移）
        max_disp_node = max(disp_data.keys(), 
                           key=lambda n: abs(disp_data[n]['uy']))
        tip_disp = abs(disp_data[max_disp_node]['uy'])
        error = abs(tip_disp - theoretical_disp) / theoretical_disp * 100
        
        print(f"   粗网格结果:")
        print(f"   末端节点: {max_disp_node}")
        print(f"   末端位移: {tip_disp:.6f} m")
        print(f"   相对误差: {error:.2f}%")
        
        if error < 50:
            print("   ✅ 收敛性测试通过：误差在可接受范围内")
        else:
            print("   ⚠️  收敛性测试：误差较大")
    else:
        print("   ❌ 悬臂梁分析：无有效位移数据")
    
    # 3. Cook膜问题分析
    print("\n3. Cook膜问题:")
    
    if results['cook_membrane']['displacements']:
        disp_data = results['cook_membrane']['displacements']
        
        max_disp = max([abs(d['ux']) + abs(d['uy']) for d in disp_data.values()])
        print(f"   最大位移幅值: {max_disp:.6f} m")
        
        # 找到主要变形节点
        significant_nodes = [node for node, d in disp_data.items() 
                           if (abs(d['ux']) + abs(d['uy'])) > max_disp * 0.5]
        print(f"   主要变形节点: {significant_nodes}")
        print("   ✅ Cook膜问题求解成功")
    else:
        print("   ❌ Cook膜分析：无有效位移数据")

if __name__ == "__main__":
    comprehensive_analysis()
    print("\n分析完成！")
    print("="*60)