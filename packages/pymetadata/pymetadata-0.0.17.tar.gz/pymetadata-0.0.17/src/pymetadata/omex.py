"""
COMBINE Archive helper functions and classes based on libCOMBINE.

Here common operations with COMBINE archives are implemented, like
extracting archives, creating archives from entries or directories,
adding metadata, listing content of archives.

When working with COMBINE archives these wrapper functions should be used.

"""
# FIXME: handle the adding of metadata

import os
import pprint
import shutil
import tempfile
import warnings
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, List, Optional, Tuple

import libcombine

from pymetadata import log


logger = log.get_logger(__name__)


class Creator:
    """Helper class to store the creator information."""

    def __init__(
        self, given_name: str, family_name: str, organization: str, email: str
    ):
        self.given_name = given_name
        self.family_name = family_name
        self.organization = organization
        self.email = email


class Entry:
    """Helper class to store content to create an OmexEntry."""

    def __init__(
        self,
        location: str,
        format: Optional[str] = None,
        format_key: Optional[str] = None,
        master: bool = False,
        description: Optional[str] = None,
        creators: Optional[Iterator[Creator]] = None,
    ):
        """Create entry from information.

        If format and formatKey are provided the format is used.

        :param location: location of the entry
        :param format: full format string
        :param format_key: short formatKey string
        :param master: master attribute
        :param description: description
        :param creators: iterator over Creator objects
        """
        if (format_key is None) and (format is None):
            raise ValueError(
                "Either 'formatKey' or 'format' must be specified for Entry."
            )
        if format is None:
            format = libcombine.KnownFormats.lookupFormat(formatKey=format_key)

        self.format: str = format
        self.location: str = location
        self.master: bool = master
        self.description: Optional[str] = description
        self.creators: Optional[Iterator[Creator]] = creators

    def __str__(self) -> str:
        """Get string of Entry."""
        if self.master:
            return f"<*master* Entry {self.location} | {self.format}>"
        else:
            return f"<Entry {self.location} | {self.format}>"


