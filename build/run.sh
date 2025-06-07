#!/bin/bash
echo "=========================================="
echo "T3三角形单元验证测试套件"
echo "=========================================="

cd ~/WorkSpace/STAPpp/build

# 测试案例列表
tests=(
    "t3_patch_constant_strain.dat"
    "t3_patch_pure_shear.dat"
    "t3_cantilever_coarse.dat"
    "t3_cantilever_medium.dat"
    "t3_cantilever_fine.dat"
    "t3_cook_membrane.dat"
    "t3_square_plate.dat"
)

# 运行所有测试
for test in "${tests[@]}"; do
    echo "------------------------------------------"
    echo "运行测试: $test"
    echo "------------------------------------------"
    
    if [ -f "../data/$test" ]; then
        ./stap++ "../data/$test" > "../data/results_${test%.dat}.out"
        
        if [ $? -eq 0 ]; then
            echo "✅ $test 测试成功"
        else
            echo "❌ $test 测试失败"
        fi
    else
        echo "⚠️  文件 $test 不存在"
    fi
    echo ""
done

echo "=========================================="
echo "所有测试完成！"
echo "=========================================="