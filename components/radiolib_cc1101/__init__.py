import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import spi
from esphome import pins
from esphome.const import *
from esphome.cpp_helpers import gpio_pin_expression
from esphome.core import CORE
import os

DEPENDENCIES = ["spi"]

MULTI_CONF = True

radiolib_cc1101_ns = cg.esphome_ns.namespace("radiolib_cc1101")
RadiolibCC1101Component = radiolib_cc1101_ns.class_(
    "RadiolibCC1101Component", cg.Component, spi.SPIDevice
)

CONF_MODULATION = "modulation"
CC1101Modulation = radiolib_cc1101_ns.enum("CC1101Modulation")
CC1101_MODULATIONS = {
    "OOK": CC1101Modulation.OOK_MODULATION,
    "FSK": CC1101Modulation.FSK_MODULATION,
}

CONFIG_SCHEMA = (
    cv.Schema({
        cv.GenerateID(): cv.declare_id(RadiolibCC1101Component),
        cv.Optional(CONF_RX_PIN): pins.internal_gpio_input_pin_schema,
        cv.Optional(CONF_FREQUENCY, default="433.92MHz"): cv.frequency,
        cv.Optional(CONF_MODULATION, default="ook"): cv.enum(CC1101_MODULATIONS, upper=True, space="_"),
        cv.Optional(CONF_FILTER, default="464kHz"): cv.frequency,
        cv.Optional('bitrate',default=5): cv.float_range(0.025,600), # 40k = 25us resolution, 5k=less noisy
        cv.Optional('reg_agcctrl0',default=0xb2): cv.hex_uint8_t,
        cv.Optional('reg_agcctrl1',default=0x00): cv.hex_uint8_t,
        cv.Optional('reg_agcctrl2',default=0xc7): cv.hex_uint8_t,
        })
    .extend(cv.COMPONENT_SCHEMA)
    .extend(spi.spi_device_schema(cs_pin_required=True))
)

async def to_code(config):
    # When using Arduino, RadioLib includes SPI.h (even though we abstract out the SPI functions)
    # so we need RadioLib to be able to find it...
    if CORE.using_arduino:
        # this probably doesn't work with platformio, but platformio seems to 
        # be being deprecated anyway for esphome builds...
        cg.add_library("SPI",None)        

    cg.add_library("RadioLib",None)

    var = cg.new_Pvariable(config[CONF_ID])

    if CONF_RX_PIN in config:
        pin = await gpio_pin_expression(config[CONF_RX_PIN])
        cg.add(var.set_rx_pin(pin))

    cg.add(var.set_frequency(config[CONF_FREQUENCY]))
    cg.add(var.set_modulation(config[CONF_MODULATION]))
    cg.add(var.set_filter(config[CONF_FILTER]))
    cg.add(var.set_bitrate(config['bitrate']))
    cg.add(var.set_reg_agcctrl0(config['reg_agcctrl0']))
    cg.add(var.set_reg_agcctrl1(config['reg_agcctrl1']))
    cg.add(var.set_reg_agcctrl2(config['reg_agcctrl2']))

    await cg.register_component(var, config)
    await spi.register_spi_device(var, config)
