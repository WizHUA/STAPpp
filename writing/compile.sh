#!/bin/bash
# filepath: /home/wiz/WorkSpace/STAPpp/writing/compile.sh

echo "清理编译文件..."
rm -f *.aux *.toc *.out *.log *.fdb_latexmk *.fls *.pdf *.synctex.gz

echo "第一次编译..."
xelatex main.tex

echo "第二次编译..."
xelatex main.tex

echo "第三次编译..."
xelatex main.tex

echo "编译完成！"
ls -la main.pdf