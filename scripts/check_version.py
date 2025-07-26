#!/usr/bin/env python3
"""
Check for new version of awscli-local on PyPI and compare with current PKGBUILD version.
Sets GitHub Actions outputs for use in subsequent steps.
"""

import requests
import re
import os
import sys

def get_current_version():
    """Extract current version from PKGBUILD."""
    try:
        with open('PKGBUILD', 'r') as f:
            pkgbuild_content = f.read()
        
        current_version_match = re.search(r'pkgver=(.+)', pkgbuild_content)
        if not current_version_match:
            print("ERROR: Could not find current version in PKGBUILD")
            return None
            
        return current_version_match.group(1)
    except FileNotFoundError:
        print("ERROR: PKGBUILD file not found")
        return None

def get_latest_version():
    """Get latest version from PyPI."""
    try:
        response = requests.get('https://pypi.org/pypi/awscli-local/json')
        response.raise_for_status()
        return response.json()['info']['version']
    except requests.RequestException as e:
        print(f"ERROR: Failed to fetch version from PyPI: {e}")
        return None

def set_github_output(key, value):
    """Set GitHub Actions output."""
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"{key}={value}\n")
    print(f"Output: {key}={value}")

def main():
    current_version = get_current_version()
    if not current_version:
        sys.exit(1)
        
    latest_version = get_latest_version()
    if not latest_version:
        sys.exit(1)
    
    print(f"Current version: {current_version}")
    print(f"Latest version: {latest_version}")
    
    needs_update = current_version != latest_version
    print(f"Needs update: {needs_update}")
    
    # Set GitHub Actions outputs
    set_github_output("current_version", current_version)
    set_github_output("latest_version", latest_version)
    set_github_output("needs_update", "true" if needs_update else "false")
    
    if needs_update:
        print(f"✓ Update available: {current_version} → {latest_version}")
    else:
        print("✓ Already up to date")

if __name__ == "__main__":
    main()
