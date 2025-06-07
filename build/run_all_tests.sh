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
