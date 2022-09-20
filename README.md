# Sommer Pro+ Garage Door Control
<img src="sommerpro.svg" width="200" algin="right">
This ESP8266-based controller allows to remotely steer the [Sommer Pro+](https://www.sommer.eu/de/sommer-pro-plus.html) Garage door control.

It connects to an MQTT broker and listens on one topic `<device-name>/comand` to steer the garage door and updates it state in real-time at `<device-name>/isclosed`. In my case I use [IOBroker MQTT adapter](https://github.com/ioBroker/ioBroker.mqtt) in server mode as broker, but it also works with Mosquito and such.

## MQTT broker topics
| Topic | Values | Description |
|-------|--------|-------------|
|`<device-name>/command`| `open`, `close` | Trigger the door to open/close. |
|`<device-name>/isclosed` | `true`, `false` | Current status of the door. |

## Board
Please refer to the [board design description](board/README.md) for more information about the board. This repo contains all files required to print/assemble it yourself.

## Alternatives
- Sommer in their online document-library provide a set of instructions on how to connect the garage door control to Somfy's Tahoma box: https://downloads.sommer.eu/files/Anbindung-base+pro+anSomfyTahomaBoxRaccordementdebase+pro+laSomfyTahomaBox_S12360-00000.pdf. However there are (from my perspective) some issues with it.
  - Somfy GU Controller io Art. No. 1841211 is required, which is a) very expensive and b) hardly available, as apparently Somfy stopped manifacturing it (for unknown reason)
  - You also need the Somfy Tahoma box ($$$) to make any use of it
- There is a custom-built solution based on Arduino described/sold here: https://arduino-projekte.info/homekit-garagentor-und-drehtoroeffner-eps8266-arduino-hoermann-sommer-antriebe/
  - Although quite cool, it offers no integration with Sommer Relay (Art. 7042V000), only with Sommer Connex (Art. S10807-00001), meaning you can steer the garage door, but will not know if it actually is opened or closed.
  - Software-wise it integrates directly with Homekit (Apple Smarthome), making it unusable for my smarthome setup.