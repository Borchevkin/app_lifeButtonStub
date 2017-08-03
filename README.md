# app_lifeButtonStub
Life Button Stub repository

## Adaptation for your case

Please change ***PORT_NAME*** according to your system

## Settings of serial port

* Speed - 115200

* Data bits - 8

* Parity - None

* Flow control - Hardware (CTS/RTS)

## Working requests

### Heart Rate Single measurement

For get answer need to send in hex (following data in hex convinient for copy to terminal) :

*AB 05 FF 31 09 00 FF*

Answer will be *0xAB 0x04 0xFF 0x31 0x09 0x44*

### SPO2 Single Measurement

For get answer need to send in hex (following data in hex convinient for copy to terminal) :

*AB 05 FF 31 11 00 FF*

Answer will be *0xAB 0x04 0xFF 0x31 0x11 0x22*

### Unhadled request or errors

If the stub received wrong request it response by *FF FF FF FF*