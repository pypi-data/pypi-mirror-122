from __future__ import annotations

import collections
import enum  # for type hints
import os
import struct
from types import MethodType, ModuleType
from typing import Dict, List

from . import lumps


# NOTE: LumpHeaders must have these attrs, but how they are read / order will vary
LumpHeader = collections.namedtuple("LumpHeader", ["offset", "length", "version", "fourCC"])
ExternalLumpHeader = collections.namedtuple("ExternalLumpHeader", ["offset", "length", "version", "fourCC",
                                                                   "filename", "filesize"])
# NOTE: if fourCC != 0: lump is compressed  (fourCC value == uncompressed size)


class Bsp:
    """Bsp base class"""
    bsp_version: int = 0  # .bsp format version
    associated_files: List[str]  # files in the folder of loaded file with similar names
    branch: ModuleType  # soft copy of "branch script"
    bsp_file_size: int = 0  # size of .bsp in bytes
    file_magic: bytes = b"XBSP"
    filename: str
    folder: str
    headers: Dict[str, LumpHeader]
    # ^ {"LUMP_NAME": LumpHeader}
    loading_errors: Dict[str, Exception]
    # ^ {"LUMP_NAME": Exception encountered}

    def __init__(self, branch: ModuleType, filename: str = "untitled.bsp", autoload: bool = True):
        if not filename.endswith(".bsp"):
            raise RuntimeError("Not a .bsp")
        filename = os.path.realpath(filename)
        self.folder, self.filename = os.path.split(filename)
        self.set_branch(branch)
        self.headers = dict()
        if autoload:
            if os.path.exists(filename):
                self._preload()
            else:
                print(f"{filename} not found, creating a new .bsp")
                self.headers = {L.name: LumpHeader(0, 0, 0, 0) for L in self.branch.LUMP}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()

    def __repr__(self):
        version = f"({self.file_magic.decode('ascii', 'ignore')} version {self.bsp_version})"
        game = self.branch.__name__[len(self.branch.__package__) + 1:]
        return f"<{self.__class__.__name__} '{self.filename}' {game} {version} at 0x{id(self):016X}>"

    def _read_header(self, LUMP: enum.Enum) -> LumpHeader:
        """Reads bytes of lump"""
        self.file.seek(self.branch.lump_header_address[LUMP])
        offset, length, version, fourCC = struct.unpack("4I", self.file.read(16))
        # TODO: use a read & write function / struct.iter_unpack
        # -- this could potentially allow for simplified subclasses
        # -- e.g. LumpHeader(*struct.unpack("4I", self.file.read(16)))  ->  self.LumpHeader(self.file)
        header = LumpHeader(offset, length, version, fourCC)
        return header

    def _preload(self):
        """Loads filename using the format outlined in this .bsp's branch defintion script"""
        local_files = os.listdir(self.folder)
        def is_related(f): return f.startswith(os.path.splitext(self.filename)[0])
        self.associated_files = [f for f in local_files if is_related(f)]
        # open .bsp
        self.file = open(os.path.join(self.folder, self.filename), "rb")
        file_magic = self.file.read(4)
        if file_magic != self.file_magic:
            raise RuntimeError(f"{self.file} is not a valid .bsp!")
        self.bsp_version = int.from_bytes(self.file.read(4), "little")
        self.file.seek(0, 2)  # move cursor to end of file
        self.bsp_file_size = self.file.tell()

        self.headers = dict()
        self.loading_errors: Dict[str, Exception] = dict()
        for LUMP_enum in self.branch.LUMP:
            # CHECK: is lump external? (are associated_files overriding)
            lump_header = self._read_header(LUMP_enum)
            LUMP_NAME = LUMP_enum.name
            self.headers[LUMP_NAME] = lump_header
            if lump_header.length == 0:
                continue
            try:
                if LUMP_NAME == "GAME_LUMP":
                    GameLumpClasses = getattr(self.branch, "GAME_LUMP_CLASSES", dict())
                    BspLump = lumps.GameLump(self.file, lump_header, GameLumpClasses)
                elif LUMP_NAME in self.branch.LUMP_CLASSES:
                    LumpClass = self.branch.LUMP_CLASSES[LUMP_NAME][lump_header.version]
                    BspLump = lumps.create_BspLump(self.file, lump_header, LumpClass)
                elif LUMP_NAME in self.branch.SPECIAL_LUMP_CLASSES:
                    SpecialLumpClass = self.branch.SPECIAL_LUMP_CLASSES[LUMP_NAME][lump_header.version]
                    d_file, d_header = lumps.decompressed(self.file, lump_header)
                    d_file.seek(d_header.offset)
                    lump_data = d_file.read(d_header.length)
                    BspLump = SpecialLumpClass(lump_data)
                elif LUMP_NAME in self.branch.BASIC_LUMP_CLASSES:
                    LumpClass = self.branch.BASIC_LUMP_CLASSES[LUMP_NAME][lump_header.version]
                    BspLump = lumps.create_BasicBspLump(self.file, lump_header, LumpClass)
                else:
                    BspLump = lumps.create_RawBspLump(self.file, lump_header)
            except KeyError:  # lump VERSION not supported
                self.loading_errors[LUMP_NAME] = KeyError(f"{LUMP_NAME} v{lump_header.version} is not supported")
                BspLump = lumps.create_RawBspLump(self.file, lump_header)
            except Exception as exc:
                self.loading_errors[LUMP_NAME] = exc
                BspLump = lumps.create_RawBspLump(self.file, lump_header)
            setattr(self, LUMP_NAME, BspLump)

    def save_as(self, filename: str):
        """Expects outfile to be a file with write bytes capability"""
        raise NotImplementedError()
        # os.makedirs(os.path.dirname(os.path.realpath(filename)), exist_ok=True)
        # outfile = open(filename, "wb")
        # # try to preserve the original order of lumps
        # outfile.write(self.file_magic)
        # outfile.write(self.version.to_bytes(4, "little"))  # .bsp format version
        # for LUMP in self.branch.LUMP:
        #     pass  # calculate and write each header
        #     # adapting each header to bytes could be hard
        # # write the contents of each lump
        # outfile.write(b"0001") # map revision
        # # write contents of lumps

    def save(self):
        self.save_as(os.path.join(self.folder, self.filename))

    def set_branch(self, branch: ModuleType):
        """Calling .set_branch(...) on a loaded .bsp will not convert it!"""
        # branch is a "branch script" that has been imported into python
        # if writing your own "branch script", see branches/README.md for a guide
        self.branch = branch
        # attach methods
        for method in getattr(branch, "methods", list()):
            method = MethodType(method, self)
            setattr(self, method.__name__, method)
        # NOTE: does not remove methods from former branch
        # could we also attach static methods?

    def lump_as_bytes(self, lump_name: str) -> bytes:
        # NOTE: if a lump failed to read correctly, converting to bytes will fail
        # -- this is because LumpClasses are expected
        # -- even though the bytes are saved directly to a RawBspLump... FIXME
        if not hasattr(self, lump_name):
            return b""  # lump is empty / deleted
        lump_entries = getattr(self, lump_name)
        lump_version = self.headers[lump_name].version
        # NOTE: IBSP & GoldSrcBsp don't have lump versions
        if lump_name in self.branch.BASIC_LUMP_CLASSES:
            _format = self.branch.BASIC_LUMP_CLASSES[lump_name][lump_version]._format
            raw_lump = struct.pack(f"{len(lump_entries)}{_format}", *lump_entries)
        elif lump_name in self.branch.LUMP_CLASSES:
            _format = self.branch.LUMP_CLASSES[lump_name][lump_version]._format
            raw_lump = b"".join([struct.pack(_format, *x.flat()) for x in lump_entries])
        elif lump_name in self.branch.SPECIAL_LUMP_CLASSES:
            raw_lump = lump_entries.as_bytes()
        elif lump_name == "GAME_LUMP":
            raw_lump = lump_entries.as_bytes()
        else:  # assume lump_entries is RawBspLump
            raw_lump = bytes(lump_entries)
        return raw_lump
