# AWS Secrets Manager Utility

[![PyPI version](https://badge.fury.io/py/secrets-manager-aws.svg)](https://badge.fury.io/py/secrets-manager-aws)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/secrets-manager-aws.svg)](https://pypi.org/project/secrets-manager-aws)

A streamlined utility for managing secrets in a Simpler way on AWS Secrets Manager with hierarchical organization without opening multiple aws management console tabs. This tool simplifies secret management by grouping them based on service and environment, creating a clear and maintainable structure.

## ✨ Features

- 🔐 Hierarchical secret organization (`/<environment>/<service>/<secret>`)
- 🌐 Environment-based segregation
- 📝 Interactive secret editing using familiar VIM interface
- 🏗️ Service-based grouping for better organization

## 📋 Prerequisites

- Python 3.9 or higher
- AWS credentials configured (`~/.aws/credentials` or environment variables)
- AWS IAM permissions for Secrets Manager operations

## 🚀 Installation

### Option 1: Using pip (Recommended)
```bash
pip install secrets-manager-aws
```

### Option 2: Using poetry
```bash
poetry add secrets-manager-aws
```

## 🎯 Usage

The utility provides a simple and intuitive command-line interface for managing your AWS Secrets.

### Command Line Options

```bash
asm --help                          # Show help and available commands
asm -e ENV -s SERVICE              # Create/edit/view secrets for a service in an environment

```

### Examples

1. **Creating / Managing  Secrets**
   ```bash
   # Create secrets for authentication service in production
   asm -e production -s auth-service

   # Create secrets for payment service credentials in development
   asm -e development -s payment-service
   ```



## 🌉 Roadmap

- [ ] Implement support for aws parameter store integration
- [ ] Add support for search and filtering secrets
- [ ] Add support for cross-env secret copying
- [ ] Add Github Actions for CI/CD
-  More to follow...

## 🤝 Feature Requests

If you have a feature request, please open an issue to discuss it. We welcome all ideas and contributions!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


### Contributing Guidelines

1. Fork the repository and create your branch from `master`
2. Write clear commit messages
3. Update documentation as needed
4. Add tests for new features
5. Make sure all tests pass
6. Submit a pull request


## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links & Resources

- [PyPI Package](https://pypi.org/project/secrets-manager-aws)
- [Issue Tracker](https://github.com/ARKKYN/aws-secrets-manager/issues)
- [Documentation](https://github.com/ARKKYN/aws-secrets-manager/wiki)
- [Change Log](CHANGELOG.md)

## 🙋‍♂️ Support & Community

- [Open an issue](https://github.com/ARKKYN/aws-secrets-manager/issues/new) for bug reports and feature requests
- [Discussions](https://github.com/ARKKYN/aws-secrets-manager/discussions) for questions and community support
- [Security Policy](SECURITY.md) for reporting security vulnerabilities








