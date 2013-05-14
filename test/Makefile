TESTS = enum ns inheritance arg_test template_type_param db_update enum_query inheritance_query type_info

test: $(TESTS)
	@for i in $^; \
            do (echo $$i; make -C $$i test); \
        done
clean: $(TESTS)
	@for i in $^; \
            do (echo $$i; make -C $$i clean); \
        done
