# ====================================================================================== #
# SOFTEX @ CIEXPERT 2026 (UFCG/CEEI)                                          2026.10.09 #
# -------------------------------------------------------------------------------------- #
# Script     : Makefile                                                                  #
# Author     : Thiago M. de Oliveira <thiago.oliveira@embedded.ufcg.edu.br>              #
# Description: Main automation for project execution. Designed to  be run from workspace #
# ====================================================================================== #
.PHONY: lint compile run waves clean clean_sim

BLOCKNAME = accumulator

VLOGAN_FLAGS = -full64 \
			   	-sverilog \
			   	-kdb \
			   	+lint=all

VCS_FLAGS = -full64 \
				-timescale=1ns/1ps \
				-debug_access+all \
				-kdb

# Check and create reference flow:
flow:
	bash ../scripts/reflow.sh

# Check syntax:
lint:
	vlogan $(VLOGAN_FLAGS) \
			 ../rtl/pkg/*.sv \
			 ../rtl/src/*.sv \
			 ../rtl/tb/*.sv \

# RTL Compile:
compile: lint
	vcs $(VCS_FLAGS) -top $(BLOCKNAME)_tb

# RTL Simulation:
run: compile
	./simv

# Open waveform
waves:
	verdi -ssf waves.fsdb &

# simulation cleanup
clean_sim:
	rm -rf csrc simv* work.lib++ *.daidir novas* AN.DB ucli.key verdi* DVEfiles .vlogan* *.fsdb *.log

clean: clean_sim
