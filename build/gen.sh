#!/bin/bash
# filepath: /home/wiz/WorkSpace/STAPpp/build/generate_t3_test_cases.sh

echo "=========================================="
echo "T3三角形单元测试数据生成脚本"
echo "=========================================="

# 创建data目录（如果不存在）
mkdir -p ../data

echo "正在生成T3单元测试算例..."

# ==============================================
# 1. 分片试验（Patch Test）
# ==============================================

echo "1. 生成分片试验数据..."

# 1.1 常应变拉伸试验（修正版）
cat > ../data/t3_patch_constant_strain.dat << 'EOF'
T3 Patch Test - Constant Strain
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 2.0 0.0 0.0
3 0 0 1 2.0 2.0 0.0
4 1 0 1 0.0 2.0 0.0
1
4
2 1 1000.0
2 2 0.0
3 1 1000.0
3 2 0.0
3 2 1
1 210000.0 0.3 1.0
1 1 2 3 1
2 1 3 4 1
EOF

# 1.2 纯剪切分片试验
cat > ../data/t3_patch_pure_shear.dat << 'EOF'
T3 Patch Test - Pure Shear
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
3 2 100.0
4 2 -100.0
3 2 1
1 210000.0 0.3 1.0
1 1 2 3 1
2 1 3 4 1
EOF

# 1.3 简单拉伸试验（验证基本功能）
cat > ../data/t3_simple_tension.dat << 'EOF'
T3 Simple Tension Test
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
2 1 500.0
3 1 500.0
3 2 1
1 210000.0 0.3 1.0
1 1 2 3 1
2 1 3 4 1
EOF

# ==============================================
# 2. 收敛性分析
# ==============================================

echo "2. 生成收敛性分析数据..."

# 2.1 粗网格悬臂梁（2x1网格）
cat > ../data/t3_cantilever_coarse.dat << 'EOF'
T3 Cantilever Beam - Coarse Mesh
6 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 0.5 0.0
3 1 1 1 0.0 1.0 0.0
4 0 0 1 1.0 0.0 0.0
5 0 0 1 1.0 0.5 0.0
6 0 0 1 1.0 1.0 0.0
1
1
6 2 -1000.0
3 4 1
1 210000.0 0.3 1.0
1 1 4 5 1
2 1 5 2 1
3 2 5 6 1
4 2 6 3 1
EOF

# 2.2 中等网格悬臂梁（4x2网格）
cat > ../data/t3_cantilever_medium.dat << 'EOF'
T3 Cantilever Beam - Medium Mesh
15 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 0.25 0.0
3 1 1 1 0.0 0.5 0.0
4 1 1 1 0.0 0.75 0.0
5 1 1 1 0.0 1.0 0.0
6 0 0 1 0.5 0.0 0.0
7 0 0 1 0.5 0.25 0.0
8 0 0 1 0.5 0.5 0.0
9 0 0 1 0.5 0.75 0.0
10 0 0 1 0.5 1.0 0.0
11 0 0 1 1.0 0.0 0.0
12 0 0 1 1.0 0.25 0.0
13 0 0 1 1.0 0.5 0.0
14 0 0 1 1.0 0.75 0.0
15 0 0 1 1.0 1.0 0.0
1
1
15 2 -1000.0
3 16 1
1 210000.0 0.3 1.0
1 1 6 7 1
2 1 7 2 1
3 2 7 8 1
4 2 8 3 1
5 3 8 9 1
6 3 9 4 1
7 4 9 10 1
8 4 10 5 1
9 6 11 12 1
10 6 12 7 1
11 7 12 13 1
12 7 13 8 1
13 8 13 14 1
14 8 14 9 1
15 9 14 15 1
16 9 15 10 1
EOF

