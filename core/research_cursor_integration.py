#!/usr/bin/env python3
"""
Adam Clay - IDE Integration Research
Badanie możliwości wykorzystania połączenia IDE z LLM

Ten skrypt bada czy można wykorzystać istniejące połączenie IDE
do komunikacji z LLM, zamiast używać własnego klucza API.
"""

import os
import json
import subprocess
import socket
import psutil
import time
from pathlib import Path
from typing import List, Dict, Optional, Any

print("🔬 Adam Clay - IDE Integration Research")
print("=" * 50)

def check_ide_processes() -> List[Dict[str, Any]]:
    """Sprawdź procesy związane z IDE"""
    print("\n🔍 Sprawdzanie procesów IDE...")
    
    ide_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name'].lower()
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()
            
            if 'ide' in name or 'ide' in cmdline:
                ide_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': proc.info['cmdline']
                })
                print(f"  ✅ Znaleziono: {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if not ide_processes:
        print("  ❌ Nie znaleziono aktywnych procesów IDE")
    
    return ide_processes

def check_ide_network_connections() -> List[Dict[str, Any]]:
    """Sprawdź połączenia sieciowe IDE"""
    print("\n🌐 Sprawdzanie połączeń sieciowych IDE...")
    
    connections = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            if 'ide' in name:
                try:
                    for conn in proc.connections() or []:
                        if conn.status == 'ESTABLISHED':
                            connections.append({
                                'pid': proc.info['pid'],
                                'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                                'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                                'status': conn.status
                            })
                            print(f"  🔗 {proc.info['name']}: {conn.laddr.ip}:{conn.laddr.port} → {conn.raddr.ip if conn.raddr else 'None'}:{conn.raddr.port if conn.raddr else 'N/A'}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if not connections:
        print("  ❌ Nie znaleziono aktywnych połączeń IDE")
    
    return connections

def check_ide_config_files() -> Dict[str, Any]:
    """Sprawdź pliki konfiguracyjne IDE"""
    print("\n📁 Sprawdzanie plików konfiguracyjnych IDE...")
    
    config_paths = [
        Path.home() / ".ide",
        Path.home() / ".config" / "ide",
        Path.home() / ".ide-tutor",
        Path.home() / "Library" / "Application Support" / "IDE",  # macOS
        Path.home() / "AppData" / "Roaming" / "IDE",  # Windows
    ]
    
    found_configs = {}
    
    for config_path in config_paths:
        if config_path.exists():
            print(f"  ✅ Znaleziono: {config_path}")
            found_configs[str(config_path)] = {
                'exists': True,
                'files': []
            }
            
            # Lista plików konfiguracyjnych
            try:
                for file_path in config_path.rglob("*"):
                    if file_path.is_file() and file_path.suffix in ['.json', '.yaml', '.yml', '.config', '.txt']:
                        relative_path = file_path.relative_to(config_path)
                        found_configs[str(config_path)]['files'].append(str(relative_path))
                        print(f"    📄 {relative_path}")
            except PermissionError:
                print(f"    ⚠️  Brak uprawnień do odczytu {config_path}")
        else:
            print(f"  ❌ Nie znaleziono: {config_path}")
    
    return found_configs

def scan_local_ports() -> List[int]:
    """Sprawdź lokalne porty, które mogą być używane przez IDE"""
    print("\n🔌 Skanowanie lokalnych portów...")
    
    common_ports = [3000, 3001, 8000, 8001, 8080, 8081, 9000, 9001, 5000, 5001]
    open_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            open_ports.append(port)
            print(f"  ✅ Port {port} jest otwarty")
    
    if not open_ports:
        print("  ❌ Nie znaleziono otwartych portów ze standardowej listy")
    
    return open_ports

def check_vscode_extensions() -> List[Dict[str, Any]]:
    """Sprawdź rozszerzenia VS Code/IDE"""
    print("\n🧩 Sprawdzanie rozszerzeń VS Code/IDE...")
    
    extension_paths = [
        Path.home() / ".vscode" / "extensions",
        Path.home() / ".ide" / "extensions",
        Path.home() / ".config" / "ide" / "extensions",
    ]
    
    extensions = []
    
    for ext_path in extension_paths:
        if ext_path.exists():
            print(f"  📂 Sprawdzanie: {ext_path}")
            try:
                for ext_dir in ext_path.iterdir():
                    if ext_dir.is_dir():
                        package_json = ext_dir / "package.json"
                        if package_json.exists():
                            try:
                                with open(package_json, 'r') as f:
                                    data = json.load(f)
                                    if 'llm-provider' in data.get('name', '').lower() or 'llm' in data.get('name', '').lower():
                                        extensions.append({
                                            'name': data.get('name'),
                                            'version': data.get('version'),
                                            'path': str(ext_dir)
                                        })
                                        print(f"    🤖 {data.get('name')} v{data.get('version')}")
                            except (json.JSONDecodeError, KeyError):
                                continue
            except PermissionError:
                print(f"    ⚠️  Brak uprawnień do odczytu {ext_path}")
    
    if not extensions:
        print("  ❌ Nie znaleziono rozszerzeń związanych z LLM/LLM provider")
    
    return extensions

def test_potential_endpoints() -> Dict[str, Any]:
    """Testuj potencjalne endpointy API"""
    print("\n🎯 Testowanie potencjalnych endpointów API...")
    
    endpoints = [
        "http://localhost:3000/api/chat",
        "http://localhost:8000/api/llm",
        "http://127.0.0.1:5000/llm-provider",
        "http://localhost:9000/api/ai",
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            import requests
            response = requests.get(endpoint, timeout=2)
            results[endpoint] = {
                'accessible': True,
                'status_code': response.status_code,
                'headers': dict(response.headers)
            }
            print(f"  ✅ {endpoint} → {response.status_code}")
        except requests.exceptions.RequestException:
            results[endpoint] = {'accessible': False}
            print(f"  ❌ {endpoint} → niedostępny")
        except ImportError:
            print("  ⚠️  Brak modułu requests - pomijam testy HTTP")
            break
    
    return results

def analyze_ide_executable() -> Dict[str, Any]:
    """Analizuj plik wykonywalny IDE"""
    print("\n🔍 Analiza pliku wykonywalnego IDE...")
    
    ide_paths = [
        "/Applications/IDE.app/Contents/MacOS/IDE",  # macOS
        "/usr/bin/ide",  # Linux
        Path.home() / "Applications" / "IDE.app" / "Contents" / "MacOS" / "IDE",
    ]
    
    ide_info = {}
    
    for ide_path in ide_paths:
        if Path(ide_path).exists():
            print(f"  ✅ Znaleziono IDE: {ide_path}")
            ide_info['path'] = str(ide_path)
            
            # Sprawdź wersję
            try:
                result = subprocess.run([str(ide_path), '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    ide_info['version'] = result.stdout.strip()
                    print(f"    📋 Wersja: {ide_info['version']}")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print("    ⚠️  Nie udało się sprawdzić wersji")
            
            break
    else:
        print("  ❌ Nie znaleziono pliku wykonywalnego IDE")
    
    return ide_info

def generate_research_report(data: Dict[str, Any]) -> str:
    """Generuj raport z badań"""
    report = """
# 🔬 Adam Clay - Raport Badań Integracji z IDE

## 📊 Podsumowanie wyników

"""
    
    if data.get('ide_processes'):
        report += "✅ **IDE jest aktywny** - znaleziono działające procesy\n"
    else:
        report += "❌ **IDE nie jest aktywny** - brak procesów\n"
    
    if data.get('network_connections'):
        report += "✅ **IDE ma aktywne połączenia sieciowe**\n"
    else:
        report += "❌ **Brak aktywnych połączeń sieciowych**\n"
    
    if data.get('config_files'):
        report += "✅ **Znaleziono pliki konfiguracyjne IDE**\n"
    else:
        report += "❌ **Brak plików konfiguracyjnych**\n"
    
    report += f"""
## 🚀 Rekomendacje dla Adam Clay

### Opcja 1: Oficjalny klucz LLM provider (ZALECANE)
- Szybkie uruchomienie: 5 minut
- Pełna kontrola nad requestami  
- Przewidywalne koszty (~$3-30/miesiąc)

### Opcja 2: Badanie integracji z IDE (EKSPERYMENTALNE)
"""
    
    if data.get('ide_processes'):
        report += "- ✅ IDE jest dostępny do dalszych badań\n"
        report += "- 🔬 Możliwe kierunki: proxy server, API discovery\n"
    else:
        report += "- ❌ IDE nie jest aktywny - brak możliwości integracji\n"
    
    report += """
### 💡 Następne kroki
1. **Szybki start**: `export LLM_PROVIDER_API_KEY="klucz"` + `make consciousness`
2. **Dalsze badania**: Kontynuować analizę IDE API (jeśli dostępny)
3. **Hybrydowe podejście**: Oficjalny API + eksperymentalna integracja z IDE

---
*Raport wygenerowany przez Adam Clay Research Assistant*
"""
    
    return report

def main():
    """Główna funkcja badawcza"""
    
    print("Rozpoczynam badanie możliwości integracji Adam Clay z IDE...\n")
    
    research_data = {}
    
    # Zbierz dane
    research_data['ide_processes'] = check_ide_processes()
    research_data['network_connections'] = check_ide_network_connections()
    research_data['config_files'] = check_ide_config_files()
    research_data['local_ports'] = scan_local_ports()
    research_data['vscode_extensions'] = check_vscode_extensions()
    research_data['api_endpoints'] = test_potential_endpoints()
    research_data['ide_executable'] = analyze_ide_executable()
    
    # Generuj raport
    report = generate_research_report(research_data)
    
    # Zapisz wyniki
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = f"ide_research_report_{timestamp}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Raport zapisany: {output_file}")
    print("\n" + "=" * 50)
    print("🎯 WNIOSKI:")
    
    if research_data['ide_processes']:
        print("✅ IDE jest aktywny - możliwa dalsza integracja!")
        print("💡 Zalecam: rozpocznij od oficjalnego API, potem eksperymentuj z IDE")
    else:
        print("⚠️  IDE nie jest aktywny - użyj oficjalnego klucza API")
    
    print("\n🚀 Aby uruchomić Adam Clay z oficjalnym API:")
    print("1. Zdobądź klucz: https://console.llm-provider.com/")
    print("2. export LLM_PROVIDER_API_KEY='your-key'")
    print("3. make consciousness")
    
    return research_data

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Badanie przerwane przez użytkownika")
    except Exception as e:
        print(f"\n❌ Błąd podczas badania: {e}")
        import traceback
        traceback.print_exc() 