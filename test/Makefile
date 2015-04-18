#TESTS = enum ns inheritance arg_test template_type_param db_update enum_query inheritance_query type_info rebuild
TESTS = keyword_with_space enum ns inheritance rebuild cxxtags_run_proj/dir_hir macro

test: $(TESTS)
	rm -f log
	@for i in $^; \
            do ((echo $$i; make -C $$i test) 2>&1 | tee -a log); \
        done
	test 0 -eq `grep -i ERROR log | wc -l`
clean: $(TESTS)
	@for i in $^; \
            do (echo $$i; make -C $$i clean); \
        done
