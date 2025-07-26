#!/usr/bin/env python3
"""
Update PKGBUILD with new version, source URL, and SHA256 checksum.
Downloads and verifies the package from PyPI.
"""

import requests
import re
import hashlib
import sys
import argparse

def get_package_info(version):
    """Get package information from PyPI."""
    try:
        response = requests.get(f'https://pypi.org/pypi/awscli-local/{version}/json')
        response.raise_for_status()
        
        # Find the source tarball
        files = response.json()['urls']
        source_file = None
        for file_info in files:
            if file_info['packagetype'] == 'sdist':
                source_file = file_info
                break
        
        if not source_file:
            print("ERROR: No source distribution found on PyPI")
            return None
            
        return {
            'url': source_file['url'],
            'sha256': source_file['digests']['sha256']
        }
    except requests.RequestException as e:
        print(f"ERROR: Failed to get package info from PyPI: {e}")
        return None

def verify_checksum(url, expected_sha256):
    """Download package and verify its checksum."""
    print("Downloading package to verify checksum...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        calculated_sha256 = hashlib.sha256(response.content).hexdigest()
        
        if expected_sha256 != calculated_sha256:
            print(f"ERROR: Checksum mismatch!")
            print(f"PyPI reports: {expected_sha256}")
            print(f"Calculated:   {calculated_sha256}")
            return False
        else:
            print("✓ Checksum verification passed")
            return True
            
    except requests.RequestException as e:
        print(f"ERROR: Failed to download package for verification: {e}")
        return False

def update_pkgbuild(version, package_info):
    """Update PKGBUILD with new version and package information."""
    try:
        with open('PKGBUILD', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("ERROR: PKGBUILD file not found")
        return False
    
    # Update version
    content = re.sub(r'pkgver=.+', f'pkgver={version}', content)
    
    # Reset pkgrel to 1 for new version
    content = re.sub(r'pkgrel=.+', 'pkgrel=1', content)
    
    # Update source URL - handle the PyPI URL pattern
    download_url = package_info['url']
    if 'source=(' in content:
        # Extract just the filename part after packages/ for the URL
        url_suffix = download_url.split('packages/')[-1]
        content = re.sub(
            r'(source=\([^)]*https://files\.pythonhosted\.org/packages/)[^")]+([^)]*\))',
            lambda m: m.group(1) + url_suffix + m.group(2),
            content
        )
    
    # Update sha256sum
    sha256_hash = package_info['sha256']
    if "sha256sums=('SKIP')" in content:
        content = re.sub(r"sha256sums=\('SKIP'\)", f"sha256sums=('{sha256_hash}')", content)
    elif 'sha256sums=(' in content:
        # Replace existing checksum
        content = re.sub(
            r"sha256sums=\('[^']*'\)",
            f"sha256sums=('{sha256_hash}')",
            content
        )
    else:
        # Add sha256sums if it doesn't exist
        source_line = re.search(r'source=\([^)]+\)', content)
        if source_line:
            insert_pos = source_line.end()
            content = (content[:insert_pos] + 
                      f"\nsha256sums=('{sha256_hash}')" + 
                      content[insert_pos:])
    
    # Write updated PKGBUILD
    try:
        with open('PKGBUILD', 'w') as f:
            f.write(content)
        print("✓ PKGBUILD updated successfully")
        return True
    except IOError as e:
        print(f"ERROR: Failed to write PKGBUILD: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Update PKGBUILD with new version from PyPI')
    parser.add_argument('version', help='New version to update to')
    parser.add_argument('--verify', action='store_true', 
                       help='Download and verify package checksum (default: True)', default=True)
    parser.add_argument('--no-verify', dest='verify', action='store_false',
                       help='Skip checksum verification')
    
    args = parser.parse_args()
    
    print(f"Updating PKGBUILD to version {args.version}")
    
    # Get package information from PyPI
    package_info = get_package_info(args.version)
    if not package_info:
        sys.exit(1)
    
    print(f"Download URL: {package_info['url']}")
    print(f"SHA256: {package_info['sha256']}")
    
    # Verify checksum if requested
    if args.verify:
        if not verify_checksum(package_info['url'], package_info['sha256']):
            sys.exit(1)
    
    # Update PKGBUILD
    if not update_pkgbuild(args.version, package_info):
        sys.exit(1)
    
    print(f"✓ Successfully updated to version {args.version}")

if __name__ == "__main__":
    main()
