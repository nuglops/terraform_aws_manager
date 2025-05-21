#!/usr/bin/env python3
"""
Terraform AWS Manager
Automates Terraform workflow (init, plan, apply, destroy) across AWS workspaces.
Author: Jeff Silver
License: MIT
"""
import os
import subprocess
import argparse
import yaml
import sys

DEFAULT_TF_DIR = "./terraform"
DEFAULT_AWS_PROFILE = "default"

def run_command(cmd, env=None):
    print(f"🔧 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    if result.returncode != 0:
        print(f"❌ Error:\n{result.stderr}")
        sys.exit(result.returncode)
    print(result.stdout)
    return result.stdout

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def terraform_workflow(action, tf_dir, workspace=None, aws_profile=DEFAULT_AWS_PROFILE, auto_approve=False):
    env = os.environ.copy()
    env["AWS_PROFILE"] = aws_profile
    os.chdir(tf_dir)
    run_command(["terraform", "init"], env)
    if workspace:
        run_command(["terraform", "workspace", "select", workspace], env)
    if action == "plan":
        run_command(["terraform", "plan"], env)
    elif action == "apply":
        cmd = ["terraform", "apply"]
        if auto_approve:
            cmd.append("-auto-approve")
        run_command(cmd, env)
    elif action == "destroy":
        cmd = ["terraform", "destroy"]
        if auto_approve:
            cmd.append("-auto-approve")
        run_command(cmd, env)
    else:
        print("Unsupported action:", action)

def main():
    parser = argparse.ArgumentParser(description="Manage Terraform AWS workflows via Python.")
    parser.add_argument("action", choices=["plan", "apply", "destroy"], help="Terraform action to perform.")
    parser.add_argument("--dir", default=DEFAULT_TF_DIR, help="Terraform config directory.")
    parser.add_argument("--workspace", help="Terraform workspace to use.")
    parser.add_argument("--profile", default=DEFAULT_AWS_PROFILE, help="AWS CLI profile.")
    parser.add_argument("--auto-approve", action="store_true", help="Skip interactive approval.")
    parser.add_argument("--config", help="YAML config file to automate multiple runs.")
    args = parser.parse_args()
    if args.config:
        config = load_config(args.config)
        for env_name, settings in config.items():
            print(f"\n🌍 Executing for environment: {env_name}")
            terraform_workflow(
                action=args.action,
                tf_dir=settings.get("dir", args.dir),
                workspace=settings.get("workspace"),
                aws_profile=settings.get("profile", args.profile),
                auto_approve=args.auto_approve
            )
    else:
        terraform_workflow(
            action=args.action,
            tf_dir=args.dir,
            workspace=args.workspace,
            aws_profile=args.profile,
            auto_approve=args.auto_approve
        )

if __name__ == "__main__":
    main()
