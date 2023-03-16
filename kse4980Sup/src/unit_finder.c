#include <registryFunction.h>
#include <aSubRecord.h>
#include <epicsExport.h>

#include "unit_finder.h"

long work_out_units(aSubRecord *prec)
{
    return WorkOutUnits(prec);
}

epicsRegisterFunction(work_out_units);
