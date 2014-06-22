#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/wdt.h>
#include <util/delay.h>

typedef enum
{
	STATE_LOCKED = 0,
	STATE_TIMERUN = 1,
	STATE_UNLOCKED = 2,
	STATE_RELOCKING = 3
} turnoutState_t;

#define MODE_TIMELOCK 1
#define MODE_DUALCNTL 0

uint8_t configTimelock()
{
	// Returns 1 if configured for timelock, 0 if configured for dual-control
	// There's no debounce here because it shouldn't be changing at runtime
	return ((PINC & _BV(PC4))?MODE_TIMELOCK:MODE_DUALCNTL);
}

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
		PORTC |= _BV(PC7);
	else
		PORTC &= ~_BV(PC7);
}

void timelockLEDOn()
{
	PORTD |= _BV(PD2);
}

void timelockLEDOff()
{
	PORTD &= ~_BV(PD2);
}

void auxLEDOn()
{
	PORTD |= _BV(PD4);
}

void auxLEDOff()
{
	PORTD &= ~_BV(PD4);
}

void trackShuntOn()
{
	PORTD |= _BV(PD3);
}

void trackShuntOff()
{
	PORTD &= ~_BV(PD3);
}

#define UNLOCK_SWITCH_MASK  (_BV(0))
#define MANUAL_DIR_MASK     (_BV(1))
#define INPUT_DIR_MASK      (_BV(2))

uint8_t debounceInputs(uint8_t* ioState)
{
	//  Bit 0 - PD0 - Lock/Manual Control switch (in, needs pullup on)
	//  Bit 1 - PD1 - Manual Control direction (in, needs pullup on)
	//  Bit 2 - PC5 - Input Turnout Dir (in, needs pullup on)
	static uint8_t clock_A=0, clock_B=0;
	uint8_t rawInput = ((PINC & _BV(PC5))>>3) | (PIND & (_BV(PD0) | _BV(PD1)));
	uint8_t delta = rawInput ^ *ioState;
	uint8_t changes;

	clock_A ^= clock_B;                     //Increment the counters
	clock_B  = ~clock_B;
	clock_A &= delta;                       //Reset the counters if no changes
	clock_B &= delta;                       //were detected.
	changes = ~((~delta) | clock_A | clock_B);
	*ioState ^= changes;	

	return(changes);
}

uint8_t unlockSwitchOn(uint8_t ioState)
{
	if (0 == (ioState & _BV(0)))
		return(1);
	else
		return(0);
}

uint8_t getInputTurnoutPosition()
{
	return ((PINC & _BV(PC5))?1:0);
}

uint8_t getTimeIntervalInSecs()
{
	uint8_t configSwitchValue = (~PINC) & 0x0F;
	const uint8_t timeValues[16] = { 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 90, 120, 180, 240 };

	return(timeValues[configSwitchValue]);
}

void blinkAndDie()
{
	while(1)
	{
		PORTD ^= _BV(PD4);// | _BV(PD3) | _BV(PD4);
		_delay_ms(200);
	}
}

int main(void)
{
	uint8_t moduleMode = 0;
	uint8_t defaultTurnoutPosition = 1;
	uint8_t ioState = 0xFF;
	turnoutState_t state = STATE_LOCKED;

	// Deal with watchdog first thing
	MCUSR = 0;								// Clear reset status
//	wdt_disable();
//	WDTCSR = _BV(WDP3);		// Enable WDT (4s)

	// Initialize ports 
	// Pin Assignments for PORTA/DDRA
	//  PA0 - Not used
	//  PA1 - Not used
	//  PA2 - Not used
	//  PA3 - Not used
	//  PA4 - N/A (doesn't exist)
	//  PA5 - N/A (doesn't exist)
	//  PA6 - N/A (doesn't exist)
	//  PA7 - N/A (doesn't exist)
	DDRA  = 0b00001111;
	PORTA = 0b00000000;

	// Pin Assignments for PORTB/DDRB
	//  PB0 - Not used
	//  PB1 - Not used
	//  PB2 - Not used
	//  PB3 - MOSI (in,pulled up)
	//  PB4 - MISO (in)
	//  PB5 - SCK (in)
	//  PB6 - Not used
	//  PB7 - Not used
	DDRB  = 0b11000111;
	PORTB = 0b00111000;

	// Pin Assignments for PORTC/DDRC
	//  PC0 - Cfg Switch 1 (in, needs pullup on)
	//  PC1 - Cfg Switch 2 (in, needs pullup on)
	//  PC2 - Cfg Switch 3 (in, needs pullup on)
	//  PC3 - Cfg Switch 4 (in, needs pullup on)
	//  PC4 - Cfg Switch 5 (in, needs pullup on)
	//  PC5 - Input Turnout Dir (in, needs pullup on)
	//  PC6 - N/A (/RESET pin)
	//  PC7 - Output Turnout Dir (output)
	DDRC  = 0b10000000;
	PORTC = 0b11111111;

	
	// Pin Assignments for PORTD/DDRD
	//  PD0 - Lock/Manual Control switch (in, needs pullup on)
	//  PD1 - Manual Control direction (in, needs pullup on)
	//  PD2 - Time running LED (out)
	//  PD3 - Track shunt relay (out)
	//  PD4 - Aux onboard LED (out)
	//  PD5 - N/A (doesn't exist)
	//  PD6 - N/A (doesn't exist)
	//  PD7 - N/A (doesn't exist)
	DDRD  = 0b00011100;
	PORTD = 0b00000011;

	initialize500msTimer();
	moduleMode = configTimelock();
	if (MODE_TIMELOCK == moduleMode)
		defaultTurnoutPosition = (PIND & _BV(PD1))?1:0;

	sei();

	// TIME_RUN - passes ctrl in to ctrl out

	while(1)
	{
		wdt_reset();
		debounceInputs(&ioState);

		if (MODE_TIMELOCK == moduleMode)
		{
			// Timelocked Manual Switch Simulator
			switch(state)
			{
				// STATE_LOCKED - holds turnout in default position	
				case STATE_LOCKED:
					timelock = 0;
					setTurnoutPosition(defaultTurnoutPosition);
					trackShuntOff();
					timelockLEDOff();

					if (unlockSwitchOn(ioState))
					{
						timelock = getTimeIntervalInSecs();
						state = STATE_TIMERUN;
					}
					break;
			
				case STATE_TIMERUN:
					setTurnoutPosition(defaultTurnoutPosition);
					trackShuntOn();
					if (timerPhase) 
						timelockLEDOn();
					else
						timelockLEDOff();

					if (0 == timelock)
						state = STATE_UNLOCKED;

					break;
			
				case STATE_UNLOCKED:
					trackShuntOn();
					timelockLEDOn();
					setTurnoutPosition(getInputTurnoutPosition());
					
					// If the user has moved the turnout back to the default position
					// and released the lock, return to the locked up state
					if (!unlockSwitchOn(ioState) 
						&& getInputTurnoutPosition() == defaultTurnoutPosition)
					{
						// Give the switch machine two seconds to lock back up
						setTurnoutPosition(defaultTurnoutPosition);
						timelock = 2;
						state = STATE_RELOCKING;
					}
					break;

				case STATE_RELOCKING:
					if (0 == timelock)
						state = STATE_LOCKED;
					break;

				default:
					state = STATE_LOCKED;
					break;
			}
		}
		else
		{
			// Dual Control Power Switch Simulator
		
		}

		// Wait 10mS before we get the inputs again and debounce again
		_delay_ms(10);
	}
}

