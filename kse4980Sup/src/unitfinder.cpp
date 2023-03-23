#include <string.h>
#include <stdlib.h>
#include <registryFunction.h>
#include <aSubRecord.h>
#include <menuFtype.h>
#include <errlog.h>
#include <epicsString.h>
#include <epicsExport.h>
#include "epicsTypes.h"
#include "subRecord.h"
#include <unordered_map>


#include "unit_finder.h"

long WorkOutUnits(aSubRecord *prec) {
    // INPA - func (string)
    // OUTA - first reading (need to set egu on this)
    // OUTB - secondary reading (need to set egu on this)
    std::string first_meas, second_meas;


    epicsOldString* rec = (epicsOldString*)(prec->vala);
    char buffer[sizeof(epicsOldString)+1];  // +1 for null terminator in the case where epics str is exactly 40 chars (unterminated)
    buffer[sizeof(epicsOldString)] = '\0';
    std::string s(strncpy(buffer, *rec, sizeof(epicsOldString)));

    
    std::unordered_map<std::string, std::string> egus = {
        {"CP", "F"},
        {"CS", "F"}, 
        {"R", "Ohms"},
        {"LP", "H"},
        {"LS", "H"},
        {"D", ""},
        {"Z", "Ohms"},
        {"TD", "deg"},
        {"TR", "rad"},
        {"G", "S"},
        {"Y", "S"},
        {"VD", "V"}, 
        {"ID", "A"},
        {"RS", ""}, 
        {"Q", ""},
        {"RP", "Ohms"},
        {"RD", "Ohms"},
        {"B", "S"},
    };

    // if len is 2 then split down the middle 
    // if len is 3 then use first 2 chars
    // if len is 4 then use first 2 chars and last 2 chars
    // if begins with Z or Y use 1 char for first and 2 for second

    auto first_char = s.at(0);
    if (first_char == 'Y' || first_char == 'Z')
    {
        first_meas = first_char;
        second_meas = s.at(1) + s.at(2);
    }
    else {
        switch(s.length()){
            case 2:
                first_meas = first_char;
                second_meas = s.at(1);
                break;
            case 3:
                first_meas = first_char + s.at(1);
                second_meas = s.at(2);
                break;
            case 4:
                first_meas = first_char + s.at(1);
                second_meas = s.at(2) + s.at(3);
                break;
            default:
                return 1;
        }
    };

    std::string first_egu, second_egu;

    std::unordered_map<std::string, std::string>::iterator pos = egus.find(first_meas);
    if (pos == egus.end()) {

    } else {
        first_egu = std::string(pos->second);
    }

    pos = egus.find(second_meas);

    if (pos == egus.end()) {

    } else {
        second_egu = std::string(pos->second);
    }

    prec->a = (epicsOldString*)first_egu.c_str();
    prec->b = (epicsOldString*)second_egu.c_str();

    return 0;
}
