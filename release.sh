git checkout main
git pull
current_version=$(git describe --tags --abbrev=0)
echo "Current version: $current_version"

# Accept version bump type from user
echo "Enter version bump type (major, minor, patch):"
read bump_type

# Bump version
bumpversion --current-version $current_version $bump_type setup.py

# Get new version
new_version=$(git describe --tags --abbrev=0)
echo "New version: $new_version"

# Commit and push
git push --tags $new_version
git push origin main

# Build and upload to PyPI
python setup.py sdist bdist_wheel
twine upload dist/*
