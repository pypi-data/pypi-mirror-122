import os
from typing import List, Optional

import pystac
from stactools.core.io.xml import XmlElement

from .constants import (OLCI_L1_ASSET_KEYS, OLCI_L2_LAND_ASSET_KEYS,
                        OLCI_L2_WATER_ASSET_KEYS, SAFE_MANIFEST_ASSET_KEY,
                        SENTINEL_OLCI_BANDS, SENTINEL_SLSTR_BANDS,
                        SENTINEL_SRAL_BANDS, SENTINEL_SYNERGY_BANDS,
                        SLSTR_L1_ASSET_KEYS, SYNERGY_SYN_ASSET_KEYS,
                        SYNERGY_V10_VG1_VGP_ASSET_KEYS)


class ManifestError(Exception):
    pass


class MetadataLinks:
    def __init__(
        self,
        granule_href: str,
    ):
        self.granule_href = granule_href
        self.href = os.path.join(granule_href, "xfdumanifest.xml")

        root = XmlElement.from_file(self.href)
        data_object_section = root.find("dataObjectSection")
        if data_object_section is None:
            raise ManifestError(
                f"Manifest at {self.href} does not have a dataObjectSection")

        self._data_object_section = data_object_section
        self.product_metadata_href = os.path.join(granule_href,
                                                  "xfdumanifest.xml")

    def _find_href(self, xpaths: List[str]) -> Optional[str]:
        file_path = None
        for xpath in xpaths:
            file_path = self._data_object_section.find_attr("href", xpath)
            if file_path is not None:
                break

        if file_path is None:
            return None
        else:
            # Remove relative prefix that some paths have
            file_path = file_path.strip("./")
            return os.path.join(self.granule_href, file_path)

    @property
    def thumbnail_href(self) -> Optional[str]:
        preview = os.path.join(self.granule_href, "preview")
        return os.path.join(preview, "quick-look.png")

    def create_manifest_asset(self):
        asset = pystac.Asset(
            href=self.href,
            media_type=pystac.MediaType.XML,
            roles=["metadata"],
        )
        return (SAFE_MANIFEST_ASSET_KEY, asset)

    def create_band_asset(self):
        asset_list = []
        root = XmlElement.from_file(self.product_metadata_href)
        product_type = root.findall(".//sentinel3:productType")[0].text

        if product_type.split("_")[0] == "OL":
            instrument_bands = SENTINEL_OLCI_BANDS
        elif product_type.split("_")[0] == "SL":
            instrument_bands = SENTINEL_SLSTR_BANDS
        elif product_type.split("_")[0] == "SR":
            instrument_bands = SENTINEL_SRAL_BANDS
        elif product_type.split("_")[0] == "SY":
            instrument_bands = SENTINEL_SYNERGY_BANDS

        if instrument_bands == SENTINEL_SRAL_BANDS:
            asset_key_list = ["standardMeasurementData"]
            band_dict_list = []
            for asset_key in asset_key_list:
                for band in instrument_bands:
                    band_dict = {
                        "name":
                        instrument_bands[band].name,
                        "description":
                        instrument_bands[band].description,
                        "central_frequency":
                        instrument_bands[band].center_wavelength,
                        "band_width_in_Hz":
                        instrument_bands[band].full_width_half_max
                    }
                    band_dict_list.append(band_dict)
                asset_location = root.find_attr(
                    "href", f".//dataObject[@ID='{asset_key}']//fileLocation")
                asset_href = os.path.join(self.granule_href, asset_location)
                media_type = root.find_attr(
                    "mimeType",
                    f".//dataObject[@ID='{asset_key}']//byteStream")
                asset_description = root.find_attr(
                    "textInfo",
                    f".//dataObject[@ID='{asset_key}']//fileLocation")
                asset_obj = pystac.Asset(
                    href=asset_href,
                    media_type=media_type,
                    description=asset_description,
                    roles=["data"],
                    extra_fields={"eo:bands": band_dict_list})
                asset_list.append(asset_obj)
        elif instrument_bands == SENTINEL_SYNERGY_BANDS:
            if "_AOD_" in product_type:
                band_key_list = list(SENTINEL_SYNERGY_BANDS.keys())[26:32]
                asset_key_list = ["NTC_AOD_Data"]
                band_dict_list = []
                for asset_key in asset_key_list:
                    for band in band_key_list:
                        band_dict = {
                            "name":
                            instrument_bands[band].name,
                            "description":
                            instrument_bands[band].description,
                            "center_wavelength":
                            instrument_bands[band].center_wavelength,
                            "band_width":
                            instrument_bands[band].full_width_half_max
                        }
                        band_dict_list.append(band_dict)
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location)
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = "Global aerosol parameters"
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": band_dict_list})
                    asset_list.append(asset_obj)
            elif "_SYN_" in product_type:
                asset_key_list = SYNERGY_SYN_ASSET_KEYS
                band_key_list = list(SENTINEL_SYNERGY_BANDS.keys())[:26]
                for asset_key, band in zip(asset_key_list, band_key_list):
                    band_dict = {
                        "name": instrument_bands[band].name,
                        "description": instrument_bands[band].description,
                        "center_wavelength":
                        instrument_bands[band].center_wavelength,
                        "band_width":
                        instrument_bands[band].full_width_half_max
                    }
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = root.find_attr(
                        "textInfo",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": [band_dict]})
                    asset_list.append(asset_obj)
            else:
                asset_key_list = SYNERGY_V10_VG1_VGP_ASSET_KEYS
                band_key_list = list(SENTINEL_SYNERGY_BANDS.keys())[-4:]
                for asset_key, band in zip(asset_key_list, band_key_list):
                    band_dict = {
                        "name": instrument_bands[band].name,
                        "description": instrument_bands[band].description,
                        "center_wavelength":
                        instrument_bands[band].center_wavelength,
                        "band_width":
                        instrument_bands[band].full_width_half_max
                    }
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    if "_VGP_" in product_type:
                        asset_href = os.path.join(self.granule_href,
                                                  asset_location)
                    else:
                        asset_href = os.path.join(self.granule_href,
                                                  asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = root.find_attr(
                        "textInfo",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": [band_dict]})
                    asset_list.append(asset_obj)
        elif instrument_bands == SENTINEL_OLCI_BANDS:
            if "OL_1_" in product_type:
                asset_key_list = OLCI_L1_ASSET_KEYS
                for asset_key, band in zip(asset_key_list, instrument_bands):
                    band_dict = {
                        "name": instrument_bands[band].name,
                        "description": instrument_bands[band].description,
                        "center_wavelength":
                        instrument_bands[band].center_wavelength,
                        "band_width":
                        instrument_bands[band].full_width_half_max
                    }
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = root.find_attr(
                        "textInfo",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": [band_dict]})
                    asset_list.append(asset_obj)
            elif any(_str in product_type for _str in ["_LFR_", "_LRR_"]):
                asset_key_list = OLCI_L2_LAND_ASSET_KEYS
                for asset_key in asset_key_list:
                    if asset_key == "ogviData":
                        band_key_list = ["Oa03", "Oa10", "Oa17"]
                    elif asset_key == "otciData":
                        band_key_list = ["Oa10", "Oa11", "Oa12"]
                    elif asset_key == "iwvData":
                        band_key_list = ["Oa18", "Oa19"]
                    band_dict_list = []
                    for band in band_key_list:
                        band_dict = {
                            "name":
                            instrument_bands[band].name,
                            "description":
                            instrument_bands[band].description,
                            "center_wavelength":
                            instrument_bands[band].center_wavelength,
                            "band_width":
                            instrument_bands[band].full_width_half_max
                        }
                        band_dict_list.append(band_dict)
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = root.find_attr(
                        "textInfo",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": band_dict_list})
                    asset_list.append(asset_obj)
            elif "_WFR_" in product_type:
                asset_key_list = OLCI_L2_WATER_ASSET_KEYS
                for asset_key in asset_key_list:
                    if (asset_key == "chlNnData" or asset_key == "tsmNnData"):
                        band_key_list = [
                            "Oa01", "Oa02", "Oa03", "Oa04", "Oa05", "Oa06",
                            "Oa07", "Oa08", "Oa09", "Oa10", "Oa11", "Oa12",
                            "Oa16", "Oa17", "Oa18", "Oa21"
                        ]
                    elif asset_key == "chlOc4meData":
                        band_key_list = ["Oa03", "Oa04", "Oa05", "Oa06"]
                    elif asset_key == "iopNnData":
                        band_key_list = [
                            "Oa01",
                            "Oa12",
                            "Oa16",
                            "Oa17",
                            "Oa21",
                        ]
                    elif asset_key == "iwvData":
                        band_key_list = [
                            "Oa18",
                            "Oa19",
                        ]
                    elif asset_key == "parData":
                        pass
                    elif asset_key == "trspData":
                        band_key_list = ["Oa04", "Oa06"]
                    elif asset_key == "wAerData":
                        band_key_list = ["Oa05", "Oa06", "Oa17"]
                    else:
                        band_key_list = [asset_key[:4]]
                    if not band_key_list:
                        band_dict_list = [{
                            "description":
                            "Spectral range 400-700 nm"
                        }]
                    else:
                        band_dict_list = []
                        for band in band_key_list:
                            band_dict = {
                                "name":
                                instrument_bands[band].name,
                                "description":
                                instrument_bands[band].description,
                                "center_wavelength":
                                instrument_bands[band].center_wavelength,
                                "band_width":
                                instrument_bands[band].full_width_half_max
                            }
                            band_dict_list.append(band_dict)
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = root.find_attr(
                        "textInfo",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    if asset_key != "parData":
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={"eo:bands": band_dict_list})
                        asset_list.append(asset_obj)
                    else:
                        asset_obj = pystac.Asset(href=asset_href,
                                                 media_type=media_type,
                                                 description=asset_description,
                                                 roles=["data"])
                        asset_list.append(asset_obj)
        elif instrument_bands == SENTINEL_SLSTR_BANDS:
            if "SL_1_" in product_type:
                asset_key_list = SLSTR_L1_ASSET_KEYS
                for asset_key, band in zip(asset_key_list, instrument_bands):
                    band_dict = {
                        "name": instrument_bands[band].name,
                        "description": instrument_bands[band].description,
                        "center_wavelength":
                        instrument_bands[band].center_wavelength,
                        "band_width":
                        instrument_bands[band].full_width_half_max
                    }
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = root.find_attr(
                        "textInfo",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": [band_dict]})
                    asset_list.append(asset_obj)
            elif "_FRP_" in product_type:
                asset_key_list = ["FRP_IN_Data"]
                band_key_list = ["S05", "S06", "S07", "S10"]
                band_dict_list = []
                for asset_key in asset_key_list:
                    for band in band_key_list:
                        band_dict = {
                            "name":
                            instrument_bands[band].name,
                            "description":
                            instrument_bands[band].description,
                            "center_wavelength":
                            instrument_bands[band].center_wavelength,
                            "band_width":
                            instrument_bands[band].full_width_half_max
                        }
                        band_dict_list.append(band_dict)
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = "Fire Radiative Power (FRP) dataset"
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": band_dict_list})
                    asset_list.append(asset_obj)
            elif "_LST_" in product_type:
                asset_key_list = ["LST_IN_Data"]
                band_key_list = ["S08", "S09"]
                band_dict_list = []
                for asset_key in asset_key_list:
                    for band in band_key_list:
                        band_dict = {
                            "name":
                            instrument_bands[band].name,
                            "description":
                            instrument_bands[band].description,
                            "center_wavelength":
                            instrument_bands[band].center_wavelength,
                            "band_width":
                            instrument_bands[band].full_width_half_max
                        }
                        band_dict_list.append(band_dict)
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = "Land Surface Temperature (LST) values"
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": band_dict_list})
                    asset_list.append(asset_obj)
            elif "_WST_" in product_type:
                asset_key_list = ["L2P_Data"]
                band_key_list = ["S07", "S08", "S09"]
                band_dict_list = []
                for asset_key in asset_key_list:
                    for band in band_key_list:
                        band_dict = {
                            "name":
                            instrument_bands[band].name,
                            "description":
                            instrument_bands[band].description,
                            "center_wavelength":
                            instrument_bands[band].center_wavelength,
                            "band_width":
                            instrument_bands[band].full_width_half_max
                        }
                        band_dict_list.append(band_dict)
                    asset_location = root.find_attr(
                        "href",
                        f".//dataObject[@ID='{asset_key}']//fileLocation")
                    asset_href = os.path.join(self.granule_href,
                                              asset_location.split("/")[1])
                    media_type = root.find_attr(
                        "mimeType",
                        f".//dataObject[@ID='{asset_key}']//byteStream")
                    asset_description = (
                        "Data respects the Group for High Resolution "
                        "Sea Surface Temperature (GHRSST) L2P specification")
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={"eo:bands": band_dict_list})
                    asset_list.append(asset_obj)
        return (asset_key_list, asset_list)
