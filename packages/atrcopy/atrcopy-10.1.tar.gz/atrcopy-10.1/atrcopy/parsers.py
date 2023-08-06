import hashlib

import numpy as np

from .segments import SegmentData, DefaultSegment
from .kboot import KBootImage
from .ataridos import AtariDosDiskImage, BootDiskImage, AtariDosFile, XexContainerSegment, AtariDiskImage
from .spartados import SpartaDosDiskImage
from .cartridge import AtariCartImage, Atari8bitCartImage, Atari5200CartImage, get_known_carts, RomImage, Atari2600CartImage, Atari2600StarpathImage, VectrexCartImage
from .mame import MameZipImage
from .dos33 import Dos33DiskImage, ProdosDiskImage, Dos33BinFile
from .standard_delivery import StandardDeliveryImage
from . import errors
from .magic import guess_detail_for_mime
from . import container
from .dcm import DCMContainer
from .signatures import sha1_signatures

import logging
log = logging.getLogger(__name__)


class SegmentParser:
    menu_name = ""
    image_type = None
    container_segment = DefaultSegment

    def __init__(self, segment_data, strict=False):
        self.image = None
        self.segments = []
        self.strict = strict
        self.segment_data = segment_data
        self.parse()

    def __str__(self):
        lines = []
        lines.append("%s (%s)" % (self.menu_name, self.__class__.__name__))
        if log.isEnabledFor(logging.DEBUG):
            lines.append("segments:")
            for s in self.segments:
                lines.append("  %s" % s)
        return "\n".join(lines)

    def __getstate__(self):
        """Custom jsonpickle state save routine

        This routine culls down the list of attributes that should be
        serialized, and in some cases changes their format slightly so they
        have a better mapping to json objects. For instance, json can't handle
        dicts with integer keys, so dicts are turned into lists of lists.
        Tuples are also turned into lists because tuples don't have a direct
        representation in json, while lists have a compact representation in
        json.
        """
        state = dict()
        for key in ['segments', 'strict']:
            state[key] = getattr(self, key)
        return state

    def __setstate__(self, state):
        """Custom jsonpickle state restore routine

        The use of jsonpickle to recreate objects doesn't go through __init__,
        so there will be missing attributes when restoring old versions of the
        json. Once a version gets out in the wild and additional attributes are
        added to a segment, a default value should be applied here.
        """
        self.__dict__.update(state)

    def parse(self):
        r = self.segment_data
        self.segments.append(self.container_segment(r, 0, name=self.menu_name))
        try:
            log.debug("Trying %s" % self.image_type)
            log.debug(self.image_type.__mro__)
            self.image = self.get_image(r)
            self.check_image()
            self.image.parse_segments()
        except errors.UnsupportedDiskImage:
            raise
        except errors.AtrError as e:
            raise errors.InvalidSegmentParser(e)
        self.segments.extend(self.image.segments)

    def reconstruct_segments(self, new_rawdata):
        self.image = self.get_image(new_rawdata)
        self.segment_data = new_rawdata
        for s in self.segments:
            s.reconstruct_raw(new_rawdata)

    def get_image(self, r):
        log.info(f"checking image type {self.image_type}")
        return self.image_type(r)

    def check_image(self):
        if self.strict:
            try:
                self.image.strict_check()
            except errors.AtrError as e:
                raise errors.InvalidSegmentParser(e)
        else:
            self.image.relaxed_check()


class DefaultSegmentParser(SegmentParser):
    menu_name = "Raw Data"

    def parse(self):
        self.segments = [DefaultSegment(self.segment_data, 0)]


class KBootSegmentParser(SegmentParser):
    menu_name = "KBoot Disk Image"
    image_type = KBootImage


class AtariDosSegmentParser(SegmentParser):
    menu_name = "Atari DOS Disk Image"
    image_type = AtariDosDiskImage


class SpartaDosSegmentParser(SegmentParser):
    menu_name = "Sparta DOS Disk Image"
    image_type = SpartaDosDiskImage


class AtariBootDiskSegmentParser(SegmentParser):
    menu_name = "Atari Boot Disk Image"
    image_type = BootDiskImage


class AtariUnidentifiedSegmentParser(SegmentParser):
    menu_name = "Atari Disk Image"
    image_type = AtariDiskImage


class XexSegmentParser(SegmentParser):
    menu_name = "XEX (Atari 8-bit executable)"
    image_type = AtariDosFile
    container_segment = XexContainerSegment