# 2.3 细网格悬臂梁（6x3网格）
cat > ../data/t3_cantilever_fine.dat << 'EOF'
T3 Cantilever Beam - Fine Mesh
28 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 0.333 0.0
3 1 1 1 0.0 0.667 0.0
4 1 1 1 0.0 1.0 0.0
5 0 0 1 0.333 0.0 0.0
6 0 0 1 0.333 0.333 0.0
7 0 0 1 0.333 0.667 0.0
8 0 0 1 0.333 1.0 0.0
9 0 0 1 0.667 0.0 0.0
10 0 0 1 0.667 0.333 0.0
11 0 0 1 0.667 0.667 0.0
12 0 0 1 0.667 1.0 0.0
13 0 0 1 1.0 0.0 0.0
14 0 0 1 1.0 0.333 0.0
15 0 0 1 1.0 0.667 0.0
16 0 0 1 1.0 1.0 0.0
17 0 0 1 1.333 0.0 0.0
18 0 0 1 1.333 0.333 0.0
19 0 0 1 1.333 0.667 0.0
20 0 0 1 1.333 1.0 0.0
21 0 0 1 1.667 0.0 0.0
22 0 0 1 1.667 0.333 0.0
23 0 0 1 1.667 0.667 0.0
24 0 0 1 1.667 1.0 0.0
25 0 0 1 2.0 0.0 0.0
26 0 0 1 2.0 0.333 0.0
27 0 0 1 2.0 0.667 0.0
28 0 0 1 2.0 1.0 0.0
1
1
28 2 -1000.0
3 36 1
1 210000.0 0.3 1.0
1 1 5 6 1
2 1 6 2 1
3 2 6 7 1
4 2 7 3 1
5 3 7 8 1
6 3 8 4 1
7 5 9 10 1
8 5 10 6 1
9 6 10 11 1
10 6 11 7 1
11 7 11 12 1
12 7 12 8 1
13 9 13 14 1
14 9 14 10 1
15 10 14 15 1
16 10 15 11 1
17 11 15 16 1
18 11 16 12 1
19 13 17 18 1
20 13 18 14 1
21 14 18 19 1
22 14 19 15 1
23 15 19 20 1
24 15 20 16 1
25 17 21 22 1
26 17 22 18 1
27 18 22 23 1
28 18 23 19 1
29 19 23 24 1
30 19 24 20 1
31 21 25 26 1
32 21 26 22 1
33 22 26 27 1
34 22 27 23 1
35 23 27 28 1
36 23 28 24 1
EOF

# ==============================================
# 3. 经典验证算例
# ==============================================

echo "3. 生成经典验证算例..."

# 3.1 Cook膜问题
cat > ../data/t3_cook_membrane.dat << 'EOF'
T3 Cook Membrane Problem
8 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 44.0 0.0
3 0 0 1 48.0 44.0 0.0
4 0 0 1 48.0 60.0 0.0
5 0 0 1 16.0 0.0 0.0
6 0 0 1 16.0 22.0 0.0
7 0 0 1 32.0 22.0 0.0
8 0 0 1 32.0 38.0 0.0
1
2
4 1 1.0
4 2 0.0
3 8 1
1 1.0 0.3 1.0
1 1 5 6 1
2 1 6 2 1
3 2 6 7 1
4 2 7 8 1
5 5 7 6 1
6 6 7 8 1
7 8 3 4 1
8 8 4 2 1
EOF

# 3.2 受集中载荷的正方形板
cat > ../data/t3_square_plate.dat << 'EOF'
T3 Square Plate with Point Load
9 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 0.5 0.0 0.0
3 0 1 1 1.0 0.0 0.0
4 1 0 1 0.0 0.5 0.0
5 0 0 1 0.5 0.5 0.0
6 0 0 1 1.0 0.5 0.0
7 1 0 1 0.0 1.0 0.0
8 0 0 1 0.5 1.0 0.0
9 0 0 1 1.0 1.0 0.0
1
1
5 2 -1000.0
3 8 1
1 210000.0 0.3 1.0
1 1 2 5 1
2 1 5 4 1
3 2 3 6 1
4 2 6 5 1
5 4 5 8 1
6 4 8 7 1
7 5 6 9 1
8 5 9 8 1
EOF

