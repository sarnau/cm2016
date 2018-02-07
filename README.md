# Charge Master 2016 Serial Protocol

The Voltcraft (Conrad) Charge Master 2016 has a completely different protocol from the CM2010 and other devices.

The USB port is still a serial port which is `/dev/cu.SLAB_USBtoUART` on my Mac. Every second the device sends a package with 19200 baud 8N1. I've written a simple python script to demonstrate reading and interpreting the data. For actual use you should add some error handling.

Only one byte in the slot header is unknown (it seems the Windows software is also not using it) and the device header has a few semi-unknown ones (the version, the temperature, etc) – only the chemical setting is actually used by the Window software.