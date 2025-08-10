#include "temperature.h"
#include <avr/io.h>   // for ADMUX, ADCSRA, etc.

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

void temperature_init(void){
    adc_init();
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

// Convenience wrapper for T0 sensor (assuming T0_SENSOR_PIN is channel number)
double t0_get_temperature_celsius(void) {
    uint16_t adc = read_adc(T0_SENSOR_PIN); // ensure T0_SENSOR_PIN defined as ADC channel number
    double c = adc_to_celsius_beta(adc);
    if (isnan(c)) return 0xFFFF; // error code
    return c;
    // return temperature in centi-degrees (°C * 100) as integer to avoid floats in comms
    // int32_t scaled = (int32_t)round(c * 100.0);
    // if (scaled < -32768) scaled = -32768;
    // if (scaled > 32767) scaled = 32767;
    // return (uint16_t)scaled;
}