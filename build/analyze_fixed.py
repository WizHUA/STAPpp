#!/usr/bin/env python3
"""T3单元验证分析工具 - 最终修正版"""

import numpy as np
import re
import os

def parse_stap_debug_output(filename):
    """解析带调试信息的STAPpp输出"""
    displacements = {}
    stresses = {}
    debug_info = {}
    
    if not os.path.exists(filename):
        print(f"❌ 文件不存在: {filename}")
        return displacements, stresses, debug_info
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return displacements, stresses, debug_info
    
    # 解析调试信息中的B矩阵
    b_matrix_pattern = r'B matrix:.*?\n((?:\s*\[.*?\]\n){3})'
    b_matches = re.findall(b_matrix_pattern, content, re.DOTALL)
    if b_matches:
        debug_info['b_matrices'] = b_matches
    
    # 解析位移
    disp_pattern = r'D I S P L A C E M E N T S.*?\n.*?\n(.*?)(?=\n\s*S T R E S S|\n\s*\n|$)'
    disp_match = re.search(disp_pattern, content, re.DOTALL)
    
    if disp_match:
        for line in disp_match.group(1).strip().split('\n'):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    node = int(parts[0])
                    ux, uy = float(parts[1]), float(parts[2])
                    displacements[node] = {'ux': ux, 'uy': uy}
                except ValueError:
                    continue
    
    # 解析应力
    stress_pattern = r'S T R E S S  C A L C U L A T I O N S.*?\n.*?\n.*?\n(.*?)(?=\n\s*\n|$)'
    stress_match = re.search(stress_pattern, content, re.DOTALL)
    
    if stress_match:
        for line in stress_match.group(1).strip().split('\n'):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    elem = int(parts[0])
                    sxx, syy, sxy = float(parts[1]), float(parts[2]), float(parts[3])
                    stresses[elem] = {'sxx': sxx, 'syy': syy, 'sxy': sxy}
                except ValueError:
                    continue
    
    return displacements, stresses, debug_info

def theoretical_analysis():
    """理论分析验证"""
    print("理论验证分析:")
    print("="*50)
    
    # 几何参数
    print("几何配置:")
    print("  节点1: (0,0)")
    print("  节点2: (1,0)")  
    print("  节点3: (1,1)")
    print("  节点4: (0,1)")
    print("  单元1: 1-2-3 (右下三角)")
    print("  单元2: 1-3-4 (左上三角)")
    
    # 形函数系数理论计算
    print("\n理论形函数系数:")
    
    # 单元1: (0,0), (1,0), (1,1)
    x1, y1 = 0, 0
    x2, y2 = 1, 0
    x3, y3 = 1, 1
    
    area1 = 0.5 * abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))
    a1 = [x2*y3 - x3*y2, x3*y1 - x1*y3, x1*y2 - x2*y1]
    b1 = [y2-y3, y3-y1, y1-y2]
    c1 = [x3-x2, x1-x3, x2-x1]
    
    print(f"  单元1 (面积={area1}):")
    print(f"    a: {a1}")
    print(f"    b: {b1}")
    print(f"    c: {c1}")
    print(f"    验证: sum(a)={sum(a1)}, 2*area={2*area1}")
    
    # 单元2: (0,0), (1,1), (0,1)
    x1, y1 = 0, 0
    x2, y2 = 1, 1
    x3, y3 = 0, 1
    
    area2 = 0.5 * abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))
    a2 = [x2*y3 - x3*y2, x3*y1 - x1*y3, x1*y2 - x2*y1]
    b2 = [y2-y3, y3-y1, y1-y2]
    c2 = [x3-x2, x1-x3, x2-x1]
    
    print(f"  单元2 (面积={area2}):")
    print(f"    a: {a2}")
    print(f"    b: {b2}")
    print(f"    c: {c2}")
    print(f"    验证: sum(a)={sum(a2)}, 2*area={2*area2}")
    
    # 常应变试验理论
    print(f"\n常应变试验理论:")
    E, nu, t = 210000, 0.3, 0.01
    total_force = 2000  # N
    total_area = 1.0 * t  # m²
    
    theoretical_strain_xx = total_force / (E * total_area)
    theoretical_stress_xx = E * theoretical_strain_xx
    theoretical_stress_yy = 0  # 平面应力
    theoretical_stress_xy = 0  # 无剪切
    
    print(f"  载荷: {total_force} N")
    print(f"  截面积: {total_area} m²")
    print(f"  理论应变εxx: {theoretical_strain_xx:.6e}")
    print(f"  理论应力σxx: {theoretical_stress_xx:.0f} Pa")
    print(f"  理论应力σyy: {theoretical_stress_yy} Pa")
    print(f"  理论应力τxy: {theoretical_stress_xy} Pa")
    
    return theoretical_stress_xx, theoretical_stress_yy, theoretical_stress_xy

