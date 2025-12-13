# Publishing LLM Safety Guard to PyPI

This guide walks you through publishing the `llm-safety-guard` package to PyPI.

## Prerequisites

1. **Create PyPI Account**
   - Go to https://pypi.org/account/register/
   - Verify your email
   - Enable 2FA (recommended)

2. **Create Test PyPI Account** (for testing)
   - Go to https://test.pypi.org/account/register/

3. **Install Publishing Tools**
   ```powershell
   pip install --upgrade build twine
   ```

## Step 1: Prepare Your Package

1. **Update Version Number** (in `setup.py` and `pyproject.toml`)
   ```python
   version='0.1.0'  # Change this for new releases
   ```

2. **Update Author Email** (in `setup.py` and `pyproject.toml`)
   ```python
   author_email='your.email@example.com'  # Replace with your email
   ```

3. **Update README.md**
   - Ensure all examples work
   - Add shields/badges
   - Include installation instructions

## Step 2: Build the Package

```powershell
# Clean previous builds
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build the package
python -m build
```

This creates:
- `dist/llm_safety_guard-0.1.0.tar.gz` (source distribution)
- `dist/llm_safety_guard-0.1.0-py3-none-any.whl` (wheel distribution)

## Step 3: Test on Test PyPI (Recommended)

1. **Upload to Test PyPI**
   ```powershell
   python -m twine upload --repository testpypi dist/*
   ```

2. **Enter Credentials**
   - Username: `__token__`
   - Password: Your Test PyPI API token (get from https://test.pypi.org/manage/account/#api-tokens)

3. **Test Installation**
   ```powershell
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ llm-safety-guard
   ```

4. **Verify Installation**
   ```python
   python -c "from llm_safety_guard import Guards; print('Success!')"
   ```

## Step 4: Publish to PyPI

1. **Upload to PyPI**
   ```powershell
   python -m twine upload dist/*
   ```

2. **Enter Credentials**
   - Username: `__token__`
   - Password: Your PyPI API token (get from https://pypi.org/manage/account/#api-tokens)

3. **Verify on PyPI**
   - Visit: https://pypi.org/project/llm-safety-guard/

## Step 5: Test Installation from PyPI

```powershell
# Create fresh environment
python -m venv test_env
.\test_env\Scripts\Activate.ps1

# Install from PyPI
pip install llm-safety-guard

# Test import
python -c "from llm_safety_guard import Guards; print('Package works!')"
```

## Using API Tokens (Recommended)

Instead of using username/password, use API tokens:

1. **Create PyPI API Token**
   - Go to https://pypi.org/manage/account/#api-tokens
   - Click "Add API token"
   - Name: "llm-safety-guard-upload"
   - Scope: "Entire account" or specific project

2. **Create .pypirc File** (in your home directory)
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YourActualTokenHere

   [testpypi]
   username = __token__
   password = pypi-YourTestTokenHere
   ```

3. **Upload with Token**
   ```powershell
   python -m twine upload dist/*
   ```

## Versioning Best Practices

Follow Semantic Versioning (SemVer):
- **0.1.0** - Initial release
- **0.1.1** - Bug fixes
- **0.2.0** - New features (backward compatible)
- **1.0.0** - Stable release
- **2.0.0** - Breaking changes

Update version in both:
- `setup.py`
- `pyproject.toml`

## Publishing Checklist

- [ ] Update version number
- [ ] Update CHANGELOG.md (if you have one)
- [ ] Update README.md with latest examples
- [ ] Update author email
- [ ] Clean build artifacts
- [ ] Build package (`python -m build`)
- [ ] Test on Test PyPI
- [ ] Verify test installation works
- [ ] Upload to PyPI
- [ ] Verify PyPI page looks correct
- [ ] Test installation from PyPI
- [ ] Create GitHub release/tag
- [ ] Update documentation

## Troubleshooting

### Error: "File already exists"
- The version already exists on PyPI
- Update version number in `setup.py` and `pyproject.toml`
- Rebuild: `python -m build`

### Error: "Invalid distribution"
- Check MANIFEST.in includes all necessary files
- Ensure `__init__.py` exists in all package directories
- Verify package structure with: `python setup.py check`

### Error: "Module not found" after install
- Check package structure in `setup.py`
- Ensure all packages listed in `packages=find_packages()`
- Add `__init__.py` to module directories

## Quick Reference Commands

```powershell
# Clean and rebuild
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
python -m build

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Check package
python -m twine check dist/*

# Test installation locally
pip install -e .
```

## After Publishing

1. **Announce**
   - Tweet about it
   - Post on Reddit (r/Python, r/MachineLearning)
   - LinkedIn post
   - Dev.to article

2. **Add Badges to README**
   ```markdown
   [![PyPI version](https://badge.fury.io/py/llm-safety-guard.svg)](https://badge.fury.io/py/llm-safety-guard)
   [![Downloads](https://pepy.tech/badge/llm-safety-guard)](https://pepy.tech/project/llm-safety-guard)
   ```

3. **Monitor**
   - Watch GitHub issues
   - Check PyPI download stats
   - Monitor for bug reports

## Support

For issues with publishing:
- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/
