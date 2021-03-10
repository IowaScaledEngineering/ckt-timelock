/*************************************************************************
Title:    CKT-TINYBELL Railroad Crossing Bell Circuit
Authors:  Nathan D. Holmes <maverick@drgw.net>
File:     $Id: $
License:  GNU General Public License v3

CREDIT:
    The basic idea behind this playback design came from David Johson-Davies, who
    provided the basic framework and the place where I started.

LICENSE:
    Copyright (C) 2021 Michael Petersen and Nathan Holmes

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

*************************************************************************/

#include <stdlib.h>
#include <stdbool.h>

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>
#include <util/delay.h>

#include "debouncer.h"


typedef enum
{
	STATE_LOCKED = 0,
	STATE_TIMERUN = 1,
	STATE_UNLOCKED = 2,
	STATE_RELOCKING = 3
} turnoutState_t;


volatile uint8_t timelock;

void initialize500msTimer()
{
	// Set up timer 0 for 2Hz interrupts
	TCNT1 = 0;
	OCR1A = 0x0F41;
	TCCR1A = 0;
	TCCR1B = _BV(WGM12) | _BV(CS12) | _BV(CS10);
	TCCR1C = 0;
	TIFR1 |= _BV(OCF1A);
	TIMSK1 |= _BV(OCIE1A);
}

volatile uint8_t timerPhase = 0;
ISR(TIMER1_COMPA_vect)
{
	timerPhase ^= 0xFF;

	if (timerPhase)
	{
		if (timelock)
			timelock--;
	}
}

void setTurnoutPosition(uint8_t pos)
{
	if (pos)
		PORTB = (PORTB & ~(_BV(PB1) | _BV(PB2))) | _BV(PB1);
	else
		PORTB = (PORTB & ~(_BV(PB1) | _BV(PB2))) | _BV(PB2);
}

void timelockLEDOn()
{
	PORTB |= _BV(PB0);
}

void timelockLEDOff()
{
	PORTB &= ~_BV(PB0);
}

void trackShuntOn()
{
	PORTA |= _BV(PA7);
}

void trackShuntOff()
{
	PORTA &= ~_BV(PA7);
}

uint8_t getInputState()
{
	uint8_t retval = PINA & 0x7F;
	return (~retval); // Invert since these are all negative logic (switch on = low)
}


void init_gpio()
{
	// Initialize ports 
	// Pin Assignments for PORTA/DDRA
	//  PA0 - SW1
	//  PA1 - SW2
	//  PA2 - SW3
	//  PA3 - SW4
	//  PA4 - SW5
	//  PA5 - Lock Switch
	//  PA6 - Ctrl Input
	//  PA7 - Track Shunt (output)
	DDRA  = 0b10000000;
	PORTA = 0b01111111; // Pull-ups on for all inputs

	// Pin Assignments for PORTB/DDRB
	//  PB0 - Timelock Indicator Lamp
	//  PB1 - Output Driver F
	//  PB2 - Output Driver R
	//  PB3 - /RESET (not IO)
	//  PB4 - N/A
	//  PB5 - N/A
	//  PB6 - N/A
	//  PB7 - N/A
	DDRB  = 0b00000111;
	PORTB = 0b00000000;
}

int main(void)
{
	DebounceState8_t debouncedInputs;
	turnoutState_t state = STATE_LOCKED;

	// Deal with watchdog first thing
	MCUSR = 0;                       // Clear reset status
	wdt_reset();                     // Reset the WDT, just in case it's still enabled over reset
	wdt_enable(WDTO_1S);             // Enable it at a 1S timeout.
	cli();

	init_gpio();
	initDebounceState8(&debouncedInputs, getInputState());

	sei();
	while(1)
	{
		wdt_reset();
		debounce8(getInputState(), &debouncedInputs);
		if(debouncedInputs.debounced_state & _BV(PA5))
		{
			timelockLEDOn();
			trackShuntOn();
			setTurnoutPosition(1);
		} else {
			timelockLEDOff();
			trackShuntOff();
			setTurnoutPosition(0);
		}
	}

}

