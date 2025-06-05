### 清华大学有限元法基础大作业实验过程整理  
#### 一、大作业基本信息  
- **作业名称**：有限元法基础大作业  
- **提交时间**：2025年6月8日前  
- **参与形式**：个人独立完成或4-5人组队（二选一）  
- **成绩占比**：20%  

#### 二、大作业内容及任务要求  
##### （一）编程训练：扩展STAPpp程序功能  
1. **核心任务**  
   - 个人需新增1个单元类型，团队成员每人至少新增1个单元，团队可组合使用所有单元（总成绩加0-5分）  
   - 求解包含梁单元{insert\_element\_0\_}、板单元、六面体实体单元的综合考题，并用ABAQUS验证结果  
   - 自愿参加程序功{insert\_element\_1\_}能、求解规模、精度与效率竞赛（加0-5分）  
   - 后处理：用Te{insert\_element\_2\_}cPlot/ParaView绘制变形图或应力云图  
2. **技术要求** {insert\_element\_3\_} 
   - 所有单元需完成收敛性分析、分片试验及验证算例  
   - 从GitHub{insert\_element\_4\_}仓库（xzhang66/STAP90或xzhang66/STAPpp）fork代码并进行版本控制  
3. **报告内容** {insert\_element\_5\_} 
   - 单元基本原理、编程思路、输入数据格式说明  
   - 收敛率分析、分{insert\_element\_6\_}片试验及验证算例结果  

##### （二）问题{insert\_element\_7\_}求解：自选实际问题分析  
1. **任务要求**  
   - 自选工程问题，使用ABAQUS或其他软件建模分析  
   - 可进行改进/优{insert\_element\_8\_}化设计（加0-5分）  
2. **报告规范** {insert\_element\_9\_} 
   - 符合GB 3102.11-1993标准：变量/函数用斜体，矢量用斜黑体，已知函数/常数用正体  

#### 三、成果提交{insert\_element\_10\_}规范  
1. **文件结构**  
   - 源程序、工程文件、算例文件（每个算例单独建文件夹）🔶1-35🔶  
   - 输{insert\_element\_11\_}入/输出数据{insert\_element\_12\_}文件  
   - STAPxx程{insert\_element\_13\_}序研发报告（需包含以下内容）：  
     - 引言（功能说明）、算法说明、实现方案、使用方法  
     - 程序验证：{insert\_element\_14\_}各单元分片试验、收敛率分析（需解析解或人工解）🔶1-45🔶  
     - 团队需说明{insert\_element\_15\_}任务分工与合作情况  
     - 结论及参考{insert\_element\_16\_}文献引用  

2. **版本控制与提{insert\_element\_17\_}交**  
   - **Git目录结构**：src/（源代码）、make/、data/、doc/、others/（其他文件移至此）  
   - **GitHu{insert\_element\_18\_}b工作流**：  
     1. 基于master分支创建描述性分支  
     2. 提交更改{insert\_element\_19\_}（规范commit信息）  
     3. 发起Pu{insert\_element\_20\_}ll Request讨论并根据反馈修改  
     4. 合并至m{insert\_element\_21\_}aster分支并部署（master始终可部署）  
   - **提交方式*{insert\_element\_22\_}*：网络学堂提交报告，并附上GitHub仓库链接  

#### 四、参考资料{insert\_element\_23\_}与工具  
1. **后处理工具**  
   - TecPlot：参考《计算动力学（第2版）》附录B及tecplot_example示例  
   - ParaVie{insert\_element\_24\_}w：参考《计算动力学（第2版）》附录C及Example.zip（含vtk/vtu格式）  
2. **版本控制** {insert\_element\_25\_} 
   - GitHub Flow指南：https://guides.github.com/introduction/flow/   
   - 《Git版本控{insert\_element\_26\_}制基础教程》（倪锐晨整理）  
3. **其他资源** {insert\_element\_27\_} 
   - QUADS.for程序、RCM半带宽优化算法  
   - 桥梁结构背景知{insert\_element\_28\_}识（竞赛参考）  