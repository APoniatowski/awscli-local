#!/usr/bin/env python3
"""
Generate .SRCINFO file from PKGBUILD.
This is a simplified version that handles the basic PKGBUILD format.
"""

import re
import sys

def parse_pkgbuild():
    """Parse PKGBUILD and extract key information."""
    try:
        with open('PKGBUILD', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("ERROR: PKGBUILD file not found")
        return None
    
    def extract_field(pattern, required=True):
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        elif required:
            print(f"ERROR: Could not find required field: {pattern}")
            return None
        return ""
    
    def extract_array(pattern):
        match = re.search(pattern, content)
        if match:
            array_content = match.group(1)
            # Parse array elements - handle both 'quoted' and unquoted items
            items = []
            for item in re.findall(r"'([^']+)'|\"([^\"]+)\"|([^\s'\"]+)", array_content):
                # item is a tuple, get the non-empty group
                value = next(filter(None, item), None)
                if value:
                    items.append(value)
            return items
        return []
    
    # Extract basic fields
    pkgname = extract_field(r'pkgname=([^\s]+)')
    pkgver = extract_field(r'pkgver=([^\s]+)')
    pkgrel = extract_field(r'pkgrel=([^\s]+)')
    pkgdesc = extract_field(r'pkgdesc="([^"]+)"')
    url = extract_field(r'url="([^"]+)"')
    
    if not all([pkgname, pkgver, pkgrel, pkgdesc, url]):
        return None
    
    # Extract arrays
    arch = extract_array(r"arch=\(([^)]+)\)")
    license_arr = extract_array(r"license=\(([^)]+)\)")
    depends = extract_array(r"depends=\(([^)]+)\)")
    makedepends = extract_array(r"makedepends=\(([^)]+)\)")
    
    # Set defaults
    if not arch:
        arch = ['any']
    if not license_arr:
        license_arr = ['unknown']
    
    return {
        'pkgname': pkgname,
        'pkgver': pkgver,
        'pkgrel': pkgrel,
        'pkgdesc': pkgdesc,
        'url': url,
        'arch': arch,
        'license': license_arr,
        'depends': depends,
        'makedepends': makedepends
    }

def generate_srcinfo(pkg_info):
    """Generate .SRCINFO content from parsed PKGBUILD info."""
    lines = []
    
    # pkgbase section
    lines.append(f"pkgbase = {pkg_info['pkgname']}")
    lines.append(f"\tpkgdesc = {pkg_info['pkgdesc']}")
    lines.append(f"\tpkgver = {pkg_info['pkgver']}")
    lines.append(f"\tpkgrel = {pkg_info['pkgrel']}")
    lines.append(f"\turl = {pkg_info['url']}")
    
    # Add arrays
    for arch in pkg_info['arch']:
        lines.append(f"\tarch = {arch}")
    
    for license_item in pkg_info['license']:
        lines.append(f"\tlicense = {license_item}")
    
    for dep in pkg_info['depends']:
        lines.append(f"\tdepends = {dep}")
    
    for makedep in pkg_info['makedepends']:
        lines.append(f"\tmakedepends = {makedep}")
    
    # pkgname section
    lines.append("")
    lines.append(f"pkgname = {pkg_info['pkgname']}")
    
    return '\n'.join(lines) + '\n'

def main():
    print("Generating .SRCINFO from PKGBUILD...")
    
    # Parse PKGBUILD
    pkg_info = parse_pkgbuild()
    if not pkg_info:
        sys.exit(1)
    
    # Generate .SRCINFO content
    srcinfo_content = generate_srcinfo(pkg_info)
    
    # Write .SRCINFO file
    try:
        with open('.SRCINFO', 'w') as f:
            f.write(srcinfo_content)
        print("✓ .SRCINFO generated successfully")
    except IOError as e:
        print(f"ERROR: Failed to write .SRCINFO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
