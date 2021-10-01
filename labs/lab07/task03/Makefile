.PHONY: build
build:
	docker build --tag devnet:latest -f Dockerfile .

.PHONY: run
run:
	docker run --add-host csr1kv1:10.254.0.1 --add-host csr1kv2:10.254.0.2 --add-host csr1kv3:10.254.0.3 -v ${PWD}:/devnet  -it devnet:latest /bin/bash

.PHONY: clean
clean:
	docker rmi devnet:latest --force

