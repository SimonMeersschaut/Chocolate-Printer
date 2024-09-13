# Chocolate Printer

## Components

### 1. Printer Temperature Conversion

| Resistance (\Ohm) | Printer Temperature |
| ----------------- | ------------------- |
| 217               | 253                 |
| 555               | 200                 |
| 558               | 200                 |
| 559               | 200                 |
| 994               | 172                 |
| 1000              | 173                 |
| 4500              | 111                 |
| 4600              | 111                 |
| 9720              | 85                  |
| 1190              | 164                 |
| 19500             | 65                  |
| 30000             | 54                  |
| 81000             | 25                  |
| 100000            | 25                  |

![alt text](<images/Temperature sensor.png>)

### 2. Temperature Sensor

    - NTC 10K
    - B57164 - K103 - K

    25°C = 6.000 Ohm

    50°C = 2000 Ohm (target: 1000Ohm)
    => parralel: 2 KOhm

### 3. Heating Element

![alt text](<images/Voltage by Temperature.png>)

    - Original:
      - Resistance: 15 Ohm
    - New
      - Resistance 10.51 Ohm
      - Length: 297 cm

### 4. Extrusion Motor

    - First Set:
      - 1A: 1
      - 1B: 4
    - Second Set
      - 2A: 3
      - 2B: 6

### 5. Stepper Motor

Creality CR - M4 42-34 Motor

    24V DC
    0.84A
    Holding Torque
    – 2.86kg.cm Typ.

Controller

    Type: A4988

![alt text](images/A4988.bmp)

GRBL docs: https://github.com/grbl/grbl
