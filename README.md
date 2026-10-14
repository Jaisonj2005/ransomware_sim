# Educational Ransomware Simulator 🚨

A Python-based cryptographic simulation designed for Incident Response and SOC training. This tool safely demonstrates how malicious payloads leverage Advanced Encryption Standard (AES) to lock file systems and extort organizations.

**Features:**
* Strictly implements a closed-loop sandbox environment, dynamically generating a targeted test directory to ensure host system safety.
* Leverages the `cryptography.fernet` module to perform legitimate, mathematically sound symmetric encryption (AES-128) on target files.
* Simulates the exact lifecycle of a ransomware infection: Key Generation -> File Discovery -> Iterative Data Encryption -> Extension Appending (`.LOCKED`).
* Includes a fully functional decryption recovery mechanism simulating the application of a purchased threat-actor decryption key.

*Built as the Day 30 Finale of a 30-Day Network Engineering & Security portfolio streak. For educational use only.*
