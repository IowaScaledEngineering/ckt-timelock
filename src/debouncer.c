#include "debouncer.h"

void initDebounceState8(DebounceState8_t* d, uint8_t initialState)
{
	d->clock_A = d->clock_B = 0;
	d->debounced_state = initialState;
	
	// Run the vertical counters so there's no glitch
	for(uint8_t i=0; i<4; i++)
		debounce8(initialState, d);
	
}

uint8_t debounce8(uint8_t raw_inputs, DebounceState8_t* d)
{
	uint8_t delta = raw_inputs ^ d->debounced_state;   //Find all of the changes
	uint8_t changes;

	d->clock_A ^= d->clock_B;                     //Increment the counters
	d->clock_B  = ~d->clock_B;

	d->clock_A &= delta;                       //Reset the counters if no changes
	d->clock_B &= delta;                       //were detected.

	changes = ~((~delta) | d->clock_A | d->clock_B);
	d->debounced_state ^= changes;
	return(changes & ~(d->debounced_state));
}
