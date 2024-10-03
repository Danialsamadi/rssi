import subprocess
import numpy as np


class WiFiScanner:
    def __init__(self):
        self.ssids = []
        self.signal_strengths = []

    def scan_networks(self):
        """Scans Wi-Fi networks and extracts SSID and signal strength in dBm."""
        try:
            result = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
            data = result.decode('ASCII').split()
            self._parse_wifi_data(data)
        except subprocess.CalledProcessError as e:
            print(f"Error fetching Wi-Fi data: {e}")

    def _parse_wifi_data(self, data):
        """Extract SSID names and corresponding signal strengths from Wi-Fi data."""
        s1 = [i for i, x in enumerate(data) if x == 'SSID']
        s2 = [i for i, x in enumerate(data) if x == 'Network']

        for i in range(len(s1)):
            ssid_name = " ".join(data[s1[i] + 3:s2[i]])
            self.ssids.append(ssid_name)

        for i, value in enumerate(data):
            if value == 'Signal':
                signal_percent = data[i + 2][:-1]
                signal_dbm = (int(signal_percent) / 2) - 100
                self.signal_strengths.append(signal_dbm)

        print(f"SSIDs: {self.ssids}")
        print(f"Signal Strengths (dBm): {self.signal_strengths}")


class LocationEstimator:
    def __init__(self, access_points):
        self.access_points = access_points
        self.distances = []

    def calc_distance(self, ss, rss=-41.4568, n=3.6105, rd=1):
        """Calculates the distance based on RSSI values."""
        return rd * (10 ** ((rss - ss) / (10 * n)))

    def calculate_distances(self, signal_strengths):
        """Calculate distances from signal strengths."""
        self.distances = [self.calc_distance(ss) for ss in signal_strengths]
        print(f"Calculated Distances: {self.distances}")
        return self.distances

    def trilaterate(self, x1, y1, x2, y2, x3, y3):
        """Trilaterates to find the position based on distances from access points."""
        A = np.array([[2 * (x1 - x3), 2 * (y1 - y3)], [2 * (x2 - x3), 2 * (y2 - y3)]], dtype=float)
        B = np.array([[x1 ** 2 + y1 ** 2 - x3 ** 2 - y3 ** 2 + self.distances[0] ** 2 - self.distances[2] ** 2],
                      [x2 ** 2 + y2 ** 2 - x3 ** 2 - y3 ** 2 + self.distances[1] ** 2 - self.distances[2] ** 2]],
                     dtype=float)
        solution = np.linalg.solve(A, B)
        return solution[0][0], solution[1][0]


class SignalProcessor:
    @staticmethod
    def average_rssi(num_samples=20, delay=20):
        """Fetches and averages the RSSI over multiple readings."""
        avg = 0
        for _ in range(num_samples):
            try:
                result = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
                wifi_data = result.decode('ASCII').split()
                for i, value in enumerate(wifi_data):
                    if value == 'Signal':
                        signal_percent = wifi_data[i + 2][:-1]
                        signal_dbm = (int(signal_percent) / 2) - 100
                        avg += signal_dbm
                time.sleep(delay)
            except subprocess.CalledProcessError:
                print("Error fetching Wi-Fi data.")
                return None
        return avg / num_samples


def main():
    # Initialize Wi-Fi scanner and scan for available networks
    wifi_scanner = WiFiScanner()
    wifi_scanner.scan_networks()

    # Estimate the location based on signal strength
    location_estimator = LocationEstimator(access_points=wifi_scanner.ssids)
    distances = location_estimator.calculate_distances(wifi_scanner.signal_strengths)

    # Perform trilateration to estimate position
    x0, y0 = location_estimator.trilaterate(4.5, 4.5, 6, 3.5, 1, 0.5)
    print(f"Estimated Position: ({x0:.2f}, {y0:.2f})")


if __name__ == "__main__":
    main()
