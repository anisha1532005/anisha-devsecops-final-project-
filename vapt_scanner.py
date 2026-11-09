import os
import yaml

def run_vapt_scan():
    print("[*] Initializing VAPT Posture Scan (Simulating Nikto & Checkov checks)...")
    score = 100
    vulnerabilities = []

    # Check 1: Verify if YAML Intent Manifest exists and is secure
    manifest_path = "manifests/deploy-intent.yaml"
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            manifest = yaml.safe_load(f)
            actions = manifest.get("declared_intent", {}).get("actions", [])
            if "*" in actions:
                score -= 30
                vulnerabilities.append("HIGH: Wildcard permission detected in intent manifest.")
    else:
        score -= 50
        vulnerabilities.append("CRITICAL: Missing deployment intent manifest.")

    # Check 2: Check local directory security posture
    sensitive_files = [".env", "credentials.txt", "id_rsa"]
    for sf in sensitive_files:
        if os.path.exists(sf):
            score -= 20
            vulnerabilities.append(f"MEDIUM: Sensitive file found exposed in root directory: {sf}")

    print(f"\n[+] VAPT Assessment Complete.")
    print(f"[+] Posture Score: {score}/100")
    if vulnerabilities:
        print("[!] Findings Discovered:")
        for v in vulnerabilities:
            print(f"    - {v}")
    else:
        print("[+] Environment clean. No security misconfigurations found.")

    return score

if __name__ == "__main__":
    run_vapt_scan()