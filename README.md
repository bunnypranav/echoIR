# EchoIR
![image](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MTEyMzAzLCJwdXIiOiJibG9iX2lkIn19--b5351d5cba5a79004f6b0b1f036364e221b21c53/image.png)

This is an IR hub, with both an IR receiver and a handful of transmitters, which can control my IR appliances, like the AC, fan, and TV, with my phone and over the internet. It wouldn't replace the remotes, but it could learn their signals and replay them whenever I want from my phone.

# Schematic
*Made in KiCad*

On the left side is the USB-C connector, going into the polyfuse, then into the +5V rail. The three IR LEDs each have their own 33-ohm resistor and connect from +5V to the IRLEDNODE. When the MOSFET turns on, current flows through all three LEDs to ground. The TSOP38238 receiver runs from +3.3V, which comes from the Pico's internal regulator. There is a 100nF capacitor and a 4.7uF capacitor close to it, because IR receivers are sensitive to noise. The button connected to GPIO 14 controls the "record" mode, with its status led just being the inbuild Pi led at GPIO25.

![page_1](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MTA5MjQ3LCJwdXIiOiJibG9iX2lkIn19--2f004636d84b69bf3c7ba1875538e1916b5b8ca3/page_1.png)

# PCB
*Made in KiCad*
![pcb](https://blueprint.hackclub.com/user-attachments/blobs/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MTEyMzAyLCJwdXIiOiJibG9iX2lkIn19--739b4251a62233c70dc10884b5ee17d4c09a9169/image.png)
![pcb2](images/image.png)