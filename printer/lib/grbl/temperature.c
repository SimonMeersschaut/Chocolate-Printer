#include "temperature.h"
#include <avr/io.h>   // for ADMUX, ADCSRA, etc.

#define HEATER_PORT PORTB
#define HEATER_DDR  DDRB

// PUBLIC FUNCTIONS

void temperature_init(void){
    adc_init();

    // Init heater pins
    HEATER_DDR |= (1 << SYRINGE_HEATER_PIN);
    HEATER_DDR |= (1 << EXTRUDER_HEATER_PIN);
}

// Syringe (T0) state
double last_t0_reading = 0;
double t0_target_temperature = 20;

// Extruder (T1) state
double last_t1_reading = 0;
double t1_target_temperature = 20;

void update_temperature(void){
    // --- T0 (syringe) ---
    uint16_t adc0 = read_adc(T0_SENSOR_PIN);
    double c0 = adc_to_celsius_beta(adc0);
    last_t0_reading = c0;

    if (last_t0_reading >= t0_target_temperature) {
        HEATER_PORT &= ~(1 << SYRINGE_HEATER_PIN); // off
    } else {
        HEATER_PORT |= (1 << SYRINGE_HEATER_PIN);  // on
    }

    // --- T1 (extruder) ---
    uint16_t adc1 = read_adc(T1_SENSOR_PIN);
    double c1 = adc_to_celsius_beta(adc1);
    last_t1_reading = c1;

    if (last_t1_reading >= t1_target_temperature) {
        HEATER_PORT &= ~(1 << EXTRUDER_HEATER_PIN); // off
    } else {
        HEATER_PORT |= (1 << EXTRUDER_HEATER_PIN);  // on
    }
}

// Convenience wrappers for T0 (syringe)
double get_syringe_temperature(void) {
    return last_t0_reading;
}
void set_syringe_temperature(double target) {
    t0_target_temperature = target;
}

// Convenience wrappers for T1 (extruder)
double get_extruder_temperature(void) {
    return last_t1_reading;
}
void set_extruder_temperature(double target) {
    t1_target_temperature = target;
}

// HELPER FUNCTIONS

void adc_init(void) {
    ADCSRA = (1 << ADEN)
           | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // prescaler 128
    ADMUX = (1 << REFS0); // AVcc reference
}

uint16_t read_adc(uint8_t channel) {
    ADMUX = (ADMUX & 0xE0) | (channel & 0x07);
    ADCSRB = (ADCSRB & ~(1 << MUX5)) | ((channel & 0x08) ? (1 << MUX5) : 0);
    ADCSRA |= (1 << ADSC);
    while (ADCSRA & (1 << ADSC));
    return ADC;
}

// Returns temperature in degrees Celsius as double.
double adc_to_celsius_beta(uint16_t adc_value)
{
    if (adc_value == 0 || adc_value >= 1023) { return 0; } // error / open thermistor

    double adc = (double) adc_value;
    double r_therm = PULLUP_R_OHM * (adc / (1023.0 - adc));

    double invT = (1.0 / T0_KELVIN) + (1.0 / BETA_VALUE) * log(r_therm / THERM_R0_OHM);

    double tempK = 1.0 / invT;
    return tempK - 273.15;
}
