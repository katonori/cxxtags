check:
ifeq (${LLVM_HOME},)
	@echo "ERROR: set LLVM_HOME"
	@exit 1
endif
