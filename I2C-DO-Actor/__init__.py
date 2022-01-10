
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from smbus import SMBus


logger = logging.getLogger(__name__)

def get_Address():
        bus = SMBus(1) # 1 indicates /dev/i2c-1
        addresses = []
        for address in range(128):
            try:
                bus.read_byte(address)
                addresses.append(address)
            except:
                pass
        return addresses


@parameters([Property.Select("Address DO", get_Address(), description="The I2C actor address."),Property.Select("Port DO", options=[0,1,2,3,4,5,6,7], description="Port of the Digital-Ouput-Modul to which the actor is connected")])
class CustomActor(CBPiActor):
    @action("Set Power", parameters=[Property.Number(label="Power", configurable=True,description="Power Setting [0-100]")])

    async def setpower(self,Power = 100 ,**kwargs):
        self.power=int(Power)
        if self.power < 0:
            self.power = 0
        if self.power > 100:
            self.power = 100           
        await self.set_power(self.power)  
 
    async def on_start(self):
        self.power = None
        self.adress_DO = int(self.props.get("Adress AO",88))
        self.port_DO = int(self.props.get("Port AO",0))
        self.bus = SMBus(1) # 1 indicates /dev/i2c-1
        self.state = False  
   
    async def on(self, power=0):
      logger.info("ACTOR %s ON" % self.id)
      self.power = int(power)
      o1 = set_bit(o1, self.port_DO)
      try:
           bus.write_byte(self.adress_DO,255-o1)
      except: # exception if write_byte fails
          pass  
      self.state = True

    async def off(self):
      logger.info("ACTOR %s OFF " % self.id)
      bus = SMBus(1) # 1 indicates /dev/i2c-1
      o1 = clear_bit(o1, 6)
      try:
          bus.write_byte(self.adress_DO,255-o1)
      except: # exception if write_byte fails
          pass
      self.state = False
    async def set_power(self, power):
      self.power = power
      pass

    def get_state(self):
      return self.state
  
def setup(cbpi):
   cbpi.plugin.register("I2C-DO-Actor", CustomActor)
   pass
