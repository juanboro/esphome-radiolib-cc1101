import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import spi
from esphome import pins
from esphome.const import *
from esphome.cpp_helpers import gpio_pin_expression

DEPENDENCIES = ["spi"]

radiolib_cc1101_ns = cg.esphome_ns.namespace("radiolib_cc1101")
RadiolibCC1101Component = radiolib_cc1101_ns.class_(
    "RadiolibCC1101Component", cg.Component, spi.SPIDevice
)

CONFIG_SCHEMA = (
    cv.Schema({
        cv.GenerateID(): cv.declare_id(RadiolibCC1101Component),
        cv.Required(CONF_RX_PIN): pins.internal_gpio_input_pin_schema,
        cv.Required(CONF_TX_PIN): pins.internal_gpio_output_pin_schema,
        cv.Optional(CONF_FREQUENCY, default="433.92MHz"): cv.frequency,
        cv.Optional(CONF_FILTER, default="464kHz"): cv.frequency,
        cv.Optional('bitrate',default=40): cv.float_range(0.025,600), # 40k = 25us resolution
        })
    .extend(cv.COMPONENT_SCHEMA)
    .extend(spi.spi_device_schema(cs_pin_required=True))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    pin = await gpio_pin_expression(config[CONF_RX_PIN])
    cg.add(var.set_rx_pin(pin))

    pin = await gpio_pin_expression(config[CONF_TX_PIN])
    cg.add(var.set_tx_pin(pin))

    cg.add(var.set_frequency(config[CONF_FREQUENCY]))
    cg.add(var.set_filter(config[CONF_FILTER]))
    cg.add(var.set_bitrate(config['bitrate']))

    await cg.register_component(var, config)
    await spi.register_spi_device(var, config)
