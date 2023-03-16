TOP=../..
include $(TOP)/configure/CONFIG

LIBRARY_IOC = kse4980

kse4980_LIBS += $(EPICS_BASE_IOC_LIBS)
kse4980_LIBS += asyn asubFunctions utilities 
kse4980_SRCS += unitfinder.cpp unit_finder.c  


include $(TOP)/configure/RULES
