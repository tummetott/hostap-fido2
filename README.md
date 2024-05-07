# 802.1X EAP-TLS Wi-Fi Network with FIDO authentication

This repository contains a quick and dirty proof-of-concept implementation, that
uses the `OpenSSL` extension [fidoSSL](https://github.com/tummetott/fidoSSL) in
`hostapd` and `wpa_supplicant` in order to create a Wi-Fi network that uses
802.1X EAP-TLS with an external FIDO hardware token as authentication mechanism.

This implementation is not meant for production!

## Dependencies

On Ubuntu, dependencies can be installed with [aptitude](https://wiki.ubuntuusers.de/aptitude/).
Unfortunately I found no solution to compile it on macOS, since the code depends
on `libnl`. 

```sh
# Update apt in order to get the newest packages sources
sudo apt update

# Install dependencies
sudo apt install build-essential libssl-dev libfido2-dev libsqlite3-dev  libjansson-dev \
        checkinstall pkg-config libnl-genl-3-dev libnl-route-3-dev libdbus-1-dev
```

## Build

First, we need to configure the hostapd build. From the root of the repository,
run the following:

```sh
cp hostapd/defconfig hostapd/.config
cp wpa_supplicant/defconfig wpa_supplicant/.config
```

Open both `.config` files and add the following line, so the FIDO extension is
compiled into `hostapd` and `wpa_supplicant`.

```config
CONFIG_FIDO=y
```

Next, compile the supplicant and the access point with:

```
pushd hostapd
make

popd
pushd wpa_supplicant
make
```

## Config files

#### `hostapd.conf`

```bash
## Basic network configuration settings:

# Interface used by the access point
interface=wlan0

# SSID of the Wi-Fi network
ssid=DemoNetwork

# Wireless mode, g for 2.4 GHz
hw_mode=g

# Wi-Fi channel to use
channel=6

# Authentication algorithm; 1 for open system
auth_algs=1

# Broadcast SSID; 0 to enable SSID broadcasting
ignore_broadcast_ssid=0

# WPA2 only
wpa=2

# Key management set to WPA-EAP for enterprise networks
wpa_key_mgmt=WPA-EAP

# WPA pairwise encryption method
wpa_pairwise=CCMP

# WPA2 pairwise encryption method
rsn_pairwise=CCMP

# Enables 802.1X authentication
ieee8021x=1

# Internal EAP server enabled
eap_server=1

# Path to EAP user database file
eap_user_file=/path/to/eap_user_file

# Path to CA certificate file
ca_cert=/path/to/ca.crt

# Path to server's certificate
server_cert=/path/to/server.crt

# Path to server's private key
private_key=/path/to/server.key

# Enables TLS version 1.3
tls_flags=[ENABLE-TLSv1.3]

## FIDO2-specific configurations:

# Relying Party identifier for FIDO
fido_rp_id=demo.fido2.tls.edu

# Descriptive name for the Relying Party
fido_rp_name=Demo_FIDO2_TLS

# User verification policy (required, preferred, discouraged)
fido_user_verification=required

# Policy for device-resident keys (required, preferred, discouraged)
fido_resident_key=required

# Type of authenticator attachment (cross-platform or platform)
fido_auth_attach=cross-platform

# Transport protocol for the FIDO device (usb, nfc, ble, internal)
fido_transport=usb

# Timeout for FIDO operations in milliseconds
fido_timeout=30000

# Debug level for FIDO operations: 1 for errors, 2 for verbose, 3 for very verbose
fido_debug_level=2

```

#### `supplicant.conf`

```bash
ctrl_interface=/var/run/wpa_supplicant

network={
    ssid="DemoNetwork"
    scan_ssid=1
    key_mgmt=WPA-EAP
    eap=TLS
    identity="Alice"
    ca_cert="/path/to/ca.crt"
    client_cert="/path/to/client.crt"
    private_key="/path/to/client.key"
}
```

#### `eap user file`

```bash
# EAP User File for hostapd
# Each line defines an EAP user

"Alice" TLS
```


## Troubleshooting

A good resource on how to compile and run `hostapd` and `wpa_supplicant`:
[link](https://wireless.wiki.kernel.org/en/users/documentation/hostapd)
