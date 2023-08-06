# sweet-pipes

## Install

```bash
pip install "sweet-pipes @ git+ssh://git@github.com/fkodom/sweet-pipes.git"

# Install all dev dependencies (tests etc.)
pip install "sweet-pipes[all] @ git+ssh://git@github.com/fkodom/sweet-pipes.git"

# Setup pre-commit hooks
pre-commit install
```


## Test

Tests run automatically through GitHub Actions.
* Fast tests run on each push.
* Slow tests (decorated with `@pytest.mark.slow`) run on each PR.


## Release

[Optional] Requires either PyPI or Docker GHA workflows to be enabled.

Just tag a new release in this repo, and GHA will automatically publish Python wheels and/or Docker images.