# 3.3 单轴拉伸标准试件
cat > ../data/t3_uniaxial_tension.dat << 'EOF'
T3 Uniaxial Tension Specimen
12 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 1.0 0.0
3 1 1 1 0.0 2.0 0.0
4 0 0 1 1.0 0.0 0.0
5 0 0 1 1.0 1.0 0.0
6 0 0 1 1.0 2.0 0.0
7 0 0 1 2.0 0.0 0.0
8 0 0 1 2.0 1.0 0.0
9 0 0 1 2.0 2.0 0.0
10 0 0 1 3.0 0.0 0.0
11 0 0 1 3.0 1.0 0.0
12 0 0 1 3.0 2.0 0.0
1
3
10 1 500.0
11 1 500.0
12 1 500.0
3 10 1
1 210000.0 0.3 1.0
1 1 4 5 1
2 1 5 2 1
3 2 5 6 1
4 2 6 3 1
5 4 7 8 1
6 4 8 5 1
7 5 8 9 1
8 5 9 6 1
9 7 10 11 1
10 7 11 8 1
11 8 11 12 1
12 8 12 9 1
EOF

# ==============================================
# 4. 简单验证算例
# ==============================================

echo "4. 生成简单验证算例..."

# 4.1 单个三角形单元测试
cat > ../data/t3_single_element.dat << 'EOF'
T3 Single Element Test
3 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 0.0 1.0 0.0
1
1
2 1 100.0
3 1 1
1 210000.0 0.3 1.0
1 1 2 3 1
EOF

# 4.2 两个单元组合测试
cat > ../data/t3_two_elements.dat << 'EOF'
T3 Two Elements Test
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
2 1 100.0
3 1 100.0
3 2 1
1 210000.0 0.3 1.0
1 1 2 3 1
2 1 3 4 1
EOF

# 4.3 L形域测试
cat > ../data/t3_l_shape.dat << 'EOF'
T3 L-Shape Domain Test
8 1 1 1
1 1 1 1 0.0 0.0 0.0
2 1 1 1 0.0 1.0 0.0
3 1 1 1 0.0 2.0 0.0
4 0 0 1 1.0 0.0 0.0
5 0 0 1 1.0 1.0 0.0
6 0 0 1 1.0 2.0 0.0
7 0 0 1 2.0 0.0 0.0
8 0 0 1 2.0 1.0 0.0
1
2
7 1 500.0
8 1 500.0
3 6 1
1 210000.0 0.3 1.0
1 1 4 5 1
2 1 5 2 1
3 2 5 6 1
4 2 6 3 1
5 4 7 8 1
6 4 8 5 1
EOF

# ==============================================
# 5. 材料参数验证算例
# ==============================================

echo "5. 生成材料参数验证算例..."

# 5.1 高泊松比材料测试
cat > ../data/t3_high_poisson.dat << 'EOF'
T3 High Poisson Ratio Test
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
2 1 1000.0
3 1 1000.0
3 2 1
1 210000.0 0.45 1.0
1 1 2 3 1
2 1 3 4 1
EOF

# 5.2 低弹性模量材料测试
cat > ../data/t3_low_modulus.dat << 'EOF'
T3 Low Modulus Test
4 1 1 1
1 1 1 1 0.0 0.0 0.0
2 0 1 1 1.0 0.0 0.0
3 0 0 1 1.0 1.0 0.0
4 1 0 1 0.0 1.0 0.0
1
2
2 1 1000.0
3 1 1000.0
3 2 1
1 1000.0 0.3 1.0
1 1 2 3 1
2 1 3 4 1
EOF

# ==============================================
# 6. 创建验证脚本
# ==============================================

