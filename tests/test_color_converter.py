"""Test color converter."""


import sys

from unittest import TestCase

COLOR_CONVERTER = sys.modules["Rainmeter.color.converter"]


class IntToHexTest(TestCase):
    """Testing int to hex conversion and its corner cases."""

    def test_below_lower_boundary(self):
        """Rainmeter only supports from 0 upwards."""
        self.assertRaises(AssertionError, COLOR_CONVERTER.int_to_hex, -1)

    def test_lower_boundary(self):
        """Zero is a corner case and should return 00."""
        hex_value = COLOR_CONVERTER.int_to_hex(0)

        self.assertEqual(hex_value, "00")

    def test_default(self):
        """A random number within the boundary 0, 255 should work."""
        hex_value = COLOR_CONVERTER.int_to_hex(128)

        self.assertEqual(hex_value, "80")

    def test_upper_boundary(self):
        """255 is a corner case and should return FF."""
        hex_value = COLOR_CONVERTER.int_to_hex(255)

        self.assertEqual(hex_value, "FF")

    def test_over_upper_boundary(self):
        """Rainmeter only supports up to 255."""
        self.assertRaises(AssertionError, COLOR_CONVERTER.int_to_hex, 256)

    def test_letter_case(self):
        """We also support lower case if it is requested."""
        hex_value = COLOR_CONVERTER.int_to_hex(255, letter_case=COLOR_CONVERTER.LetterCase.Lower)

        self.assertEqual(hex_value, "ff")


class RGBsToHexesTest(TestCase):
    """Testing RGBs to hexes conversion and its corner cases."""

    def test_default_rgb_conversion(self):
        """3 valid ints should convert to 3 hexes."""
        hexes = COLOR_CONVERTER.rgbs_to_hexes([128, 128, 128])

        self.assertEqual(hexes, ["80", "80", "80"])

    def test_default_rgba_conversion(self):
        """4 valid ints should convert to 4 hexes."""
        hexes = COLOR_CONVERTER.rgbs_to_hexes([128, 128, 128, 128])

        self.assertEqual(hexes, ["80", "80", "80", "80"])

    def test_invalid_rgb_low_len(self):
        """RGB are at least 3 values."""
        self.assertRaises(AssertionError, COLOR_CONVERTER.rgbs_to_hexes, [128, 128])

    def test_invalid_rgb_high_len(self):
        """RGB are at most 4 values."""
        self.assertRaises(AssertionError, COLOR_CONVERTER.rgbs_to_hexes, [128, 128, 128, 128, 128])


class HexesToStringTest(TestCase):
    """This test guerentees that a proper string conversion ."""

    def test_stringing(self):
        """Default case with one spacing."""
        stringed = COLOR_CONVERTER.hexes_to_string(["80", "80", "80"])

        self.assertEqual(stringed, "808080")

    def test_rgba(self):
        """RGBA case."""
        stringed = COLOR_CONVERTER.hexes_to_string(["80", "80", "80", "80"])

        self.assertEqual(stringed, "80808080")


class HexToIntTest(TestCase):
    """Testing hex to int conversion and its corner cases."""

    def test_below_lower_boundary(self):
        """Rainmeter only supports from 0 upwards."""
        self.assertRaises(AssertionError, COLOR_CONVERTER.hex_to_int, "-1")

    def test_lower_boundary(self):
        """00 is a corner case and should return 0."""
        int_value = COLOR_CONVERTER.hex_to_int("00")

        self.assertEqual(int_value, 0)

    def test_default(self):
        """A random number within the boundary 0, 255 should work."""
        int_value = COLOR_CONVERTER.hex_to_int("80")

        self.assertEqual(int_value, 128)

    def test_upper_boundary(self):
        """FF is a corner case and should return 255."""
        int_value = COLOR_CONVERTER.hex_to_int("FF")

        self.assertEqual(int_value, 255)

    def test_over_upper_boundary(self):
        """Rainmeter only supports up to 255."""
        self.assertRaises(AssertionError, COLOR_CONVERTER.hex_to_int, "100")


