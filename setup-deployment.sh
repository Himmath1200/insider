#!/bin/bash
# Setup script for deployment preparation
# Usage: bash setup-deployment.sh

echo "=================================================="
echo "Insider Threat Detection - Deployment Setup"
echo "=================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env with your configuration:"
    echo "   - Generate a strong SECRET_KEY"
    echo "   - Update ALLOWED_ORIGINS with your domain"
else
    echo "✓ .env file already exists"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p dist
mkdir -p instance
mkdir -p logs
echo "✓ Directories created"

# Copy static files to dist (for Netlify)
echo ""
echo "Preparing frontend for Netlify..."
mkdir -p dist
cp -r templates/* dist/ 2>/dev/null || true
cp -r static/* dist/ 2>/dev/null || true
echo "✓ Frontend files prepared"

echo ""
echo "=================================================="
echo "✓ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Initialize Git: git init && git add . && git commit -m 'Initial commit'"
echo "3. Push to GitHub"
echo "4. Deploy backend to Railway"
echo "5. Deploy frontend to Netlify"
echo ""
echo "For detailed instructions, see DEPLOYMENT.md"
echo ""
