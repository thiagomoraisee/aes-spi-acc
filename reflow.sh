#!/bin/bash
# ====================================================================================== #
# SOFTEX @ CIEXPERT 2026 (UFCG/CEEI)                                          2026.10.09 # 
# -------------------------------------------------------------------------------------- #
# Script     : reflow.sh                                                                 #
# Author     : Thiago M. de Oliveira <thiago.oliveira@embedded.ufcg.edu.br>              #
# Description: Reference flow generator/verifier. Creates initial directory structure    #
#              and check project deliverables.                                           #
# ====================================================================================== #

DIRS=(
   "docs/spec"
   "docs/architecture"
   "docs/reports"
   "rtl/src"
   "rtl/tb"
   "model"
   "formal"
   "synth"
   "power"
   "scripts"
   "workspace"
)

echo "============================"
echo "  Reference Flow Generator  "
echo "------==== [v0.1] ====------"

miss_dirs=0

for dir in "${DIRS[@]}"; do
   if [ ! -d "$dir" ]; then
      mkdir -p "$dir"
      echo " Created dir: $dir"
      ((miss_dirs++))
   fi
done

echo "[INFO] Created $miss_dirs directories"
echo "[INFO] Directory structure generation complete!"
tree
