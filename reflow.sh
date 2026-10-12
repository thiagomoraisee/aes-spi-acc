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
   "docs/spec"             # Functional specification
   "docs/architecture"     # Microarchitecture and power supply architecture
   "docs/reports"          # Follow-up weekly reports
   "rtl/src"               # RTL source codes
   "rtl/tb"                # Testbenches
   "model"                 # Imported behavioral models (memory, PLL, etc)
   "formal"                # Formality scripts and reports
   "synth"                 # SDC, scripts and synthesis repots
   "power"                 # UPF files and reports
   "scripts"               # Automatio flow scripts
   "workspace"             # Work directory
)

echo "============================"
echo "  Reference Flow Generator  "
echo "------==== [v0.1] ====------"
echo ""

# Test if you're in a git repository
if git rev-parse --is-inside-work-tree &>/dev/null; then
   ROOT_DIR=$(git rev-parse --show-toplevel)
   echo "[INFO] Root directory: $ROOT_DIR"
else
   ROOT_DIR=$PWD
   echo "[WARN] You are not in a git repository." 
   echo "Directories will be created in current directory ($PWD)."
   read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
fi

# Test the ROOT_DIR variable is valid
if [ -z "$ROOT_DIR" ]; then
    echo "[ERROR] ROOT_DIR is empty. Aborting execution." >&2
    exit 1
fi

NAME_DIR=$(basename $ROOT_DIR)

miss_dirs=0

for dir in "${DIRS[@]}"; do
   target_dir="$ROOT_DIR/$dir"
   if [ ! -d "$target_dir" ]; then
      mkdir -p "$target_dir"
      echo " Created directory: $NAME_DIR/$dir"
      ((miss_dirs++))
   fi
done

echo "[INFO] Created $miss_dirs directories"
echo "[INFO] Directory structure generation complete!"
echo "Please move this script to $NAME_DIR/scripts/"
tree $ROOT_DIR
