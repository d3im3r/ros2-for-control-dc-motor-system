# Calibración Experimental del Encoder

## Procedimiento
1. Cargar firmware de calibración serial en el ESP32.
2. Girar manualmente el eje exactamente una revolución completa ($360^\circ$).
3. Registrar los ticks leídos por el canal A en interrupción `CHANGE`.
4. Repetir 5 ensayos independientes.

## Resultados
| Ensayo | Ticks Medidos ($|N_i|$) |
| :---: | :---: |
| 1 | 960 |
| 2 | 960 |
| 3 | 960 |
| 4 | 960 |
| 5 | 960 |

### Constante Adoptada
$$N_{rev} = 960 \text{ ticks/rev}$$
```cpp
const float COUNTS_PER_REV = 960.0f;
```
