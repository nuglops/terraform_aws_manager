# Terraform AWS Manager 🛠️

A Python utility to automate Terraform workflows in AWS. Supports multiple environments via workspaces and AWS CLI profiles.

## Features

- Run `init`, `plan`, `apply`, and `destroy` with CLI or config file
- Workspace-aware
- AWS profile support
- CI/CD-ready structure
- YAML config for multiple environment automation

## Usage

```bash
python main.py plan --dir ./prod --workspace production --profile prod-profile
python main.py apply --config config.yaml --auto-approve
```

## YAML Config Example

```yaml
staging:
  dir: ./terraform/staging
  workspace: staging
  profile: staging-profile

production:
  dir: ./terraform/prod
  workspace: production
  profile: prod-profile
```

## Requirements

- Terraform (v1.0+)
- Python 3.7+
- AWS CLI (configured)

```bash
pip install -r requirements.txt
```

## License

MIT
