#include "temperature.h"
#include <avr/io.h>   // for ADMUX, ADCSRA, etc.


#define EXTRUDER_HEATER_PORT PORTB
#define EXTRUDER_HEATER_DDR  DDRB
#define EXTRUDER_HEATER_PIN  4 // digital pin 10 on arduino Mega

// PUBLIC FUNCTIONS

void temperature_init(void){
    adc_init();
    extruder_heater_init();
}

double last_t0_reading = 0;
double t0_target_temperature = 0;

void update_temperature(void){
    // update temperature reading
    uint16_t adc = read_adc(T0_SENSOR_PIN); // ensure T0_SENSOR_PIN defined as ADC channel number
    double c = adc_to_celsius_beta(adc);
    // if (isnan(c)) return 0xFFFF; // error code
    last_t0_reading = c;

    // set extruder heating    
    if (last_t0_reading >= t0_target_temperature){
        // too hot, turn heating off
        EXTRUDER_HEATER_PORT &= ~(1 << EXTRUDER_HEATER_PIN);
    }

    if (last_t0_reading < t0_target_temperature){
        // too cold, turn heating on
        EXTRUDER_HEATER_PORT |= (1 << EXTRUDER_HEATER_PIN);
    }
}

// Convenience wrapper for T0 sensor (assuming T0_SENSOR_PIN is channel number)
double get_extruder_temperature(void) {
    return last_t0_reading;
}

void set_extruder_temperature(double target) {
    t0_target_temperature = target;
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
// Returns NaN if ADC is exactly 0 or 1023 (open/short).
double adc_to_celsius_beta(uint16_t adc_value)
{
    if (adc_value == 0 || adc_value >= 1023) { return 0; } // NAN

    double adc = (double) adc_value;
    // compute thermistor resistance from divider
    double r_therm = PULLUP_R_OHM * (adc / (1023.0 - adc));

    // B-parameter equation: 1/T = 1/T0 + (1/B) * ln(R/R0)
    double invT = (1.0 / T0_KELVIN) + (1.0 / BETA_VALUE) * log(r_therm / THERM_R0_OHM);

    double tempK = 1.0 / invT;
    double tempC = tempK - 273.15;

    return tempC;
}

void extruder_heater_init(void) {
    // Set pin as output
    EXTRUDER_HEATER_DDR |= (1 << EXTRUDER_HEATER_PIN);
}