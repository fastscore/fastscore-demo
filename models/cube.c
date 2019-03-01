#include <fastscore.h>
#include <assert.h>

void begin()
{

}

void action(fastscore_value_t v, int slot, int seqn)
{
	assert(v.fmt == FASTSCORE_FMT_JSON);

	int x = json_integer_value(v.js);
	int x3 = x*x*x;

	fastscore_value_t o;
	o.fmt = FASTSCORE_FMT_JSON;
	o.js = json_integer(x3);

	fastscore_emit(o, 1);
}

void end1()
{
}
