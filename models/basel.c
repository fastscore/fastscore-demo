#include <fastscore.h>
#include <assert.h>
#include <stdio.h>
#include <math.h>

void begin(){}

void action(fastscore_value_t v, int slot, int seqn)
{
	assert(v.fmt == FASTSCORE_FMT_JSON);

	int n = json_integer_value(v.js);

	float b = 0.0f;
	for (int i = 0; i < n; i++)
	{
		b += 1 / (i * i);
	}

	b *= 6;
	b = sqrt(b);
	
	fastscore_value_t o;
	o.fmt = FASTSCORE_FMT_JSON;
	o.js = json_integer(b);

	fastscore_emit(o, 1);
}

void end1(){}
