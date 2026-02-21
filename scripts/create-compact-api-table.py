#!/usr/bin/env python3
"""
Create Compact API Endpoints Table
Parse API-ENDPOINTS-FULL.md and create condensed table format
"""

import re
from collections import defaultdict

def parse_full_api_doc(file_path):
    """Parse the full API documentation"""

    with open(file_path, 'r') as f:
        content = f.read()

    # Split by service sections
    sections = re.split(r'\n## ([^\n]+) \((\d+) endpoints\)', content)

    endpoints = []
    current_service = "Unknown"

    # Parse each endpoint
    endpoint_pattern = r'### ([🔵🟢🟡🟠🔴⚪]) `(\w+) ([^`]+)`\n\n\*\*Summary\*\*: ([^\n]+)'

    for match in re.finditer(endpoint_pattern, content):
        emoji, method, path, summary = match.groups()

        # Get service from context (look backwards)
        pos = match.start()
        service_match = re.search(r'\n## ([^\n]+) \(\d+ endpoints\)', content[:pos])
        if service_match:
            current_service = service_match.group(1)

        endpoints.append({
            'service': current_service,
            'method': method,
            'path': path,
            'summary': summary.strip(),
            'emoji': emoji
        })

    return endpoints

def group_by_service(endpoints):
    """Group endpoints by service"""
    grouped = defaultdict(list)
    for ep in endpoints:
        grouped[ep['service']].append(ep)
    return dict(grouped)

def create_compact_table(endpoints_by_service, output_file):
    """Create compact markdown table"""

    with open(output_file, 'w') as f:
        f.write("# API Endpoints - Compact Table\n\n")
        f.write("**Total Endpoints**: {}\n".format(sum(len(eps) for eps in endpoints_by_service.values())))
        f.write("**Format**: Compact table for quick reference\n\n")
        f.write("---\n\n")

        # Table of contents
        f.write("## 📋 Quick Index\n\n")
        for service in sorted(endpoints_by_service.keys()):
            count = len(endpoints_by_service[service])
            anchor = service.lower().replace(' ', '-').replace('/', '-')
            f.write(f"- [{service}](#{anchor}) ({count})\n")
        f.write("\n---\n\n")

        # Compact tables by service
        for service in sorted(endpoints_by_service.keys()):
            endpoints = endpoints_by_service[service]
            f.write(f"## {service}\n\n")

            # Table header
            f.write("| Method | Endpoint | Summary |\n")
            f.write("|--------|----------|----------|\n")

            # Sort by path
            for ep in sorted(endpoints, key=lambda x: (x['path'], x['method'])):
                method_emoji = ep['emoji']
                summary_short = ep['summary'][:80] + "..." if len(ep['summary']) > 80 else ep['summary']
                f.write(f"| {method_emoji} {ep['method']} | `{ep['path']}` | {summary_short} |\n")

            f.write("\n")

def create_ultra_compact(endpoints_by_service, output_file):
    """Create ultra-compact list format"""

    with open(output_file, 'w') as f:
        f.write("# API Endpoints - Ultra Compact\n\n")
        f.write("**Format**: One-line per endpoint\n\n")

        all_endpoints = []
        for service, eps in endpoints_by_service.items():
            all_endpoints.extend(eps)

        # Group by method
        by_method = defaultdict(list)
        for ep in all_endpoints:
            by_method[ep['method']].append(ep)

        for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            if method in by_method:
                f.write(f"\n## {method} ({len(by_method[method])})\n\n")
                f.write("```\n")
                for ep in sorted(by_method[method], key=lambda x: x['path']):
                    f.write(f"{ep['method']:<6} {ep['path']}\n")
                f.write("```\n")

if __name__ == '__main__':
    input_file = 'docs/backend/API-ENDPOINTS-FULL.md'

    print("📊 Parsing full API documentation...")
    endpoints = parse_full_api_doc(input_file)
    print(f"✅ Found {len(endpoints)} endpoints")

    print("📦 Grouping by service...")
    endpoints_by_service = group_by_service(endpoints)
    print(f"✅ Grouped into {len(endpoints_by_service)} services")

    # Create compact table
    output_compact = 'docs/backend/API-ENDPOINTS-COMPACT.md'
    print(f"\n📝 Creating compact table: {output_compact}")
    create_compact_table(endpoints_by_service, output_compact)

    # Create ultra-compact
    output_ultra = 'docs/backend/API-ENDPOINTS-ULTRA-COMPACT.md'
    print(f"📝 Creating ultra-compact list: {output_ultra}")
    create_ultra_compact(endpoints_by_service, output_ultra)

    print("\n✅ Compact documentation created!")
    print(f"\nFiles:")
    print(f"  - {output_compact} (table format)")
    print(f"  - {output_ultra} (one-line format)")
