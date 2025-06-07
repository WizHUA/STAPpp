#!/usr/bin/env python3
"""T3单元测试结果分析工具"""

import os
import re
import numpy as np
from pathlib import Path

def parse_stap_output(filename):
    """解析STAPpp输出文件"""
    if not os.path.exists(filename):
        return None, None, None
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None, None, None
    
    # 检查是否包含错误信息
    if 'Error' in content or 'error' in content:
        print(f"⚠️ {filename} 包含错误信息")
    
    displacements = {}
    stresses = {}
    forces = {}
    
    # 解析位移数据
    in_displacement = False
    for line in content.split('\n'):
        line = line.strip()
        
        if 'D I S P L A C E M E N T S' in line:
            in_displacement = True
            continue
        elif 'S T R E S S' in line:
            in_displacement = False
            continue
        
        if in_displacement and line:
            parts = line.split()
            if len(parts) >= 4 and parts[0].isdigit():
                try:
                    node = int(parts[0])
                    ux = float(parts[1])
                    uy = float(parts[2])
                    displacements[node] = {'ux': ux, 'uy': uy}
                except:
                    pass
    
    # 解析应力数据
    in_stress = False
    for line in content.split('\n'):
        line = line.strip()
        
        if 'S T R E S S  C A L C U L A T I O N S' in line:
            in_stress = True
            continue
        elif line == '' and in_stress:
            break
        
        if in_stress and line:
            parts = line.split()
            if len(parts) >= 4 and parts[0].isdigit():
                try:
                    element = int(parts[0])
                    sxx = float(parts[1])
                    syy = float(parts[2])
                    sxy = float(parts[3])
                    stresses[element] = {'sxx': sxx, 'syy': syy, 'sxy': sxy}
                except:
                    pass
    
    return displacements, stresses, forces

def analyze_single_test(test_name):
    """分析单个测试结果"""
    filename = f"results_{test_name}.out"
    
    print(f"\n分析 {test_name}:")
    print("-" * 40)
    
    disp, stress, forces = parse_stap_output(filename)
    
    if disp is None:
        print("❌ 无法读取结果文件")
        return False
    
    if not disp and not stress:
        print("❌ 结果文件为空或格式错误")
        return False
    
    # 位移分析
    if disp:
        max_disp = 0
        for node, d in disp.items():
            total_disp = np.sqrt(d['ux']**2 + d['uy']**2)
            max_disp = max(max_disp, total_disp)
        
        print(f"最大位移: {max_disp:.6e} m")
        
        if max_disp > 1.0:
            print("⚠️ 位移过大，可能有问题")
        elif max_disp < 1e-15:
            print("⚠️ 位移过小，可能刚体约束过度")
    
    # 应力分析
    if stress:
        stress_values = list(stress.values())
        if stress_values:
            sxx_values = [s['sxx'] for s in stress_values]
            syy_values = [s['syy'] for s in stress_values]
            sxy_values = [s['sxy'] for s in stress_values]
            
            max_stress = max([max(np.abs(sxx_values)), max(np.abs(syy_values)), max(np.abs(sxy_values))])
            print(f"最大应力: {max_stress:.2e} Pa")
            
            if len(stress_values) > 1:
                sxx_std = np.std(sxx_values)
                print(f"σxx标准差: {sxx_std:.2e}")
            
            # 检查是否有异常应力值
            if max_stress > 1e9:
                print("⚠️ 应力值过大，可能有数值问题")
        
        print(f"单元数量: {len(stress)}")
    
    print("✅ 分析完成")
    return True

def main():
    """主分析函数"""
    print("========================================")
    print("T3单元测试结果分析")
    print("========================================")
    
    # 获取所有结果文件
    result_files = list(Path('.').glob('results_*.out'))
    
    if not result_files:
        print("❌ 未找到结果文件")
        print("请先运行 ./run_all_tests.sh")
        return
    
    print(f"找到 {len(result_files)} 个结果文件")
    
    # 分析每个测试
    success_count = 0
    for result_file in sorted(result_files):
        test_name = result_file.stem.replace('results_', '')
        if analyze_single_test(test_name):
            success_count += 1
    
    print(f"\n========================================")
    print(f"分析完成: {success_count}/{len(result_files)} 个测试成功")
    print("========================================")

if __name__ == "__main__":
    main()
