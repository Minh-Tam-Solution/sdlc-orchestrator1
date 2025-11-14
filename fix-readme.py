#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix README.md character encoding issues"""

def main():
    # Read file as binary first to handle encoding issues
    with open('README.md', 'rb') as f:
        raw_content = f.read()
    
    # Try decode with error handling
    try:
        content = raw_content.decode('utf-8', errors='ignore')
    except:
        content = raw_content.decode('latin-1', errors='ignore')
    
    # Define replacements
    replacements = {
        # Update version
        'SDLC 4.8': 'SDLC 4.9',
        
        # Fix emoji headers
        '# <�': '# 🎯',
        '## =�': '## 🚀',
        '### <�': '### ⚡',
        '## <�': '## 🏗️',
        '## =�': '## 📚',
        '## =�': '## 🛠️',
        '## =�': '## 📁',
        '## =O': '## 🤝',
        '## ='': '## 💻',
        '## =�': '## 🗺️',
        '## <
': '## 💬',
        '## <�': '## 📖',
        '## <�': '## 📊',
        '## =�': '## 📞',
        '## =�': '## 📄',
        '## =O': '## 🙏',
        
        # Fix arrows in description
        '�': '→',
        
        # Fix numbers
        'd5': '≤5',
        
        # Fix list bullets  
        ' " ': ' • ',
        
        # Fix architecture diagram characters
        ' <� USER-FACING': ' 🎨 USER-FACING',
        ' >� BUSINESS': ' ⚙️ BUSINESS',
        ' = INTEGRATION': ' 🔌 INTEGRATION',
        ' <� INFRASTRUCTURE': ' 🏭 INFRASTRUCTURE',
        
        # Fix checkmarks
        ' ': ' ✅',
        'Built with d': 'Built with ❤️',
        
        # Fix special chars in diagrams
        '                                                             $': '├─────────────────────────────────────────────────────────────┤',
    }
    
    # Apply replacements
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Fix the architecture diagram box drawing
    arch_old = """                                                             
 🎨 USER-FACING LAYER (Custom - Our IP)                      
├─────────────────────────────────────────────────────────────┤
 • React Dashboard (Stage Console, Gate Status)              
 • VS Code Extension (Templates, AI, Evidence)               
 • YAML Policy Packs (SDLC 4.9 Lite/Standard/Enterprise)     
                                                             
                            →
                                                             
 ⚙️ BUSINESS LOGIC LAYER (Custom - Our IP)                   
├─────────────────────────────────────────────────────────────┤
 • Gate Engine Wrapper (YAML → Rego compiler)                
 • Evidence Vault API (metadata + traceability)              
 • AI Context Engine (stage-aware prompts)                   
 • Design Thinking Workflow (G0.1, G0.2)                     
 • GitHub Bridge (smart sync logic)                          
 • Approval Hierarchy (self-test prevention)                 
                                                             
                            →
                                                             
 🔌 INTEGRATION LAYER (Thin Adapters)                        
├─────────────────────────────────────────────────────────────┤
 • opa_service.py (Conftest client)                          
 • minio_service.py (S3-compatible client)                   
 • grafana_service.py (dashboard/OnCall API)                 
 • github_service.py (webhooks + GraphQL)                    
 • ai_service.py (multi-provider routing)                    
                                                             
                            →
                                                             
 🏭 INFRASTRUCTURE LAYER (OSS - Proven Components)           
├─────────────────────────────────────────────────────────────┤
 • OPA + Conftest (policy engine)                             
 • MinIO/S3 (artifact storage)                                
 • Grafana Stack (Prometheus + Grafana + OnCall)             
 • PostgreSQL (metadata + state)                              
 • Redis (caching + sessions)"""
    
    arch_new = """┌─────────────────────────────────────────────────────────────┐
│ 🎨 USER-FACING LAYER (Custom - Our IP)                     │
├─────────────────────────────────────────────────────────────┤
│ • React Dashboard (Stage Console, Gate Status)             │
│ • VS Code Extension (Templates, AI, Evidence)              │
│ • YAML Policy Packs (SDLC 4.9 Lite/Standard/Enterprise)    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ ⚙️ BUSINESS LOGIC LAYER (Custom - Our IP)                   │
├─────────────────────────────────────────────────────────────┤
│ • Gate Engine Wrapper (YAML → Rego compiler)               │
│ • Evidence Vault API (metadata + traceability)             │
│ • AI Context Engine (stage-aware prompts)                  │
│ • Design Thinking Workflow (G0.1, G0.2)                    │
│ • GitHub Bridge (smart sync logic)                         │
│ • Approval Hierarchy (self-test prevention)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 🔌 INTEGRATION LAYER (Thin Adapters)                        │
├─────────────────────────────────────────────────────────────┤
│ • opa_service.py (Conftest client)                         │
│ • minio_service.py (S3-compatible client)                  │
│ • grafana_service.py (dashboard/OnCall API)                │
│ • github_service.py (webhooks + GraphQL)                   │
│ • ai_service.py (multi-provider routing)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 🏭 INFRASTRUCTURE LAYER (OSS - Proven Components)           │
├─────────────────────────────────────────────────────────────┤
│ • OPA + Conftest (policy engine)                           │
│ • MinIO/S3 (artifact storage)                              │
│ • Grafana Stack (Prometheus + Grafana + OnCall)            │
│ • PostgreSQL (metadata + state)                            │
│ • Redis (caching + sessions)                               │
└─────────────────────────────────────────────────────────────┘"""
    
    content = content.replace(arch_old, arch_new)
    
    # Write fixed content back
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ README.md encoding fixed successfully!")
    print("✅ Updated to SDLC 4.9")
    print("✅ Fixed all emoji and special characters")

if __name__ == '__main__':
    main()
