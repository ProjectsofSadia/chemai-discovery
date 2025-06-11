# ChemAI Discovery - Advanced Makefile
# Simplify development and deployment

.PHONY: help install install-full setup run test clean docker deploy

help:
	@echo "🧬 ChemAI Discovery - Advanced Drug Discovery Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install basic requirements"
	@echo "  install-full - Install all requirements including optional"
	@echo "  setup        - Complete project setup"
	@echo "  run          - Run the platform"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean up generated files"
	@echo "  docker       - Build and run Docker container"
	@echo "  deploy       - Deploy to production"

install:
	@echo "📦 Installing basic requirements..."
	pip install -r requirements.txt
	@echo "✅ Basic installation complete!"

install-full:
	@echo "📦 Installing full requirements..."
	pip install -r requirements.txt
	# Optional: Uncomment to install RDKit
	# pip install rdkit-pypi
	@echo "✅ Full installation complete!"

setup: install-full
	@echo "🏗️ Setting up ChemAI Discovery..."
	mkdir -p logs data/molecules models/pretrained
	@echo "✅ Setup complete!"

run:
	@echo "🚀 Starting ChemAI Discovery Platform..."
	python src/main.py

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf logs/*.log
	@echo "✅ Cleanup complete!"

docker:
	@echo "🐳 Building and running Docker container..."
	docker-compose -f deployment/docker/docker-compose.yml up --build

deploy:
	@echo "🚀 Deploying to production..."
	@echo "Please configure your deployment target first!"

dev:
	@echo "🔧 Starting development server..."
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

format:
	@echo "🎨 Formatting code..."
	black src/ tests/
	@echo "✅ Code formatted!"

lint:
	@echo "🔍 Linting code..."
	flake8 src/ tests/
	mypy src/
	@echo "✅ Linting complete!"

benchmark:
	@echo "⚡ Running performance benchmarks..."
	python scripts/benchmark.py
	@echo "✅ Benchmarks complete!"

demo:
	@echo "🎬 Running demo..."
	python scripts/demo.py
	@echo "✅ Demo complete!"