class AtariCartSegmentParser(SegmentParser):
    menu_name = "temp"
    image_type = AtariCartImage
    cart_type = 0
    cart_info = None

    def get_image(self, r):
        log.info(f"checking cart type {self.cart_type}: {self.image_type}")
        return self.image_type(r, self.cart_type)


class Atari8bitCartParser(AtariCartSegmentParser):
    menu_name = "Atari Home Computer Cartridge"
    image_type = Atari8bitCartImage


class Atari5200CartParser(AtariCartSegmentParser):
    menu_name = "Atari 5200 Cartridge"
    image_type = Atari5200CartImage


class Atari2600CartParser(SegmentParser):
    menu_name = "Atari 2600 Cartridge"
    image_type = Atari2600CartImage


class Atari2600StarpathParser(SegmentParser):
    menu_name = "Atari 2600 Starpath Cassette"
    image_type = Atari2600StarpathImage


class VectrexParser(SegmentParser):
    menu_name = "Vectrex Cartridge"
    image_type = VectrexCartImage


class RomParser(SegmentParser):
    menu_name = "ROM Image"
    image_type = RomImage


class MameZipParser(SegmentParser):
    menu_name = "MAME ROM Zipfile"
    image_type = MameZipImage


class Dos33SegmentParser(SegmentParser):
    menu_name = "DOS 3.3 Disk Image"
    image_type = Dos33DiskImage


class Dos33BinSegmentParser(SegmentParser):
    menu_name = "BIN (Apple ][ executable)"
    image_type = Dos33BinFile


class ProdosSegmentParser(SegmentParser):
    menu_name = "ProDOS Disk Image"
    image_type = ProdosDiskImage


known_containers = [
    container.GZipContainer,
    container.BZipContainer,
    container.LZMAContainer,
    DCMContainer,
]


def guess_container(r, verbose=False):
    for c in known_containers:
        if verbose:
            log.info(f"trying container {c}")
        try:
            found = c(r)
        except errors.InvalidContainer as e:
            continue
        else:
            if verbose:
                log.info(f"found container {c}")
            return found
    log.info(f"image does not appear to be a container.")
    return None


def guess_parser_by_size(r, verbose=False):
    found = None
    mime = None
    size = len(r)
    if size in sha1_signatures:
        sha_hash = hashlib.sha1(r.data).digest()
        log.info(f"{size} in signature database, attempting to match {sha_hash}")
        try:
            match = sha1_signatures[size][sha_hash]
        except KeyError:
            pass
        else:
            mime = match[0]
            log.info(f"found match: {match}")
            parsers = mime_parsers[mime]
            for parser in parsers:
                try:
                    found = parser(r, False)
                    break
                except errors.InvalidSegmentParser as e:
                    if verbose:
                        log.info("parser isn't %s: %s" % (parser.__name__, str(e)))
                    pass
        if found is None:
            log.info(f"no matching signature")
    else:
        log.info(f"{size} not found in signature database; skipping sha1 matching")
    return mime, found

def guess_parser_for_mime(mime, r, verbose=False):
    parsers = mime_parsers[mime]
    found = None
    for parser in parsers:
        try:
            found = parser(r, True)
            break
        except errors.InvalidSegmentParser as e:
            if verbose:
                log.info("parser isn't %s: %s" % (parser.__name__, str(e)))
            pass
    return found


def guess_parser_for_system(mime_base, r):
    for mime in mime_parse_order:
        if mime.startswith(mime_base):
            p = guess_parser_for_mime(mime, r)
            if p is not None:
                mime = guess_detail_for_mime(mime, r, p)
                return mime, p
    return None, None


def iter_parsers(r):
    container = guess_container(r.data)
    if container is not None:
        r = SegmentData(container.unpacked)
    mime, parser = guess_parser_by_size(r)
    if parser is None:
        for mime in mime_parse_order:
            p = guess_parser_for_mime(mime, r)
            if p is not None:
                parser = p
                mime = guess_detail_for_mime(mime, r, p)
                break
    return mime, parser


def parsers_for_filename(name):
    matches = []
    for mime in mime_parse_order:
        parsers = mime_parsers[mime]
        found = None
        for parser in parsers:
            log.debug("parser: %s = %s" % (mime, parser))
    n = name.lower()
    if n.endswith(".atr"):
        matches.append(KBootImage)
    elif n.endswith(".dsk"):
        matches.append(StandardDeliveryImage)
    else:
        try:
            _, name = name.rsplit(".", 1)
        except ValueError:
            pass
        raise errors.InvalidDiskImage("no disk image formats that match '%s'" % name)
    return matches


