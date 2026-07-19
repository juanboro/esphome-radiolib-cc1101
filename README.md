# esphome-radiolib-cc1101
Uses [Radiolib](https://github.com/jgromes/RadioLib) to enable a TI-CC1101 module as an ESPHome RF direct OOK remote receiver/transmitter.  See note below - there is now a built in CC1101 component in ESPHome - so use that unless you want to experiment with the extras offered by RadioLib.
# Basics
The included yaml files include configuration examples for ESP8266 and ESP32 micro-controllers.  You should start by enabling dump_raw and making sure noise isn't being received when no transmissions are occurring.  Adjusting bandwidth, data-rate, and AGC parameters can help with creating an optimal receive setup.  The example includes the ability to expose these as controls in ESPHome or HomeAssistant.  
- More bandwidth will likely enable receiving more varying devices on the same frequency, but will increase noise and may decrease range.

## debugging signals
The ESP32 example includes an example UDP dumper that can help with analyzing pulse data. 
- Use rtl_433 on a host with the socat tool to decode pulses streamed to udp broadcast:
```socat -u UDP4-RECV:5009 STDOUT | rtl_433 -r ook:-```

## rtl_433 decoding with ESPHome directly
See [esphome-rtl_433-decoder](https://github.com/juanboro/esphome-rtl_433-decoder)

## notes
- Transmit/Receive was verified to work with esp8266 and ESP-32 board.

# see also:
 - Direct cc1101 support is now available directly in an ESPHOME component (no radiolib dependency): [cc1101 componen](https://esphome.io/components/cc1101/).
# based on:
- https://github.com/dbuezas/esphome-cc1101
- and https://github.com/NorthernMan54/rtl_433_ESP/blob/main/src/rtl_433_ESP.cpp
- and https://github.com/smartoctopus/RadioLib-esphome/blob/master/examples/CC1101/CC1101_Settings/CC1101_Settings.ino
- and https://github.com/LSatan/SmartRC-CC1101-Driver-Lib
