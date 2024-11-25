import subprocess
import re

def get_wifi_passwords():
    # Get the output from the netsh command
    result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)

    # Extract WiFi names
    wifi_names = re.findall(r'All User Profile\s*:\s*(.*)', result.stdout)

    wifi_passwords = {}
    
    for wifi in wifi_names:
        # Get the password for each WiFi network
        result = subprocess.run(['netsh', 'wlan', 'show', 'profile', wifi, 'key=clear'], capture_output=True, text=True)
        password = re.search(r'Key Content\s*:\s*(.*)', result.stdout)
        
        if password:
            wifi_passwords[wifi] = password.group(1)
        else:
            wifi_passwords[wifi] = None  # No password found

    return wifi_passwords

if __name__ == "__main__":
    passwords = get_wifi_passwords()
    for wifi, password in passwords.items():
        if password:
            print(f'WiFi: {wifi}, Password: {password}')
        else:
            print(f'WiFi: {wifi}, Password: Not found or open network')
