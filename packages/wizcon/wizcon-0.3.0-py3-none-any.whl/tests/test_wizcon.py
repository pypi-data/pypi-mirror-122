#!/usr/bin/env python3

import sys
import argparse
import unittest
from unittest import IsolatedAsyncioTestCase
from wizcon import wizcon
import pywizlight.scenes

IP = '192.168.0.101'

class TestTurnBulbOn(IsolatedAsyncioTestCase):
    def setUp(self):
        self.wizcon = wizcon.Wizcon(IP)

    async def test_turn_bulb_on(self):
        await self.wizcon.turn_bulb_on()
        state = await self.wizcon.light.updateState()
        response = state.get_state()
        self.assertEqual(response, True)

    def tearDown(self):
        del self.wizcon

class TestTurnBulbOff(IsolatedAsyncioTestCase):
    def setUp(self):
        self.wizcon = wizcon.Wizcon(IP)

    async def test_turn_bulb_off(self):
        await self.wizcon.turn_bulb_off()
        state = await self.wizcon.light.updateState()
        response = state.get_state()
        self.assertEqual(response, False)

    def tearDown(self):
        del self.wizcon

class TestSwitchBulb(IsolatedAsyncioTestCase):
    def setUp(self):
        self.wizcon = wizcon.Wizcon(IP)

    async def test_switch_bulb(self):
        state = await self.wizcon.light.updateState()
        initial_bulb_state = state.get_state()

        await self.wizcon.switch_bulb()
        state = await self.wizcon.light.updateState()
        response = state.get_state()

        if initial_bulb_state is True:
            self.assertFalse(response)
        elif initial_bulb_state is False:
            self.assertTrue(response)
        #else:
        #    error

    def tearDown(self):
        del self.wizcon

class TestSetSceneId(IsolatedAsyncioTestCase):
    def setUp(self):
        self.wizcon = wizcon.Wizcon(IP)
        self.scene_id = 23

    async def test_set_scene_id(self):
        await self.wizcon.set_scene_id(self.scene_id)
        state = await self.wizcon.light.updateState()
        scene_name = state.get_scene()
        scene_id = self.wizcon.light.get_id_from_scene_name(scene_name)
        self.assertEqual(scene_id, self.scene_id)

    def tearDown(self):
        del self.wizcon
        del self.scene_id

class TestSetSceneIdInvalid(IsolatedAsyncioTestCase):
    def setUp(self):
        self.wizcon = wizcon.Wizcon(IP)
        self.scene_id = 0

    async def test_set_scene_id_invalid(self):
        with self.assertRaises(IndexError):
            await self.wizcon.set_scene_id(self.scene_id)

        self.scene_id = 33

        with self.assertRaises(IndexError):
            await self.wizcon.set_scene_id(self.scene_id)

    def tearDown(self):
        del self.wizcon
        del self.scene_id

class TestSetSceneIdAll(IsolatedAsyncioTestCase):
    def setUp(self):
        self.wizcon = wizcon.Wizcon(IP)

    async def test_set_scene_id_all(self):
        for scene_id in pywizlight.scenes.SCENES.keys():
            #if scene_id == 1000:      # Skip scene 1000 Rhythm which fails test
            #    continue

            await self.wizcon.set_scene_id(scene_id)
            state = await self.wizcon.light.updateState()
            scene_name = state.get_scene()
            self.assertEqual(self.wizcon.light.get_id_from_scene_name(scene_name), scene_id)

    def tearDown(self):
        del self.wizcon

class TestSetBrightness(IsolatedAsyncioTestCase):
    def setUp(self):
        self.brightness = 0
        self.wizcon = wizcon.Wizcon(IP)

    async def test_set_brightness(self):
        await self.wizcon.set_brightness(self.brightness)
        state = await self.wizcon.light.updateState()
        brightness_value = state.get_brightness()
        # Valid brightness values are 0-255, but lamp miniumum brightness level is 10% which is 26 hex
        self.assertEqual(brightness_value, 26)

        self.brightness = 26

        await self.wizcon.set_brightness(self.brightness)
        state = await self.wizcon.light.updateState()
        brightness_value = state.get_brightness()
        self.assertEqual(brightness_value, self.brightness)

        self.brightness = 128

        await self.wizcon.set_brightness(self.brightness)
        state = await self.wizcon.light.updateState()
        brightness_value = state.get_brightness()
        self.assertEqual(brightness_value, self.brightness)

        self.brightness = 255

        await self.wizcon.set_brightness(self.brightness)
        state = await self.wizcon.light.updateState()
        brightness_value = state.get_brightness()
        self.assertEqual(brightness_value, self.brightness)

    def tearDown(self):
        del self.brightness
        del self.wizcon

class TestWizconScene(IsolatedAsyncioTestCase):
    def setUp(self):
        self.args = wizcon.parse_args([IP, 'on', '--scene_id=1'])
        self.wizcon = wizcon.Wizcon(IP)

    async def test_wizcon_scene(self):
        await self.wizcon.run(self.args)

        state = await self.wizcon.light.updateState()
        scene_name = state.get_scene()
        self.assertEqual(self.wizcon.light.get_id_from_scene_name(scene_name), self.args.scene_id)

    def tearDown(self):
        del self.args
        del self.wizcon

class TestWizconBrightness(IsolatedAsyncioTestCase):
    def setUp(self):
        self.args = wizcon.parse_args([IP, 'on', '--brightness=28'])
        self.wizcon = wizcon.Wizcon(IP)

    async def test_wizcon_brightness(self):
        await self.wizcon.run(self.args)

        state = await self.wizcon.light.updateState()
        brightness_value = state.get_brightness()
        self.assertEqual(brightness_value, self.args.brightness)

    def tearDown(self):
        del self.args
        del self.wizcon

class TestWizconOnNoOptions(IsolatedAsyncioTestCase):
    def setUp(self):
        self.args = wizcon.parse_args([IP, 'on'])
        self.wizcon = wizcon.Wizcon(IP)

    async def test_wizcon_on_no_options(self):
        await self.wizcon.turn_bulb_off()
        await self.wizcon.run(self.args)

        state = await self.wizcon.light.updateState()
        response = state.get_state()
        self.assertEqual(response, True)

    def tearDown(self):
        del self.args
        del self.wizcon

class TestWizconRGB(IsolatedAsyncioTestCase):
    def setUp(self):
        self.args = wizcon.parse_args([IP, 'on', '-rgb', '0', '128', '255'])
        self.wizcon = wizcon.Wizcon(IP)

    async def test_wizcon_rgb(self):
        await self.wizcon.run(self.args)

        state = await self.wizcon.light.updateState()
        rgb = state.get_rgb()
        self.assertEqual(rgb, tuple(self.args.rgb))

    def tearDown(self):
        del self.args
        del self.wizcon

#class TestWizconSceneAndBrightness(IsolatedAsyncioTestCase):
#class TestTurnBulbOnColor(IsolatedAsyncioTestCase):
#class TestTurnBulbOnBrightnessAndColor(IsolatedAsyncioTestCase):

if __name__ == '__main__':
    unittest.main()
