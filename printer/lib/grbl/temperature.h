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
#define T1_SENSOR_PIN 14

#define SYRINGE_HEATER_PIN  4 // digital pin 10 on arduino Mega
#define EXTRUDER_HEATER_PIN  5 // digital pin 11 on arduino Mega

// Config — updated for 10k NTC thermistor
#define PULLUP_R_OHM 4700.0
#define THERM_R0_OHM   10000.0    // thermistor resistance at 25°C = 10kΩ
#define BETA_VALUE     3950.0     // datasheet value for MF52-103
#define T0_KELVIN      298.15     // 25°C = 298.15 K

#define TEMPERATURE_MARGIN 2      // allowable deviation in °C

void adc_init(void);
uint16_t read_adc(uint8_t channel);
void temperature_init(void);
double adc_to_celsius_beta(uint16_t);

double get_syringe_temperature(void);
void set_syringe_temperature(double);

double get_extruder_temperature(void);
void set_extruder_temperature(double);

void update_temperature(void);

#endif
