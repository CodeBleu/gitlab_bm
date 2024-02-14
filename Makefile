VERSION := $(shell poetry run glbm --version | cut -d ":" -f2 | tr -d " ")

.PHONY: build
build: ## make build # Build Python package
	@poetry build

.PHONY: test
test: ## make test# Run Pytests for glbm
	@poetry run pytest tests/ ${args}

.PHONY: pre-release
pre-release: ## make pre-release  Increment 'x' ( 0.0.0-dev.x )
	@poetry version prerelease
	@./generate_version.py
	git add src/gitlab_bm/app_info.py
	git add pyproject.toml
	git status

.PHONY: update-patch
update-patch: ## make update-patch # Increment 'x' ( 0.0.x )
	@poetry version patch
	@./generate_version.py
	git add src/gitlab_bm/app_info.py
	git add pyproject.toml
	git status

.PHONY: update-minor
update-minor: ## make update-minor # Increment 'x' ( 0.x.0 )
	@poetry version minor
	@./generate_version.py
	git add src/gitlab_bm/app_info.py
	git add pyproject.toml
	git status

.PHONY: update-major
update-major: ## make update-major # Increment 'x' ( x.0.0 )
	@poetry version major
	@./generate_version.py
	git add src/gitlab_bm/app_info.py
	git add pyproject.toml
	git status

.PHONY: update
update: ## make update # Update package dependencies
	@poetry update

.PHONY: get-version
get-version: ## make get-version # Get current app version
	@poetry run glbm --version

.PHONY: publish-testpypi
publish-testpypi:## make publish-testpypi # Publish package to Test PyPi
	@ poetry build
	@ poetry publish -r testpypi
	@ git tag -a "v$(VERSION)" -m "Dev Release $(VERSION)"

.PHONY: publish
publish:## make publish # Publish package
	@poetry build
	@poetry publish
	@git push origin
	@git tag -a "v$(VERSION)" -m "Release version $(VERSION)"
	@git push origin "v$(VERSION)"

ifeq ($(MAKECMDGOALS),)
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
endif
