#!/usr/bin/env python3
"""T3单元验证结果分析工具"""

import numpy as np
import matplotlib.pyplot as plt
import re
import os

def parse_stap_output(filename):
    """解析STAPpp输出文件"""
    displacements = {}
    stresses = {}
    
    if not os.path.exists(filename):
        print(f"文件 {filename} 不存在")
        return displacements, stresses
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # 提取位移数据
    disp_section = re.search(r'D I S P L A C E M E N T S.*?(?=\n\n|\n S T R E S S|$)', content, re.DOTALL)
    if disp_section:
        lines = disp_section.group().split('\n')[3:]
        for line in lines:
            if line.strip() and not line.startswith('NODE'):
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        node = int(parts[0])
                        ux = float(parts[1])
                        uy = float(parts[2])
                        displacements[node] = {'ux': ux, 'uy': uy}
                    except (ValueError, IndexError):
                        continue
    
    # 提取应力数据
    stress_section = re.search(r'S T R E S S  C A L C U L A T I O N S.*?(?=\n\n|$)', content, re.DOTALL)
    if stress_section:
        lines = stress_section.group().split('\n')[4:]
        for line in lines:
            if line.strip() and not line.startswith('ELEMENT'):
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        element = int(parts[0])
                        sxx = float(parts[1])
                        syy = float(parts[2])
                        sxy = float(parts[3])
                        stresses[element] = {'sxx': sxx, 'syy': syy, 'sxy': sxy}
                    except (ValueError, IndexError):
                        continue
    
    return displacements, stresses

def patch_test_analysis():
    """分片试验分析"""
    print("分片试验结果分析:")
    print("="*60)
    
    # 常应变试验
    disp, stress = parse_stap_output("../data/results_t3_patch_constant_strain.out")
    print("\n1. 常应变拉伸试验:")
    if stress:
        stress_values = list(stress.values())
        sxx_values = [s['sxx'] for s in stress_values]
        syy_values = [s['syy'] for s in stress_values]
        sxy_values = [s['sxy'] for s in stress_values]
        
        print(f"   应力分布（所有单元应相同）:")
        for elem, s in stress.items():
            print(f"   单元 {elem}: σxx={s['sxx']:.2f}, σyy={s['syy']:.2f}, τxy={s['sxy']:.2f}")
        
        # 检查应力一致性
        sxx_std = np.std(sxx_values) if len(sxx_values) > 1 else 0
        syy_std = np.std(syy_values) if len(syy_values) > 1 else 0
        sxy_std = np.std(sxy_values) if len(sxy_values) > 1 else 0
        
        print(f"   应力标准差: σxx={sxx_std:.2e}, σyy={syy_std:.2e}, τxy={sxy_std:.2e}")
        
        tolerance = 1e-6
        if sxx_std < tolerance and syy_std < tolerance and sxy_std < tolerance:
            print("   ✅ 常应变试验通过：所有单元应力一致")
        else:
            print("   ❌ 常应变试验未通过：单元间应力不一致")
    else:
        print("   ❌ 无法读取应力数据")
    
    # 纯剪切试验
    print("\n2. 纯剪切试验:")
    disp, stress = parse_stap_output("../data/results_t3_patch_pure_shear.out")
    if stress:
        print(f"   剪切应力分布:")
        for elem, s in stress.items():
            print(f"   单元 {elem}: σxx={s['sxx']:.2f}, σyy={s['syy']:.2f}, τxy={s['sxy']:.2f}")
        
        # 检查正应力是否接近零
        normal_stress_max = max([abs(s['sxx']) for s in stress.values()] + 
                              [abs(s['syy']) for s in stress.values()])
        if normal_stress_max < 1e-3:
            print("   ✅ 纯剪切试验通过：正应力接近零")
        else:
            print("   ❌ 纯剪切试验未通过：存在较大正应力")
    else:
        print("   ❌ 无法读取应力数据")

def convergence_analysis():
    """收敛性分析"""
    print("\n收敛性分析:")
    print("="*60)
    
    # 理论解计算
    L, h, t = 2.0, 2.0, 0.1  # 长度，高度，厚度
    P = 1000.0  # 载荷
    E = 2.1e5   # 弹性模量
    I = t * h**3 / 12  # 惯性矩
    theoretical_disp = P * L**3 / (3 * E * I)
    
    print(f"理论解（Euler-Bernoulli梁）: {theoretical_disp:.6f} m")
    
    # 分析粗网格结果
    mesh_name = 'coarse'
    filename = f"../data/results_t3_cantilever_{mesh_name}.out"
    try:
        displacements, _ = parse_stap_output(filename)
        if displacements:
            # 找到最右上角节点（末端节点）
            max_x_nodes = [node for node, disp in displacements.items() 
                          if abs(disp['ux']) > 1e-10 or abs(disp['uy']) > 1e-10]
            if max_x_nodes:
                tip_node = max(max_x_nodes)  # 假设节点编号最大的是末端
                tip_disp = abs(displacements[tip_node]['uy'])
                error = abs(tip_disp - theoretical_disp) / theoretical_disp * 100
                
                print(f"\n粗网格结果:")
                print(f"   末端节点: {tip_node}")
                print(f"   末端位移: {tip_disp:.6f} m")
                print(f"   相对误差: {error:.2f}%")
                
                if error < 50:  # 50%以内的误差是可接受的
                    print("   ✅ 收敛性测试通过：误差在可接受范围内")
                else:
                    print("   ⚠️  收敛性测试：误差较大，建议使用更细网格")
            else:
                print(f"   ❌ 无法找到有效的末端节点")
        else:
            print(f"   ❌ 无法读取位移数据")
    except Exception as e:
        print(f"   ❌ 分析失败: {e}")

def cook_membrane_analysis():
    """Cook膜问题分析"""
    print("\nCook膜问题分析:")
    print("="*60)
    
    disp, stress = parse_stap_output("../data/results_t3_cook_membrane.out")
    
    if disp:
        # 找到受载节点的位移
        max_disp = max([abs(d['ux']) + abs(d['uy']) for d in disp.values()])
        print(f"   最大位移幅值: {max_disp:.6f} m")
        
        # Cook膜的典型特征：上角点有较大位移
        upper_nodes = [node for node, d in disp.items() if abs(d['uy']) > max_disp * 0.5]
        if upper_nodes:
            print(f"   主要变形节点: {upper_nodes}")
            print("   ✅ Cook膜问题求解成功")
        else:
            print("   ❌ Cook膜变形模式异常")
    else:
        print("   ❌ 无法读取Cook膜位移数据")

if __name__ == "__main__":
    print("T3单元验证结果分析")
    print("="*60)
    
    # 运行分析
    patch_test_analysis()
    convergence_analysis()
    cook_membrane_analysis()
    
    print("\n分析完成！")
    print("="*60)