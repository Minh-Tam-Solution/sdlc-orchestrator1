#!/usr/bin/env python3
"""
Parse OpenAPI Specification and Generate API Documentation
SDLC Orchestrator - Comprehensive Endpoint Report
"""

import json
import sys
from collections import defaultdict

def parse_openapi(spec_file):
    """Parse OpenAPI spec and extract endpoint details"""

    with open(spec_file) as f:
        spec = json.load(f)

    info = spec.get('info', {})
    paths = spec.get('paths', {})

    # Group endpoints by tag/service
    endpoints_by_tag = defaultdict(list)
    all_endpoints = []

    for path, methods in paths.items():
        for method, details in methods.items():
            if method.upper() not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']:
                continue

            endpoint = {
                'method': method.upper(),
                'path': path,
                'summary': details.get('summary', 'N/A'),
                'description': details.get('description', ''),
                'tags': details.get('tags', ['Uncategorized']),
                'operationId': details.get('operationId', 'N/A'),
                'parameters': [],
                'requestBody': None,
                'responses': {}
            }

            # Extract parameters
            if 'parameters' in details:
                for param in details['parameters']:
                    endpoint['parameters'].append({
                        'name': param.get('name'),
                        'in': param.get('in'),
                        'required': param.get('required', False),
                        'schema': param.get('schema', {}).get('type', 'string')
                    })

            # Extract request body
            if 'requestBody' in details:
                content = details['requestBody'].get('content', {})
                if 'application/json' in content:
                    schema = content['application/json'].get('schema', {})
                    endpoint['requestBody'] = {
                        'required': details['requestBody'].get('required', False),
                        'schema': schema.get('title', schema.get('type', 'object'))
                    }

            # Extract responses
            for status, response_details in details.get('responses', {}).items():
                content = response_details.get('content', {})
                if 'application/json' in content:
                    schema = content['application/json'].get('schema', {})
                    endpoint['responses'][status] = {
                        'description': response_details.get('description', ''),
                        'schema': schema.get('title', schema.get('type', 'object'))
                    }

            # Add to collections
            all_endpoints.append(endpoint)
            for tag in endpoint['tags']:
                endpoints_by_tag[tag].append(endpoint)

    return {
        'info': info,
        'total_endpoints': len(all_endpoints),
        'endpoints_by_tag': dict(endpoints_by_tag),
        'all_endpoints': all_endpoints
    }

def generate_markdown_report(data, output_file):
    """Generate comprehensive Markdown report"""

    with open(output_file, 'w') as f:
        # Header
        f.write(f"# API Endpoints Documentation - {data['info']['title']}\n\n")
        f.write(f"**Version**: {data['info']['version']}\n")
        f.write(f"**Total Endpoints**: {data['total_endpoints']}\n")
        f.write(f"**Generated**: Auto-generated from OpenAPI spec\n\n")
        f.write("---\n\n")

        # Table of Contents
        f.write("## 📋 Table of Contents\n\n")
        for i, tag in enumerate(sorted(data['endpoints_by_tag'].keys()), 1):
            count = len(data['endpoints_by_tag'][tag])
            f.write(f"{i}. [{tag}](#{tag.lower().replace(' ', '-')}) ({count} endpoints)\n")
        f.write("\n---\n\n")

        # Endpoints by tag
        for tag in sorted(data['endpoints_by_tag'].keys()):
            endpoints = data['endpoints_by_tag'][tag]
            f.write(f"## {tag} ({len(endpoints)} endpoints)\n\n")

            for endpoint in sorted(endpoints, key=lambda x: (x['path'], x['method'])):
                # Endpoint header
                method_badge = {
                    'GET': '🔵', 'POST': '🟢', 'PUT': '🟡',
                    'PATCH': '🟠', 'DELETE': '🔴'
                }.get(endpoint['method'], '⚪')

                f.write(f"### {method_badge} `{endpoint['method']} {endpoint['path']}`\n\n")

                # Summary
                if endpoint['summary'] != 'N/A':
                    f.write(f"**Summary**: {endpoint['summary']}\n\n")

                # Operation ID
                if endpoint['operationId'] != 'N/A':
                    f.write(f"**Operation ID**: `{endpoint['operationId']}`\n\n")

                # Parameters
                if endpoint['parameters']:
                    f.write("**Parameters**:\n\n")
                    f.write("| Name | In | Type | Required |\n")
                    f.write("|------|-------|------|----------|\n")
                    for param in endpoint['parameters']:
                        req = '✅' if param['required'] else '❌'
                        f.write(f"| `{param['name']}` | {param['in']} | {param['schema']} | {req} |\n")
                    f.write("\n")

                # Request Body
                if endpoint['requestBody']:
                    req = '✅' if endpoint['requestBody']['required'] else '❌'
                    f.write(f"**Request Body** (Required: {req}):\n")
                    f.write(f"- Schema: `{endpoint['requestBody']['schema']}`\n\n")

                # Responses
                if endpoint['responses']:
                    f.write("**Responses**:\n\n")
                    for status, response in sorted(endpoint['responses'].items()):
                        f.write(f"- **{status}**: {response['description']}\n")
                        f.write(f"  - Schema: `{response['schema']}`\n")
                    f.write("\n")

                f.write("---\n\n")

def generate_toon_summary(data, output_file):
    """Generate TOON format summary"""

    with open(output_file, 'w') as f:
        f.write("# API Endpoints Summary - TOON Format\n\n")
        f.write(f"**Total**: {data['total_endpoints']} endpoints\n")
        f.write(f"**Version**: {data['info']['version']}\n\n")

        # Count by method
        method_counts = defaultdict(int)
        for endpoint in data['all_endpoints']:
            method_counts[endpoint['method']] += 1

        f.write("## By Method\n\n")
        for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            if method in method_counts:
                f.write(f"- {method}: {method_counts[method]}\n")
        f.write("\n")

        # Count by tag
        f.write("## By Service/Tag\n\n")
        for tag in sorted(data['endpoints_by_tag'].keys()):
            count = len(data['endpoints_by_tag'][tag])
            f.write(f"- **{tag}**: {count} endpoints\n")
        f.write("\n")

        # Quick reference table
        f.write("## Quick Reference\n\n")
        f.write("| Method | Path | Summary |\n")
        f.write("|--------|------|----------|\n")

        # Show first 50 most important endpoints
        important = [e for e in data['all_endpoints']
                    if any(x in e['path'] for x in ['/auth/', '/gates/', '/evidence/', '/projects/'])]
        for endpoint in important[:50]:
            summary = endpoint['summary'][:60] if endpoint['summary'] != 'N/A' else ''
            f.write(f"| {endpoint['method']} | `{endpoint['path']}` | {summary} |\n")

if __name__ == '__main__':
    spec_file = '/tmp/openapi-spec.json'

    print("📊 Parsing OpenAPI specification...")
    data = parse_openapi(spec_file)

    print(f"✅ Found {data['total_endpoints']} endpoints")
    print(f"✅ Organized into {len(data['endpoints_by_tag'])} categories")

    # Generate full documentation
    output_md = 'docs/backend/API-ENDPOINTS-FULL.md'
    print(f"\n📝 Generating full documentation: {output_md}")
    generate_markdown_report(data, output_md)

    # Generate TOON summary
    output_toon = 'docs/backend/API-ENDPOINTS-TOON.md'
    print(f"📝 Generating TOON summary: {output_toon}")
    generate_toon_summary(data, output_toon)

    print("\n✅ Documentation generated successfully!")
    print(f"\nFiles created:")
    print(f"  - {output_md} (full details)")
    print(f"  - {output_toon} (TOON summary)")
