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
#include <sstream>

#include "unit_finder.h"

static std::string str_from_epics(void* raw_rec)
{
    epicsOldString* rec = reinterpret_cast<epicsOldString*>(raw_rec);
    char buffer[sizeof(epicsOldString)+1];  // +1 for null terminator in the case where epics str is exactly 40 chars (unterminated)
    buffer[sizeof(epicsOldString)] = '\0';
    return std::string(strncpy(buffer, *rec, sizeof(epicsOldString)));
}


long WorkOutUnits(aSubRecord *prec) {
    if (prec->fta != menuFtypeSTRING)
    {
        errlogSevPrintf(errlogMajor, "%s incorrect input argument type A", prec->name);
        return 1;
    }
    std::stringstream first_meas, second_meas;
    std::string s = str_from_epics(prec->a);

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

    if (s.length() == 0)
    { return 0;}

    // if function begins with Z or Y use 1 char for first and 2 for second
    // else if len is 2 then split down the middle 
    // else if len is 3 then use first 2 chars
    // else if len is 4 then use first 2 chars and last 2 chars
    char first_char = s.at(0);
    if (first_char == 'Y' || first_char == 'Z')
    {
        first_meas << first_char;
        second_meas << s.at(1) << s.at(2);
    }
    else {
        switch(s.length()){
            case 2:
                first_meas <<  first_char;
                second_meas <<  s.at(1);
                break;
            case 3:
                first_meas <<  first_char << s.at(1);
                second_meas <<  s.at(2);
                break;
            case 4:
                first_meas << first_char << s.at(1);
                second_meas <<  s.at(2) << s.at(3);
                break;
            default:
                return 1;
        }
    };

    std::string first_egu, second_egu;
    std::unordered_map<std::string, std::string>::iterator pos = egus.find(first_meas.str());
    if (pos == egus.end()) {
        // first egu not found - this is not good
    } else {
        first_egu = std::string(pos->second);
    }

    pos = egus.find(second_meas.str());
    if (pos == egus.end()) {
        // second egu not found - this is not good either
    } else {
        second_egu = std::string(pos->second);
    }

    strncpy(*reinterpret_cast<epicsOldString*>(prec->vala), first_egu.c_str(), std::min(sizeof(epicsOldString), first_egu.size()+1));
    strncpy(*reinterpret_cast<epicsOldString*>(prec->valb), second_egu.c_str(), std::min(sizeof(epicsOldString), second_egu.size()+1));
    return 0;
}