class HexesToRGBsTest(TestCase):
    """Testing Hexes to RGBs conversion and its corner cases."""

    def test_default_hex_conversion(self):
        """."""
        rgb = COLOR_CONVERTER.hexes_to_rgbs(["80", "80", "80"])

        self.assertEqual(rgb, [128, 128, 128])

    def test_default_hexa_conversion(self):
        """4 valid hexes should convert to rgba."""
        rgba = COLOR_CONVERTER.hexes_to_rgbs(["80", "80", "80", "80"])

        self.assertEqual(rgba, [128, 128, 128, 128])

    def test_invalid_hex_low_len(self):
        """Require at least 3 values."""
        self.assertRaises(AssertionError, COLOR_CONVERTER.hexes_to_rgbs, ["FF", "FF"])

    def test_invalid_hex_high_len(self):
        """Require at most 4 values."""
        self.assertRaises(
            AssertionError,
            COLOR_CONVERTER.hexes_to_rgbs,
            ["FF", "FF", "FF", "FF", "FF"]
        )


class RGBsToStringTest(TestCase):
    """This test guerentees that a proper string conversion ."""

    def test_stringing(self):
        """Default Rainmeter decimal color representation."""
        stringed = COLOR_CONVERTER.rgbs_to_string([128, 128, 128])

        self.assertEqual(stringed, "128,128,128")

    def test_with_spacing(self):
        """For people who like to space things."""
        stringed = COLOR_CONVERTER.rgbs_to_string([128, 128, 128], spacing=1)

        self.assertEqual(stringed, "128, 128, 128")

    def test_with_more_spacing(self):
        """For people who like to use a lot of spacings."""
        stringed = COLOR_CONVERTER.rgbs_to_string([128, 128, 128], spacing=5)

        self.assertEqual(stringed, "128,     128,     128")


class HexAppendAlphaTest(TestCase):
    """This test handles different cases of appended alpha values."""

    def test_lower_case(self):
        """Lower case hex string adds a lower-case full alpha channel."""
        stringed = COLOR_CONVERTER.convert_hex_to_hex_with_alpha("ff8800")

        self.assertEqual(stringed, "ff8800ff")

    def test_upper_case(self):
        """Upper case hex string adds upper-case full alpha channel."""
        stringed = COLOR_CONVERTER.convert_hex_to_hex_with_alpha("FF8800")

        self.assertEqual(stringed, "FF8800FF")

    def test_mixed_case(self):
        """If case is not clear add upper-case full alpha channel."""
        stringed = COLOR_CONVERTER.convert_hex_to_hex_with_alpha("Ff8800")

        self.assertEqual(stringed, "Ff8800FF")

    def test_already_alpha(self):
        """Only add alpha channel if have only RGB."""
        stringed = COLOR_CONVERTER.convert_hex_to_hex_with_alpha("FF8800FF")

        self.assertEqual(stringed, "FF8800FF")


class HexToRGBAStringTest(TestCase):
    """Test behaviour of hex string to rgba string converter."""

    def test_without_alpha(self):
        """
        We always get a RGBA String, but it depends if previously it had an alpha channel or not.

        In case it had no alpha channel then we ignore the alpha channel
        unless we have a value which differs from FF or 255.
        The color picker will default to FF if a non alpha channel color is inputted.
        """
        stringed = COLOR_CONVERTER.convert_hex_str_to_rgba_str("FFFFFFFF", False)

        self.assertEqual(stringed, "255,255,255")

    def test_with_alpha(self):
        """
        If there was already an alpha channel there we have to respect that.

        That way even FF is written back.
        """
        stringed = COLOR_CONVERTER.convert_hex_str_to_rgba_str("FFFFFFFF", True)

        self.assertEqual(stringed, "255,255,255,255")

    def test_without_alpha_but_non_max(self):
        """
        If we had no alpha channel but we get a value back which is different from FF.

        In that case we have to translate that information too
        and force add the alpha channel to the content.
        """
        stringed = COLOR_CONVERTER.convert_hex_str_to_rgba_str("FFFFFF01", False)

        self.assertEqual(stringed, "255,255,255,1")
