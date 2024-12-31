CONDA_DEFAULT_ENV=fluxon-env

# Helper function for printing a status message
print_status() {
    echo -e "${YELLOW}[STATUS]${NC} $1"
}

# Print a header
echo -e "${GREEN}=================================="
echo -e "Running Fluxon Release"
echo -e "==================================${NC}"

# Check for conda environment
if ! command -v conda &> /dev/null; then
    echo -e "${RED}[ERROR] Conda not found! Please install Anaconda or Miniconda.${NC}"
    exit 1
else 
    print_status "Conda is installed"
    print_status "Activating Conda environment: $CONDA_DEFAULT_ENV"
    source activate $CONDA_DEFAULT_ENV
fi

# Check if an environment is activated
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo -e "${RED}[ERROR] No Conda environment is active! Activate an environment and try again.${NC}"
    exit 1
else
    print_status "Using Conda environment: $CONDA_DEFAULT_ENV"
fi


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
git push origin --tags $new_version
git push origin main

# Create release
gh release create $new_version --target main --title $new_version --notes "Release $new_version"

# Build and upload to PyPI
python setup.py sdist bdist_wheel
twine upload dist/*
