# ASM - Utility to manage secrets in Aws Secrets Manager

This is a simple utility to manage secrets in AWS Secrets Manager. This script helps you group secrets by service and environment. It will create a secret in the format of` /<environment>/<service>/<secret>`. It makes management of secrets easier and more organized.


## Installation

```bash
pip install secrets-manager-aws
```

## Usage

```bash
asm --help
```

### To create a secret for a service

```
 asm -e <environment> -s <service>
 ```

This command will open all the secrets for the service and environment in the VIM
editor. You can then edit the secrets and save the file. This will update the secrets in the Secrets Manager automatically.