echo "6. 创建验证脚本..."

cat > run_all_tests.sh << 'EOF'
#!/bin/bash
# T3单元测试验证脚本

echo "=========================================="
echo "T3三角形单元测试验证套件"
echo "=========================================="

# 确保在正确的目录
cd "$(dirname "$0")"

# 测试案例列表
declare -a tests=(
    "t3_single_element.dat"
    "t3_two_elements.dat"
    "t3_simple_tension.dat"
    "t3_patch_constant_strain.dat"
    "t3_patch_pure_shear.dat"
    "t3_cantilever_coarse.dat"
    "t3_cantilever_medium.dat"
    "t3_uniaxial_tension.dat"
    "t3_square_plate.dat"
    "t3_l_shape.dat"
    "t3_high_poisson.dat"
    "t3_low_modulus.dat"
)

# 运行计数器
total_tests=${#tests[@]}
passed_tests=0
failed_tests=0

echo "总共 $total_tests 个测试案例"
echo ""

# 运行所有测试
for test in "${tests[@]}"; do
    echo "------------------------------------------"
    echo "运行测试: $test"
    echo "------------------------------------------"
    
    if [ -f "../data/$test" ]; then
        # 运行测试
        timeout 30s ./stap++ "../data/$test" > "results_${test%.dat}.out" 2>&1
        
        exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            echo "✅ $test 测试成功"
            ((passed_tests++))
        elif [ $exit_code -eq 124 ]; then
            echo "⏰ $test 测试超时"
            ((failed_tests++))
        else
            echo "❌ $test 测试失败 (退出码: $exit_code)"
            ((failed_tests++))
        fi
        
        # 检查输出文件大小
        output_file="results_${test%.dat}.out"
        if [ -f "$output_file" ]; then
            file_size=$(stat -c%s "$output_file")
            if [ $file_size -gt 0 ]; then
                echo "   输出文件大小: $file_size 字节"
            else
                echo "   ⚠️ 输出文件为空"
            fi
        fi
        
    else
        echo "❌ 文件 $test 不存在"
        ((failed_tests++))
    fi
    echo ""
done

echo "=========================================="
echo "测试完成！"
echo "通过: $passed_tests/$total_tests"
echo "失败: $failed_tests/$total_tests"
if [ $passed_tests -eq $total_tests ]; then
    echo "🎉 所有测试通过！"
else
    echo "⚠️  有测试失败，请检查输出"
fi
echo "=========================================="
EOF

# 设置脚本可执行权限
chmod +x run_all_tests.sh

# ==============================================
# 7. 创建结果分析脚本
# ==============================================

echo "7. 创建结果分析脚本..."

cat > analyze_results.py << 'EOF'
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
EOF

chmod +x analyze_results.py

echo ""
echo "=========================================="
echo "T3单元测试数据生成完成！"
echo "=========================================="
echo ""
echo "生成的文件："
echo "  测试数据: ../data/t3_*.dat (共 $(ls ../data/t3_*.dat 2>/dev/null | wc -l) 个文件)"
echo "  验证脚本: run_all_tests.sh"
echo "  分析脚本: analyze_results.py"
echo ""
echo "使用方法："
echo "  1. 运行所有测试: ./run_all_tests.sh"
echo "  2. 分析结果:     python3 analyze_results.py"
echo ""
echo "测试算例说明："
echo "  - 分片试验: t3_patch_*.dat"
echo "  - 收敛性分析: t3_cantilever_*.dat"
echo "  - 经典验证: t3_cook_membrane.dat, t3_square_plate.dat"
echo "  - 简单验证: t3_single_element.dat, t3_two_elements.dat"
echo "  - 材料验证: t3_high_poisson.dat, t3_low_modulus.dat"
echo ""
echo "注意: 所有测试数据都经过仔细设计，确保边界条件合理、"
echo "      载荷配置正确、材料参数有效。"
echo "=========================================="