class Omex:
    """Combine archive class."""

    def __init__(self, omex_path: Path, working_dir: Path):
        """Create combine archive."""
        if not working_dir.exists():
            logger.warning(f"Creating working directory: {working_dir}")
            working_dir.mkdir(parents=True, exist_ok=True)

        self.omex_path: Path = omex_path
        self.working_dir: Path = working_dir

    def __repr__(self) -> str:
        """Get representation string."""
        return f"Omex({self.omex_path}, working_dir={self.working_dir})"

    def __str__(self) -> str:
        """Get contents of archive string."""
        return pprint.pformat(self.list_contents())

    def _omex_init(self) -> libcombine.CombineArchive:
        """Initialize omex from archive.

        Call omex.cleanUp after finishing.
        """
        omex: libcombine.CombineArchive = libcombine.CombineArchive()
        if omex.initializeFromArchive(str(self.omex_path)) is None:
            raise IOError(f"Invalid COMBINE Archive: {self.omex_path}")
        return omex

    @classmethod
    def from_directory(
        cls,
        omex_path: Path,
        directory: Path,
        creators: Optional[Iterator[Creator]] = None,
    ) -> "Omex":
        """Create a COMBINE archive from a given folder.

        The file types are inferred,
        in case of existing manifest or metadata information this should be reused.

        For all SED-ML files in the directory the master attribute is set to True.

        :param directory: Directory to compress
        :param omex_path: Output path for omex directory
        :param creators: List of creators
        :return:
        """

        manifest_path: Path = directory / "manifest.xml"

        if manifest_path.exists():
            warnings.warn(
                f"Manifest file exists in directory, but not used in COMBINE "
                f"archive creation: {manifest_path}"
            )
            # FIXME: reuse existing manifest

        # add the base entry
        entries = [
            Entry(
                location=".",
                format="https://identifiers.org/combine.specifications/omex",
                master=False,
            )
        ]

        # iterate over all locations & guess format
        for root, _dirs, files in os.walk(str(directory)):
            for file in files:
                file_path = os.path.join(root, file)
                location = os.path.relpath(file_path, directory)
                # guess the format
                format = libcombine.KnownFormats.guessFormat(file_path)
                master = False
                if libcombine.KnownFormats.isFormat(formatKey="sed-ml", format=format):
                    master = True

                entries.append(
                    Entry(
                        location=location,
                        format=format,
                        master=master,
                        creators=creators,
                    )
                )

        # create additional metadata if available

        # write all the entries
        print("-" * 80)
        print(omex_path)
        print("-" * 80)
        omex = cls.from_entries(
            omex_path=omex_path, entries=entries, working_dir=directory
        )
        print("-" * 80)

        return omex

    @classmethod
    def from_entries(
        cls, omex_path: Path, entries: Iterable[Entry], working_dir: Path
    ) -> "Omex":
        """Create COMBINE archive from given entries.

        Overwrites existing combine archive at omex_path.

        :param omex_path: Path of archive
        :param entries:
        :param working_dir:
        :return:
        """
        omex = Omex(omex_path=omex_path, working_dir=working_dir)
        return omex._from_entries(entries, add_entries=False)  # type: ignore

    def _from_entries(self, entries: Iterable[Entry], add_entries: bool) -> None:
        """Create archive from given entries.

        :param entries: entries which should be in the archive.
        :param add_entries: boolean flag to add entries or create new archive
        :return:
        """

        if add_entries is False:
            if self.omex_path.exists():
                # delete the old omex file
                logger.warning(f"Combine archive is overwritten: {self.omex_path}")
                os.remove(str(self.omex_path))

        archive = libcombine.CombineArchive()

        if add_entries is True:
            # use existing entries
            if self.omex_path.exists():
                # init archive from existing content
                if archive.initializeFromArchive(self.omex_path) is None:
                    raise IOError(f"Combine Archive is invalid: {self.omex_path}")

        # timestamp
        time_now = libcombine.OmexDescription.getCurrentDateAndTime()

        for entry in entries:
            print(entry)
            location = entry.location
            path = os.path.join(str(self.working_dir), location)
            if not os.path.exists(path):
                raise IOError(f"File does not exist at given location: {path}")

            archive.addFile(path, location, entry.format, entry.master)

            if entry.description or entry.creators:
                omex_description: libcombine.OmexDescription = (
                    libcombine.OmexDescription()
                )
                omex_description.setAbout(location)
                omex_description.setCreated(time_now)

                if entry.description:
                    omex_description.setDescription(entry.description)

                if entry.creators:
                    for c in entry.creators:
                        creator = libcombine.VCard()
                        creator.setFamilyName(c.family_name)
                        creator.setGivenName(c.given_name)
                        creator.setEmail(c.email)
                        creator.setOrganization(c.organization)
                        omex_description.addCreator(creator)

                archive.addMetadata(location, omex_description)

        archive.writeToFile(str(self.omex_path))
        archive.cleanUp()

    def extract(self, output_dir: Path = None, method: str = "zip") -> None:
        """Extract combine archive to working directory.

        The zip method extracts all entries in the zip, the omex method
        only extracts the entries listed in the manifest.
        In some archives not all content is listed in the manifest.

        :param output_dir: output directory
        :param method: method to extract content, either 'zip' or 'omex'
        :return:
        """
        if output_dir is None:
            output_dir = self.working_dir

        if method == "zip":
            zip_ref = zipfile.ZipFile(self.omex_path, "r")
            zip_ref.extractall(output_dir)
            zip_ref.close()

        elif method == "omex":
            archive: libcombine.CombineArchive = self._omex_init()
            for i in range(archive.getNumEntries()):
                entry = archive.getEntry(i)
                location = entry.getLocation()
                filename = os.path.join(output_dir, location)
                archive.extractEntry(location, filename)

            archive.cleanUp()
        else:
            raise ValueError(f"Method is not supported '{method}'")

    def locations_by_format(
        self, format_key: str = None, method: str = "omex"
    ) -> List[Tuple[str, bool]]:
        """Get locations to files with given format in the archive.

        Uses the libcombine KnownFormats for formatKey, e.g., 'sed-ml' or 'sbml'.
        Files which have a master=True have higher priority and are listed first.

        :param omex_path:
        :param format_key:
        :param method:
        :return: List of files with master flags
        """
        if not format_key:
            raise ValueError("Format must be specified.")

        locations: List[Tuple[str, bool]] = []

        if method == "omex":
            archive: libcombine.CombineArchive = self._omex_init()

            for i in range(archive.getNumEntries()):
                entry: libcombine.CaContent = archive.getEntry(i)
                format: str = entry.getFormat()
                master: bool = entry.getMaster()
                if libcombine.KnownFormats.isFormat(format_key, format):
                    loc: str = entry.getLocation()
                    if (master is None) or (master is False):
                        locations.append((loc, False))
                    else:
                        locations.append((loc, True))
            archive.cleanUp()

        elif method == "zip":
            logger.warning("Master flag cannot be resolved, use method 'omex' instead.")
            # extract to tmpfile and guess format
            tmp_dir = tempfile.mkdtemp()

            try:
                self.extract(output_dir=Path(tmp_dir), method="zip")

                # iterate over all locations & guess format
                for root, _dirs, files in os.walk(tmp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        location = os.path.relpath(file_path, tmp_dir)
                        # guess the format
                        format = libcombine.KnownFormats.guessFormat(file_path)
                        if libcombine.KnownFormats.isFormat(
                            formatKey=format_key, format=format
                        ):
                            locations.append((location, False))

            finally:
                shutil.rmtree(tmp_dir)

        else:
            raise ValueError(f"Method is not supported '{method}'")

        return locations

    def list_contents(self, method: str = "omex") -> List["Content"]:
        """Return list of contents of the combine archive.

        :param omexPath:
        :param method: method to extract content, only 'omex' supported
        :return: list of contents
        """
        if method not in ["omex"]:
            raise ValueError("Method is not supported: {method}")

        contents = []
        omex = self._omex_init()

        for i in range(omex.getNumEntries()):
            entry = omex.getEntry(i)
            location = entry.getLocation()
            format = entry.getFormat()
            master = entry.getMaster()
            info = None
            for formatKey in ["sed-ml", "sbml", "sbgn", "cellml"]:
                if libcombine.KnownFormats_isFormat(formatKey, format):
                    info = omex.extractEntryToString(location)

            content = Content(
                location=location,
                format=format,
                master=master,
                info=info,
            )

            contents.append(content)

        omex.cleanUp()

        return contents


@dataclass
class Content:
    """Content entry of OMEX archive."""

    location: str
    format: str
    master: bool
    info: Optional[str] = field(repr=False)
