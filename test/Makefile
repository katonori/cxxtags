TESTS = enum ns inheritance arg_test template_type_param enum_query db_update inheritance_query

test: $(TESTS)
	@for i in $^; \
            do (echo $$i; make -C $$i test); \
        done
clean: $(TESTS)
	@for i in $^; \
            do (echo $$i; make -C $$i clean); \
        done