def comprehensive_patch_test_analysis():
    """综合分片试验分析"""
    print("T3单元分片试验综合分析")
    print("="*60)
    
    # 理论分析
    theo_sxx, theo_syy, theo_sxy = theoretical_analysis()
    
    # 常应变试验分析
    print("\n常应变分片试验结果:")
    print("="*50)
    
    disp, stress, debug = parse_stap_debug_output('../data/results_t3_patch_constant_strain_standard.out')
    
    if stress:
        print("实际应力结果:")
        errors_sxx = []
        all_sxx = []
        all_syy = []
        all_sxy = []
        
        for elem, s in stress.items():
            sxx, syy, sxy = s['sxx'], s['syy'], s['sxy']
            all_sxx.append(sxx)
            all_syy.append(syy)
            all_sxy.append(sxy)
            
            error_sxx = abs(sxx - theo_sxx) / abs(theo_sxx) * 100
            errors_sxx.append(error_sxx)
            
            print(f"  单元 {elem}: σxx={sxx:.0f} Pa (误差{error_sxx:.1f}%), "
                  f"σyy={syy:.0f} Pa, τxy={sxy:.0f} Pa")
        
        # 统计分析
        if len(all_sxx) > 1:
            cv_sxx = np.std(all_sxx) / abs(np.mean(all_sxx)) if abs(np.mean(all_sxx)) > 1e-10 else 1.0
            max_error_sxx = max(errors_sxx)
            
            print(f"\n统计分析:")
            print(f"  σxx变异系数: {cv_sxx:.4f}")
            print(f"  最大σxx误差: {max_error_sxx:.1f}%")
            print(f"  平均|σyy|: {np.mean([abs(s) for s in all_syy]):.0f} Pa")
            print(f"  平均|τxy|: {np.mean([abs(s) for s in all_sxy]):.0f} Pa")
            
            # 判定标准：变异系数<5%，误差<10%
            if cv_sxx < 0.05 and max_error_sxx < 10:
                print("  ✅ 常应变分片试验通过")
            else:
                print("  ❌ 常应变分片试验失败")
                print("    可能原因:")
                if cv_sxx >= 0.05:
                    print("    - 单元间应力不一致（形函数或刚度矩阵问题）")
                if max_error_sxx >= 10:
                    print("    - 应力值偏差过大（材料矩阵或应变计算问题）")
        
        # 调试信息分析
        if 'b_matrices' in debug:
            print(f"\nB矩阵调试信息:")
            for i, b_matrix in enumerate(debug['b_matrices'][:2]):
                print(f"  单元{i+1} B矩阵:")
                print(b_matrix.strip())
    else:
        print("❌ 无应力数据")
    
    # 纯剪切试验分析
    print("\n纯剪切分片试验结果:")
    print("="*50)
    
    disp2, stress2, debug2 = parse_stap_debug_output('../data/results_t3_patch_pure_shear_standard.out')
    
    if stress2:
        print("实际应力结果:")
        normal_stresses = []
        shear_stresses = []
        
        for elem, s in stress2.items():
            sxx, syy, sxy = s['sxx'], s['syy'], s['sxy']
            normal_stresses.extend([abs(sxx), abs(syy)])
            shear_stresses.append(abs(sxy))
            
            print(f"  单元 {elem}: σxx={sxx:.0f} Pa, σyy={syy:.0f} Pa, τxy={sxy:.0f} Pa")
        
        if normal_stresses and shear_stresses:
            max_normal = max(normal_stresses)
            mean_shear = np.mean(shear_stresses)
            
            print(f"\n统计分析:")
            print(f"  最大正应力: {max_normal:.0f} Pa")
            print(f"  平均剪切应力: {mean_shear:.0f} Pa")
            
            if mean_shear > 100:  # 避免除零
                ratio = max_normal / mean_shear
                print(f"  正应力/剪切应力比值: {ratio:.3f}")
                
                if ratio < 0.1:
                    print("  ✅ 纯剪切分片试验通过")
                else:
                    print("  ❌ 纯剪切分片试验失败：正应力过大")
            else:
                print("  ❌ 剪切应力过小或为零")
    else:
        print("❌ 无应力数据")

if __name__ == "__main__":
    comprehensive_patch_test_analysis()
    print("\n分析完成!")
    print("="*60)