# Kronos

## Overview
Attention!

THIS NAPP IS STILL EXPERIMENTAL AND IT'S EVENTS, METHODS AND STRUCTURES MAY CHANGE A LOT ON THE NEXT FEW DAYS/WEEKS, USE IT AT YOUR OWN DISCERNEMENT

This NApp is responsible to store data relating to time instances, and this data can be used as supply for other NApps evaluation.

This NApp intends to be time series database agnostic. Therefore, if you want to use any temporal database as backend (InfluxDB, TimeScaleDB, OpenTSDB, Graphite, or even a CSVBackend), check the methods section and generate them for your backend.

## Installing

All of the Kytos Network Applications are located in the NApps online repository. To install this NApp, run:

```
	$ kytos napps install kytos/kronos
``` 
## Configuring

If you want to configure your Napp, please take a look on settings.py file. In this file you will see a few options to configure appropriately your Napp. 

This configuring options change according to the backend you are using. Example, if you are using a CSVBackend (which is the most simple backend), it does not have options like PORT, PASS, HOST and DBNAME. However, in a more robust backend, using InfluxDB backend as example, you have this options to set.

## Methods

### Get

### Save

### Delete
