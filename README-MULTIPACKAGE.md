# Multi-Package Project Support

This project now supports multiple package managers and CLI tools, enabling development across different language ecosystems.

## Supported Package Managers

### Node.js (npm)
- **Package Manager**: npm
- **Configuration**: `package.json`
- **Installation**: `npm install`
- **Start**: `npm start`

### Python (pip/uv)
- **Package Manager**: pip (uv compatible)
- **Configuration**: `pyproject.toml`
- **Installation**: `pip install -e .` or `uv pip install -e .`
- **CLI Command**: `npm run python-cli`

### PHP (Composer)
- **Package Manager**: Composer
- **Configuration**: `composer.json`
- **Installation**: `composer install`
- **CLI Command**: `npm run php-cli`

### Ruby (RubyGems/Bundler)
- **Package Manager**: Bundler
- **Configuration**: `Gemfile`
- **Installation**: `bundle install`
- **CLI Command**: `npm run ruby-cli`

### pnpm (Monorepo Support)
- **Package Manager**: pnpm
- **Configuration**: `pnpm-workspace.yaml`
- **Installation**: `pnpm install`
- **Commands**: `npm run pnpm-install`, `npm run pnpm-start`

## CLI Tools

All CLI tools are accessible via npm scripts:

```bash
# Python CLI
npm run python-cli

# PHP CLI
npm run php-cli

# Ruby CLI
npm run ruby-cli

# pnpm commands
npm run pnpm-install
npm run pnpm-start
```

## Project Structure

```
.
├── cli/
│   ├── python/
│   │   └── main.py
│   ├── php/
│   │   └── main.php
│   └── ruby/
│       └── main.rb
├── package.json
├── composer.json
├── Gemfile
├── pyproject.toml
├── pnpm-workspace.yaml
└── multi-package-project/
    ├── package.json
    ├── composer.json
    ├── Gemfile
    ├── pyproject.toml
    └── src/
        └── main.py
```

## Getting Started

1. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -e .
   ```

3. **Install PHP dependencies**:
   ```bash
   composer install
   ```

4. **Install Ruby dependencies**:
   ```bash
   bundle install
   ```

5. **Run CLI tools**:
   ```bash
   npm run python-cli
   npm run php-cli
   npm run ruby-cli
   ```

## Development

This project demonstrates a unified approach to managing multiple language ecosystems within a single repository. Each language has its own CLI entry point and package configuration, allowing developers to work seamlessly across different technology stacks.