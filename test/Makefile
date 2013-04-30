TESTS = enum ns inheritance arg_test template_type_param enum_query 

test: $(TESTS)
	@for i in $^; \
            do (make -C $$i test); \
        done
clean: $(TESTS)
	@for i in $^; \
            do (make -C $$i clean); \
        done
