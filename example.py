#!/usr/bin/python3

import SoapySDR        # main package
from SoapySDR import * # constants
import numpy           # buffers
import sys             # exit on error
import pprint          # pretty printer

#mydriver    = "remote"     # Ref: "SoapySDRUtil --find"
mydriver    = "rtlsdr"      # Ref: "SoapySDRUtil --find"
mydirection = SOAPY_SDR_RX  # Interested in receiver info
mychannel   = 0             # Interested in first rx channel

pp = pprint.PrettyPrinter()

print('\nDevices:')
results = SoapySDR.Device.enumerate()
for result in results: 
    pp.pprint(dict(result))

print('\nInstantiate a device using driver "%s"...' % mydriver)
try:
    sdr = SoapySDR.Device(dict(driver=mydriver))
except Exception as e:
    print('Cannot instantiate device: error "%s"' % e)
    sys.exit()
else:
    print("Device instantiated...")

print('\nAntennas:')
results = sdr.listAntennas(mydirection, mychannel)
for result in results: pp.pprint(result)

print('\nGains:')
results = sdr.listGains(mydirection, mychannel)
for result in results: pp.pprint(result)

print('\nFrequency Ranges:')
results = sdr.getFrequencyRange(mydirection, mychannel)
for result in results: 
    print("%12.1f, %12.1f" % (result.minimum(), result.maximum()))

myfrequency = results[0].minimum()
myfrequency += (results[0].maximum() - results[0].minimum()) / 2.0

print('\nSampleRates:')
results = sdr.listSampleRates(mydirection, mychannel)
results = sorted(results)
for result in results: pp.pprint(result)

mysamplerate = results[-1]

print('\nSet sample rate: %.1f' % mysamplerate)
sdr.setSampleRate(mydirection, mychannel, mysamplerate)
print('Get sample rate: %.1f' % sdr.getSampleRate(mydirection, mychannel))

print('\nSet frequency: %.1f' % myfrequency)
sdr.setFrequency(mydirection, mychannel, myfrequency)
print('Get frequency: %.1f' % sdr.getFrequency(mydirection, mychannel))

print('\nSetup Stream:')
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
print('\nActivate Stream:')
sdr.activateStream(rxStream) #start streaming
print('\nCreate Buffers:')
buff = numpy.array([0]*1024, numpy.complex64)

print('\nReceive Samples:')
for i in range(25):
    sr = sdr.readStream(rxStream, [buff], len(buff))
    print('t: %10.6f flags: 0x%02x n: %4d buff0: %s' % \
          ((sr.timeNs + 0.0)/1e9,sr.flags,sr.ret,str(buff[0])))

sdr.deactivateStream(rxStream) #stop streaming
sdr.closeStream(rxStream)
