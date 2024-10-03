import subprocess
import numpy as np
import time
import math


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

    @staticmethod
    def estimate_path_loss():
        """Uses linear regression to estimate the RSSI and path loss exponent."""
        rssi_values = []
        for _ in range(10):
            avg_rssi = SignalProcessor.average_rssi()
            if avg_rssi:
                rssi_values.append(avg_rssi)
            time.sleep(5)

        Y = np.array(rssi_values).reshape((10, 1))
        Z = np.array([[1, -10 * math.log10(d)] for d in [1.5, 2, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5]])

        Z_trans = Z.T
        A = np.linalg.inv(Z_trans @ Z)
        B = Z_trans @ Y
        X = A @ B

        rss = X[0][0]
        n = X[1][0]

        print(f"Reference RSS: {rss:.2f} dBm")
        print(f"Path Loss Exponent: {n:.2f}")


if __name__ == "__main__":
    SignalProcessor.estimate_path_loss()
