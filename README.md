
# Wi-Fi Scanner with Signal Strength Analysis

This Python program scans for nearby Wi-Fi networks, extracts their SSIDs, and measures their signal strengths in dBm. It leverages the `netsh` command (Windows) to gather network information and parses the data for further processing or analysis.

---

## Features
- **Wi-Fi Network Scanning**: Identifies all available Wi-Fi networks in the vicinity.
- **Signal Strength Measurement**: Extracts signal strength (in dBm) for each detected network.
- **Data Parsing**: Efficiently parses raw network data to isolate SSIDs and signal values.
- **Expandable**: Can be extended for additional tasks like network prioritization or distance estimation.

---

## Prerequisites
1. **Operating System**: The program uses the `netsh` command, so it works on **Windows** systems.
2. **Python**: Ensure Python 3.x is installed.
3. **Permissions**: Administrative privileges may be required to run the `netsh` command.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Danialsamadi/rssi.git
   cd repository-name
   ```

2. **Run the Program**:
   Execute the Python script to scan Wi-Fi networks:
   ```bash
   python wifi_scanner.py
   ```

---

## Usage

The script scans for Wi-Fi networks and outputs the detected SSIDs and their signal strengths. Below is an example workflow:

```python
from wifi_scanner import WiFiScanner

scanner = WiFiScanner()
scanner.scan_networks()

print("Available Networks:")
for ssid, signal in zip(scanner.ssids, scanner.signal_strengths):
    print(f"SSID: {ssid}, Signal Strength: {signal} dBm")
```

---

## Limitations
- Works only on **Windows** (uses `netsh` command).
- Requires administrative privileges to access Wi-Fi data.
- Signal strengths depend on environmental factors (e.g., interference, distance).

---

## License
This project is open-source and available under the MIT License.

---

## Contributions
Feel free to fork the repository, submit issues, or make pull requests for improvements.

---

