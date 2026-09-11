# Experimental Encoder Calibration

## Procedure
1. Flash the serial calibration firmware to the ESP32.
2. Manually rotate the motor output shaft exactly one full revolution ($360^\circ$).
3. Record ticks read by Channel A on hardware interrupt (`CHANGE`).
4. Repeat across 5 independent trials.

## Results
| Trial | Measured Ticks ($\lvert N_i \rvert$) |
| :---: | :---: |
| 1 | 960 |
| 2 | 960 |
| 3 | 960 |
| 4 | 960 |
| 5 | 960 |

### Adopted Constant
$$N_{\mathrm{rev}} = 960\ \text{ticks/rev}$$
```cpp
const float COUNTS_PER_REV = 960.0f;
```
