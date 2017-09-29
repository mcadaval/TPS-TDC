#!/bin/bash
#rm informe.pdf
mkdir output ; pdflatex -output-directory=output main.tex # 1> /dev/null
ln -s output/main.pdf ./informe.pdf
xdg-open informe.pdf &