mime_parsers = {
    "application/vnd.atari8bit.atr": [
        KBootSegmentParser,
        SpartaDosSegmentParser,
        AtariDosSegmentParser,
        AtariBootDiskSegmentParser,
        AtariUnidentifiedSegmentParser,
        ],
    "application/vnd.atari8bit.xex": [
        XexSegmentParser,
        ],
    "application/vnd.atari8bit.cart": [
        Atari8bitCartParser,
        ],
    "application/vnd.atari5200.cart": [
        Atari5200CartParser,
        ],
    "application/vnd.atari2600.cart": [
        Atari2600CartParser,
        ],
    "application/vnd.atari2600.starpath": [
        Atari2600StarpathParser,
        ],
    "application/vnd.vectrex": [
        VectrexParser,
        ],
    "application/vnd.mame_rom": [
        MameZipParser,
        ],
    "application/vnd.rom": [
        RomParser,
        ],
    "application/vnd.apple2.dsk": [
        Dos33SegmentParser,
        ProdosSegmentParser,
        ],
    "application/vnd.apple2.bin": [
        Dos33BinSegmentParser,
        ],
    }

# Note: Atari 2600 scanning not performed here because it will match everything
mime_parse_order = [
    "application/vnd.atari8bit.atr",
    "application/vnd.atari8bit.xex",
    "application/vnd.atari8bit.cart",
    "application/vnd.atari5200.cart",
    "application/vnd.mame_rom",
    "application/vnd.apple2.dsk",
    "application/vnd.apple2.bin",
    "application/vnd.rom",
    ]

# different than the above mime_parse_order, this list is the order in which
# the mime parsers will appear in a UI. Some, like the vectrex and atari2600
# parsers, aren't included in the parse order because they will identify
# many things incorrectly. They are used only when parsing by size and
# signature.
mime_display_order = [
    "application/vnd.atari8bit.atr",
    "application/vnd.atari8bit.xex",
    "application/vnd.atari8bit.cart",
    "application/vnd.atari5200.cart",
    "application/vnd.atari2600.cart",
    "application/vnd.atari2600.starpath",
    "application/vnd.vectrex",
    "application/vnd.mame_rom",
    "application/vnd.apple2.dsk",
    "application/vnd.apple2.bin",
    "application/vnd.rom",
    ]

pretty_mime = {
    "application/vnd.atari8bit.atr": "Atari 8-bit Disk Image",
    "application/vnd.atari8bit.xex": "Atari 8-bit Executable",
    "application/vnd.atari8bit.cart": "Atari 8-bit Cartridge",
    "application/vnd.atari5200.cart": "Atari 5200 Cartridge",
    "application/vnd.atari2600.cart": "Atari 2600 Cartridge",
    "application/vnd.atari2600.starpath": "Atari 2600 Starpath Cassette",
    "application/vnd.vectrex": "GCE Vectrex Cartridge",
    "application/vnd.mame_rom": "MAME",
    "application/vnd.rom": "ROM Image",
    "application/vnd.apple2.dsk": "Apple ][ Disk Image",
    "application/vnd.apple2.bin": "Apple ][ Binary",
}

grouped_carts = get_known_carts()
sizes = sorted(grouped_carts.keys())
for k in sizes:
    for c in grouped_carts[k]:
        t = c[0]
        name = c[1]
        if "5200" in name:
            key = "application/vnd.atari5200.cart"
            kclass = type("Atari5200CartSegmentParser%d" % t, (Atari5200CartParser, AtariCartSegmentParser), {'cart_type': t, 'cart_info': c, 'menu_name': "%s Cartridge" % name})
        else:
            key = "application/vnd.atari8bit.cart"
            kclass = type("Atari8bitCartSegmentParser%d" % t, (Atari8bitCartParser, AtariCartSegmentParser), {'cart_type': t, 'cart_info': c, 'menu_name': "%s Cartridge" % name})
        mime_parsers[key].append(kclass)


known_segment_parsers = [DefaultSegmentParser]
for mime in mime_display_order:
    known_segment_parsers.extend(mime_parsers[mime])


def iter_known_segment_parsers():
    yield "application/octet-stream", "", [DefaultSegmentParser]
    for mime in mime_display_order:
        yield mime, pretty_mime[mime], mime_parsers[mime]
