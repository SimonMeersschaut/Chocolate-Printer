/*
AUTHOR: Simon Meersschaut

TODO: documentation
*/


#ifndef TEMPERATURE_H
#define TEMPERATURE_H

#include <stdint.h>   // for uint8_t, uint16_t
#include <math.h>
#include <avr/io.h>

// Pin mapping for RAMPS1.4 thermistors
// A13 = T0, A14 = T1, A15 = T2
#define T0_SENSOR_PIN 13

// Config — adjust if you know your exact thermistor
#define PULLUP_R_OHM   4700.0    // RAMPS typical pullup 4.7k
#define THERM_R0_OHM   100000.0  // R0 = 100k at 25°C
#define BETA_VALUE     3950.0    // common for Ender stock thermistors
#define T0_KELVIN      298.15    // 25°C = 298.15 K




void adc_init(void);
uint16_t read_adc(uint8_t channel);
void temperature_init(void);
double t0_get_temperature_celsius(void);

#endif
