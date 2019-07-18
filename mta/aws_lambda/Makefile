default: build_env

image:
	docker build -t lambda-packager .

build_env: image
	docker run --rm -v $(shell pwd)/build:/build -t lambda-packager /build/package.sh


shell: image
	docker run --rm -v $(shell pwd)/build:/build -it lambda-packager /bin/bash
