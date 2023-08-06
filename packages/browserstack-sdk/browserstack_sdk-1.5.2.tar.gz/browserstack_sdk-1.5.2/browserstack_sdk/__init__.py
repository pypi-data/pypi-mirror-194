# coding: UTF-8
import sys
bstack1ll1_opy_ = sys.version_info [0] == 2
bstack1_opy_ = 2048
bstack11_opy_ = 7
def bstack1l_opy_ (bstack1l1l_opy_):
    global bstackl_opy_
    stringNr = ord (bstack1l1l_opy_ [-1])
    bstack1l1_opy_ = bstack1l1l_opy_ [:-1]
    bstack111_opy_ = stringNr % len (bstack1l1_opy_)
    bstack1ll_opy_ = bstack1l1_opy_ [:bstack111_opy_] + bstack1l1_opy_ [bstack111_opy_:]
    if bstack1ll1_opy_:
        bstack11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1_opy_ - (bstack1lll_opy_ + stringNr) % bstack11_opy_) for bstack1lll_opy_, char in enumerate (bstack1ll_opy_)])
    else:
        bstack11l_opy_ = str () .join ([chr (ord (char) - bstack1_opy_ - (bstack1lll_opy_ + stringNr) % bstack11_opy_) for bstack1lll_opy_, char in enumerate (bstack1ll_opy_)])
    return eval (bstack11l_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack11l111_opy_ = {
	bstack1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧࠁ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡴࠪࠂ"),
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪࠃ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡬ࡧࡼࠫࠄ"),
  bstack1l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬࠅ"): bstack1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࠆ"),
  bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫࠇ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡠࡹ࠶ࡧࠬࠈ"),
  bstack1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࠉ"): bstack1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࠨࠊ"),
  bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫࠋ"): bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࠨࠌ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࠍ"): bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩࠎ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࠏ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪࠫࠐ"),
  bstack1l_opy_ (u"ࠧࡤࡱࡱࡷࡴࡲࡥࡍࡱࡪࡷࠬࠑ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡷࡴࡲࡥࠨࠒ"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠓ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࠧࠔ"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠕ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨࠖ"),
  bstack1l_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬࠗ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡶࡪࡦࡨࡳࠬ࠘"),
  bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧ࠙"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠚ"),
  bstack1l_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠛ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪࠜ"),
  bstack1l_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠝ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪࠞ"),
  bstack1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠟ"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩࠠ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࠡ"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࠢ"),
  bstack1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠣ"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡅࡲࡱࡲࡧ࡮ࡥࡵࠪࠤ"),
  bstack1l_opy_ (u"࠭ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠥ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡩࡥ࡮ࡨࡘ࡮ࡳࡥࡰࡷࡷࠫࠦ"),
  bstack1l_opy_ (u"ࠨ࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠧ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡈࡡࡴ࡫ࡦࡅࡺࡺࡨࠨࠨ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡴࡤࡌࡧࡼࡷࠬࠩ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡷࡪࡴࡤࡌࡧࡼࡷࠬࠪ"),
  bstack1l_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠫ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧࠬ"),
  bstack1l_opy_ (u"ࠧࡩࡱࡶࡸࡸ࠭࠭"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡩࡱࡶࡸࡸ࠭࠮"),
  bstack1l_opy_ (u"ࠩࡥࡪࡨࡧࡣࡩࡧࠪ࠯"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡪࡨࡧࡣࡩࡧࠪ࠰"),
  bstack1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠱"): bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬ࠲"),
  bstack1l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠳"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡪࡵࡤࡦࡱ࡫ࡃࡰࡴࡶࡖࡪࡹࡴࡳ࡫ࡦࡸ࡮ࡵ࡮ࡴࠩ࠴"),
  bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ࠵"): bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ࠶"),
  bstack1l_opy_ (u"ࠪࡶࡪࡧ࡬ࡎࡱࡥ࡭ࡱ࡫ࠧ࠷"): bstack1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡡࡰࡳࡧ࡯࡬ࡦࠩ࠸"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ࠹"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱ࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࠺"),
  bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠻"): bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡷࡶࡸࡴࡳࡎࡦࡶࡺࡳࡷࡱࠧ࠼"),
  bstack1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠽"): bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡱࡩࡹࡽ࡯ࡳ࡭ࡓࡶࡴ࡬ࡩ࡭ࡧࠪ࠾"),
  bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࠿"): bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭ࡀ"),
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡁ"): bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨࡂ"),
  bstack1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨࡃ"): bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡲࡹࡷࡩࡥࠨࡄ"),
  bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡅ"): bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࡆ"),
  bstack1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡇ"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧࡈ"),
}
bstack1ll1l11l1_opy_ = [
  bstack1l_opy_ (u"ࠧࡰࡵࠪࡉ"),
  bstack1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࡊ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡋ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࡌ"),
  bstack1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨࡍ"),
  bstack1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩࡎ"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ࡏ"),
]
bstack11l111l1_opy_ = {
  bstack1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࡐ"): bstack1l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࡑ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࡒ"): [bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࡓ"), bstack1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࡔ")],
  bstack1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࡕ"): bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫࡖ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫࡗ"): bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨࡘ"),
  bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫࡙ࠧ"): [bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࠫ"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧ࡛ࠪ")],
  bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࡜"): bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ࡝"),
  bstack1l_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫ࡞"): bstack1l_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭࡟"),
  bstack1l_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩࡠ"): [bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪࡡ"), bstack1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬࡢ")],
  bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫࡣ"): [bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹࡹࠧࡤ"), bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡓࡴ࡮ࡆࡩࡷࡺࠧࡥ")]
}
bstack11111111_opy_ = [
  bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧࡦ"),
  bstack1l_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬࡧ"),
  bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩࡨ"),
  bstack1l_opy_ (u"ࠫࡸ࡫ࡴࡘ࡫ࡱࡨࡴࡽࡒࡦࡥࡷࠫࡩ"),
  bstack1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡲࡹࡹࡹࠧࡪ"),
  bstack1l_opy_ (u"࠭ࡳࡵࡴ࡬ࡧࡹࡌࡩ࡭ࡧࡌࡲࡹ࡫ࡲࡢࡥࡷࡥࡧ࡯࡬ࡪࡶࡼࠫ࡫"),
  bstack1l_opy_ (u"ࠧࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡓࡶࡴࡳࡰࡵࡄࡨ࡬ࡦࡼࡩࡰࡴࠪ࡬"),
  bstack1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭࡭"),
  bstack1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ࡮"),
  bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ࡯"),
  bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪࡰ"),
  bstack1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ࡱ"),
]
bstack1l1lll111_opy_ = [
  bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪࡲ"),
  bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࡳ"),
  bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࡴ"),
  bstack1l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩࡵ"),
  bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࡶ"),
  bstack1l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ࡷ"),
  bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨࡸ"),
  bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪࡹ"),
  bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪࡺ"),
]
bstack1llll11l1_opy_ = [
  bstack1l_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࡻ"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡼ"),
  bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࡽ"),
  bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࡾ"),
  bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࡿ"),
  bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢀ"),
  bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢁ"),
  bstack1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢂ"),
  bstack1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢃ"),
  bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢄ"),
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢅ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢆ"),
  bstack1l_opy_ (u"࠭࡯ࡴࠩࢇ"),
  bstack1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ࢈"),
  bstack1l_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢉ"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢊ"),
  bstack1l_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢋ"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢌ"),
  bstack1l_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢍ"),
  bstack1l_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢎ"),
  bstack1l_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬ࢏"),
  bstack1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬ࢐"),
  bstack1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨ࢑"),
  bstack1l_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧ࢒"),
  bstack1l_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬ࢓"),
  bstack1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ࢔"),
  bstack1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ࢕"),
  bstack1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨ࢖"),
  bstack1l_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࢗ"),
  bstack1l_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭࢘"),
  bstack1l_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐ࢙ࠬ"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࢚࠭"),
  bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷ࢛ࠬ"),
  bstack1l_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࢜"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࢝"),
  bstack1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢞"),
  bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࢟"),
  bstack1l_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪࠫࢠ"),
  bstack1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵࠪࢡ"),
  bstack1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴࠩࢢ"),
  bstack1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࢣ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࢤ"),
  bstack1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࢥ"),
  bstack1l_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࢦ"),
  bstack1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࢧ"),
  bstack1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢨ"),
  bstack1l_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࢩ"),
  bstack1l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࢪ"),
  bstack1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࢫ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࢬ"),
  bstack1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࢭ"),
  bstack1l_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࢮ"),
  bstack1l_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬࢯ"),
  bstack1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫࢰ"),
  bstack1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫࢱ"),
  bstack1l_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧࢲ"),
  bstack1l_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࢳ"),
  bstack1l_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࢴ"),
  bstack1l_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࢵ"),
  bstack1l_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࢶ"),
  bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࢷ"),
  bstack1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࠧࢸ"),
  bstack1l_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧࢹ"),
  bstack1l_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨࢺ"),
  bstack1l_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨࢻ"),
  bstack1l_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪࠪࢼ"),
  bstack1l_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸࠬࢽ"),
  bstack1l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨࢾ"),
  bstack1l_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࠪࢿ"),
  bstack1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ࣀ"),
  bstack1l_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࠫࣁ"),
  bstack1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣂ"),
  bstack1l_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣃ"),
  bstack1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣄ"),
  bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬࣅ"),
  bstack1l_opy_ (u"࠭ࡩࡦࠩࣆ"),
  bstack1l_opy_ (u"ࠧࡦࡦࡪࡩࠬࣇ"),
  bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣈ"),
  bstack1l_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣉ"),
  bstack1l_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬ࣊"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬ࣋"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫ࣌"),
  bstack1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩ࣍"),
  bstack1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪ࣎"),
  bstack1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷ࣏ࠬ"),
  bstack1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦ࣐ࠩ"),
  bstack1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧ࣑ࠪ"),
  bstack1l_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࣒࠭"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࣓࠭"),
  bstack1l_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩࣔ"),
  bstack1l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧࣕ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩࣖ"),
  bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࣗ"),
  bstack1l_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨࣘ"),
  bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ࣙ"),
  bstack1l_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩࣚ"),
  bstack1l_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬࣛ"),
  bstack1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫࣜ"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫࣝ"),
  bstack1l_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣞ"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨࣟ"),
  bstack1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭࣠"),
  bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣡"),
  bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨ࣢"),
  bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࣣ࠭"),
  bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࣤ"),
  bstack1l_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬࣥ"),
  bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࣦࠩ"),
  bstack1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭ࣧ"),
  bstack1l_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨࣨ")
]
bstack11l1l1ll_opy_ = {
  bstack1l_opy_ (u"࠭ࡶࠨࣩ"): bstack1l_opy_ (u"ࠧࡷࠩ࣪"),
  bstack1l_opy_ (u"ࠨࡨࠪ࣫"): bstack1l_opy_ (u"ࠩࡩࠫ࣬"),
  bstack1l_opy_ (u"ࠪࡪࡴࡸࡣࡦ࣭ࠩ"): bstack1l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࣮ࠪ"),
  bstack1l_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨ࣯ࠫ"): bstack1l_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࣰࠬ"),
  bstack1l_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࣱࠫ"): bstack1l_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࣲࠬ"),
  bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬࣳ"): bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ࣴ"),
  bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧࣵ"): bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨࣶ"),
  bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩࣷ"): bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪࣸ"),
  bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࣹࠫ"): bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࣺࠬ"),
  bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫࣻ"): bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬࣼ"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ࣽ"): bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧࣾ"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨࣿ"): bstack1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऀ"),
  bstack1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫँ"): bstack1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬं"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬः"): bstack1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧऄ"),
  bstack1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨअ"): bstack1l_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩआ"),
  bstack1l_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬइ"): bstack1l_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ई"),
  bstack1l_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫउ"): bstack1l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऊ"),
  bstack1l_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऋ"): bstack1l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऌ"),
  bstack1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪऍ"): bstack1l_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫऎ"),
  bstack1l_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪए"): bstack1l_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫऐ"),
  bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ऑ"): bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
}
bstack1111111l_opy_ = bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧओ")
bstack1l1l111l_opy_ = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪऔ")
bstack1l1l1111_opy_ = {
  bstack1l_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪक"): 50,
  bstack1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨख"): 40,
  bstack1l_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫग"): 30,
  bstack1l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩघ"): 20,
  bstack1l_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫङ"): 10
}
DEFAULT_LOG_LEVEL = bstack1l1l1111_opy_[bstack1l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫच")]
bstack1l11l1l1_opy_ = bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭छ")
bstack1lll11_opy_ = bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ज")
bstack11ll11_opy_ = bstack1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨझ")
bstack1ll111l_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩञ")
bstack1ll11ll1l_opy_ = [bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬट"), bstack1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬठ")]
bstack1ll111ll_opy_ = [bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩड"), bstack1l_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩढ")]
bstack1l1lllll1_opy_ = [
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩण"),
  bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫत"),
  bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧथ"),
  bstack1l_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨद"),
  bstack1l_opy_ (u"ࠬࡧࡰࡱࠩध"),
  bstack1l_opy_ (u"࠭ࡵࡥ࡫ࡧࠫन"),
  bstack1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩऩ"),
  bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨप"),
  bstack1l_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧफ"),
  bstack1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨब"),
  bstack1l_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬभ"), bstack1l_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨम"),
  bstack1l_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩय"),
  bstack1l_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭र"),
  bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬऱ"),
  bstack1l_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬल"),
  bstack1l_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫळ"),
  bstack1l_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩऴ"), bstack1l_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩव"), bstack1l_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨश"), bstack1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨष"), bstack1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪस"),
  bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧह"),
  bstack1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧऺ"),
  bstack1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭ऻ"), bstack1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵ़ࠩ"),
  bstack1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫऽ"),
  bstack1l_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨा"),
  bstack1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧि"),
  bstack1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪी"),
  bstack1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨु"),
  bstack1l_opy_ (u"ࠫࡦࡼࡤࠨू"), bstack1l_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨृ"), bstack1l_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨॄ"), bstack1l_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨॅ"),
  bstack1l_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭ॆ"), bstack1l_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨे"), bstack1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ࠭ै"),
  bstack1l_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭ॉ"), bstack1l_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦࠪॊ"),
  bstack1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨो"), bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪौ"), bstack1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ्࠭"), bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫॎ"), bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧॏ"),
  bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧॐ"), bstack1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩ॑"),
  bstack1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨ॒"),
  bstack1l_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬ॓"),
  bstack1l_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧ॔"), bstack1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪॕ"), bstack1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨॖ"), bstack1l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧॗ"),
  bstack1l_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶࠪक़"),
  bstack1l_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨख़"), bstack1l_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧग़"),
  bstack1l_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨज़"),
  bstack1l_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫड़"),
  bstack1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬढ़"),
  bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫफ़"),
  bstack1l_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭य़"),
  bstack1l_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬॠ"),
  bstack1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨॡ"),
  bstack1l_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧॢ"),
  bstack1l_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ॣ"),
  bstack1l_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧ।"),
  bstack1l_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬ॥"),
  bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫ०"),
  bstack1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪ१"),
  bstack1l_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧ२"),
  bstack1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭३"),
  bstack1l_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭४"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪ५"),
  bstack1l_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨ६"), bstack1l_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩ७"), bstack1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩ८"),
  bstack1l_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫ९"),
  bstack1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬ॰"),
  bstack1l_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫॱ"),
  bstack1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬॲ"),
  bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨॳ"),
  bstack1l_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩॴ"),
  bstack1l_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩॵ"), bstack1l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ॶ"), bstack1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫॷ"),
  bstack1l_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩॸ"),
  bstack1l_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫॹ"),
  bstack1l_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ॺ"),
  bstack1l_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬॻ"),
  bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥࠩॼ"), bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭ॽ"),
  bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫॾ"), bstack1l_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ॿ"),
  bstack1l_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪঀ"),
  bstack1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪঁ"),
  bstack1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨং"), bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪঃ"), bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫ঄"), bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨঅ"),
  bstack1l_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩআ"),
  bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫই"),
  bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧঈ"),
  bstack1l_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬউ"),
  bstack1l_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪঊ"),
  bstack1l_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩঋ"),
  bstack1l_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩঌ"), bstack1l_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶࠪ঍"),
  bstack1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭঎"),
  bstack1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫএ"),
  bstack1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭ঐ"),
  bstack1l_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭঑"),
  bstack1l_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩ঒"),
  bstack1l_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫও"),
  bstack1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪঔ"),
  bstack1l_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫক"),
  bstack1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫখ"),
  bstack1l_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪগ"),
  bstack1l_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫঘ"),
  bstack1l_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭ঙ"),
  bstack1l_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧচ"),
  bstack1l_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫছ"),
  bstack1l_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬজ"),
  bstack1l_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧঝ"),
  bstack1l_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭ঞ"),
  bstack1l_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧট"),
  bstack1l_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫঠ"),
  bstack1l_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧড"),
  bstack1l_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬঢ"),
  bstack1l_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ণ"), bstack1l_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫত"),
  bstack1l_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩথ"), bstack1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧদ"),
  bstack1l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬধ"),
  bstack1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫন"),
  bstack1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫ঩"),
  bstack1l_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧপ"), bstack1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧফ"),
  bstack1l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨব"),
  bstack1l_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫভ"),
  bstack1l_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧম"),
  bstack1l_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩয"),
  bstack1l_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫর"),
  bstack1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭঱"),
  bstack1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩল"),
  bstack1l_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫ঳"),
  bstack1l_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨ঴"),
  bstack1l_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭঵"), bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬশ"),
  bstack1l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩষ")
]
bstack1ll1ll1_opy_ = bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩস")
bstack1lllll1_opy_ = [bstack1l_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩহ"), bstack1l_opy_ (u"ࠬ࠴ࡡࡢࡤࠪ঺"), bstack1l_opy_ (u"࠭࠮ࡪࡲࡤࠫ঻")]
bstack1ll1l11ll_opy_ = [bstack1l_opy_ (u"ࠧࡪࡦ়ࠪ"), bstack1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ঽ"), bstack1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬা"), bstack1l_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩি")]
bstack1lll11l11_opy_ = {
  bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫী"): bstack1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪু"),
  bstack1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧূ"): bstack1l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬৃ"),
  bstack1l_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৄ"): bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৅"),
  bstack1l_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭৆"): bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪে"),
  bstack1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬৈ"): bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧ৉")
}
bstack1l1111ll_opy_ = [
  bstack1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৊"),
  bstack1l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ো"),
  bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪৌ"),
  bstack1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴ্ࠩ"),
  bstack1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬৎ"),
]
bstack111l11l_opy_ = bstack1l1lll111_opy_ + bstack1llll11l1_opy_ + bstack1l1lllll1_opy_
bstack1111l111_opy_ = [
  bstack1l_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪ৏"),
  bstack1l_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧ৐"),
  bstack1l_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭৑"),
  bstack1l_opy_ (u"ࠨࡠ࠴࠴࠳࠭৒"),
  bstack1l_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨ৓"),
  bstack1l_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩ৔"),
  bstack1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪ৕"),
  bstack1l_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨ৖")
]
bstack1ll1l1l_opy_ = bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿࠪৗ")
bstack111lll1_opy_ = bstack1l_opy_ (u"ࠧࡴࡦ࡮࠳ࡻ࠷࠯ࡦࡸࡨࡲࡹ࠭৘")
bstack1ll1ll11l_opy_ = [ bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ৙") ]
bstack1ll11l11_opy_ = [ bstack1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ৚") ]
bstack1lll1_opy_ = [ bstack1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ৛") ]
bstack11lll1_opy_ = bstack1l_opy_ (u"ࠫࡘࡊࡋࡔࡧࡷࡹࡵ࠭ড়")
bstack111ll1l1_opy_ = bstack1l_opy_ (u"࡙ࠬࡄࡌࡖࡨࡷࡹࡇࡴࡵࡧࡰࡴࡹ࡫ࡤࠨঢ়")
bstack111ll_opy_ = bstack1l_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠪ৞")
bstack1ll1l1l1l_opy_ = bstack1l_opy_ (u"ࠧ࠵࠰࠳࠲࠵࠭য়")
bstack1lll1ll1l_opy_ = bstack1l_opy_ (u"ࠨࡕࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠭ࠢࡸࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠾ࠥࢁࡽࠨৠ")
bstack1l1ll1111_opy_ = bstack1l_opy_ (u"ࠩࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡹࡥࡵࡷࡳࠥࠬৡ")
bstack1111l11l_opy_ = bstack1l_opy_ (u"ࠪࡔࡦࡸࡳࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠬৢ")
bstack11l11111_opy_ = bstack1l_opy_ (u"ࠫࡘࡧ࡮ࡪࡶ࡬ࡾࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࡻࡾࠩৣ")
bstack11111l1l_opy_ = bstack1l_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤ࡭ࡻࡢࠡࡷࡵࡰ࠿ࠦࡻࡾࠩ৤")
bstack11l1l_opy_ = bstack1l_opy_ (u"࠭ࡓࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࡿࢂ࠭৥")
bstack1llllll1_opy_ = bstack1l_opy_ (u"ࠧࡓࡧࡦࡩ࡮ࡼࡥࡥࠢ࡬ࡲࡹ࡫ࡲࡳࡷࡳࡸ࠱ࠦࡥࡹ࡫ࡷ࡭ࡳ࡭ࠧ০")
bstack1l1lll1l_opy_ = bstack1l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࡥ࠭১")
bstack1l11lll_opy_ = bstack1l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶࠣࡥࡳࡪࠠࡱࡻࡷࡩࡸࡺ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡳࡥࡨࡱࡡࡨࡧࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡵࡿࡴࡦࡵࡷ࠱ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡦࠧ২")
bstack1l11llll_opy_ = bstack1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡷࡵࡢࡰࡶ࠯ࠤࡵࡧࡢࡰࡶࠣࡥࡳࡪࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࡮࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧࡶࠤࡹࡵࠠࡳࡷࡱࠤࡷࡵࡢࡰࡶࠣࡸࡪࡹࡴࡴࠢ࡬ࡲࠥࡶࡡࡳࡣ࡯ࡰࡪࡲ࠮ࠡࡢࡳ࡭ࡵࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠯ࡳࡥࡧࡵࡴࠡࡴࡲࡦࡴࡺࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࡤࠬ৩")
bstack111l11l1_opy_ = bstack1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡨࡥࡩࡣࡹࡩࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࡤࠬ৪")
bstack111l1111_opy_ = bstack1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡡࡱࡲ࡬ࡹࡲ࠳ࡣ࡭࡫ࡨࡲࡹࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡇࡰࡱ࡫ࡸࡱ࠲ࡖࡹࡵࡪࡲࡲ࠲ࡉ࡬ࡪࡧࡱࡸࡥ࠭৫")
bstack111lll1l_opy_ = bstack1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࡠࠨ৬")
bstack11llll_opy_ = bstack1l_opy_ (u"ࠧࡉࡣࡱࡨࡱ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡱࡵࡳࡦࠩ৭")
bstack11ll1111_opy_ = bstack1l_opy_ (u"ࠨࡃ࡯ࡰࠥࡪ࡯࡯ࡧࠤࠫ৮")
bstack11l11l1_opy_ = bstack1l_opy_ (u"ࠩࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࠡࡣࡷࠤࠧࢁࡽࠣ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡩ࡬ࡶࡦࡨࠤࡦࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡩࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡧࡶࡸࡸ࠴ࠧ৯")
bstack1lll1111_opy_ = bstack1l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠ࡯ࡱࡷࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡹ࡮ࡥ࡮ࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡡࡴࠢࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧࠦࡡ࡯ࡦࠣࠦࡦࡩࡣࡦࡵࡶࡏࡪࡿࠢࠡࡱࡵࠤࡸ࡫ࡴࠡࡶ࡫ࡩࡲࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠽ࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨࠠࡢࡰࡧࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠣࠩৰ")
bstack1l1111l1_opy_ = bstack1l_opy_ (u"ࠫࡒࡧ࡬ࡧࡱࡵࡱࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠨࡻࡾࠤࠪৱ")
bstack1ll1111l_opy_ = bstack1l_opy_ (u"ࠬࡋ࡮ࡤࡱࡸࡲࡹ࡫ࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࠳ࠠࡼࡿࠪ৲")
bstack11l11ll1_opy_ = bstack1l_opy_ (u"࠭ࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭৳")
bstack1ll1ll1l_opy_ = bstack1l_opy_ (u"ࠧࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧ৴")
bstack111l1ll1_opy_ = bstack1l_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࠦࡩࡴࠢࡱࡳࡼࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠡࠨ৵")
bstack1lll1l1l_opy_ = bstack1l_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭࠼ࠣࡿࢂ࠭৶")
bstack1ll1l1_opy_ = bstack1l_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡲ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࢀࢃࠧ৷")
bstack1l1ll1ll_opy_ = bstack1l_opy_ (u"࡚ࠫࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬ৸")
bstack1lll1lll_opy_ = bstack1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀࠫ৹")
bstack1ll1l1111_opy_ = bstack1l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࠠࡢࡰࠣࡥࡵࡶࡲࡰࡲࡵ࡭ࡦࡺࡥࠡࡈ࡚ࠤ࠭ࡸ࡯ࡣࡱࡷ࠳ࡵࡧࡢࡰࡶࠬࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠱ࠦࡳ࡬࡫ࡳࠤࡹ࡮ࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵ࡬ࡱࡵࡲࡥࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡤࡲࡾࠦࡆࡘ࠰ࠪ৺")
bstack11l11ll_opy_ = bstack1l_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡪࡷࡸࡵࡖࡲࡰࡺࡼ࠳࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡴࡴࠠࡤࡷࡵࡶࡪࡴࡴ࡭ࡻࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥ࠮ࡻࡾࠫ࠯ࠤࡵࡲࡥࡢࡵࡨࠤࡺࡶࡧࡳࡣࡧࡩࠥࡺ࡯ࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡁࡁ࠹࠴࠰࠯࠲ࠣࡳࡷࠦࡲࡦࡨࡨࡶࠥࡺ࡯ࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡱ࡫࡮ࡪࡷࡰ࠳ࡷࡻ࡮࠮ࡶࡨࡷࡹࡹ࠭ࡣࡧ࡫࡭ࡳࡪ࠭ࡱࡴࡲࡼࡾࠩࡰࡺࡶ࡫ࡳࡳࠦࡦࡰࡴࠣࡥࠥࡽ࡯ࡳ࡭ࡤࡶࡴࡻ࡮ࡥ࠰ࠪ৻")
bstack111lll_opy_ = bstack1l_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴࠮ࠨৼ")
bstack11ll1l1l_opy_ = bstack1l_opy_ (u"ࠩࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡩࡨࡲࡪࡸࡡࡵࡧࡧࠤࡹ࡮ࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠧࠧ৽")
bstack11ll1l1_opy_ = bstack1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦ࠰ࠣࡿࢂ࠭৾")
bstack1l1111_opy_ = bstack1l_opy_ (u"ࠫࡊࡾࡰࡦࡥࡷࡩࡩࠦࡡࡵࠢ࡯ࡩࡦࡹࡴࠡ࠳ࠣ࡭ࡳࡶࡵࡵ࠮ࠣࡶࡪࡩࡥࡪࡸࡨࡨࠥ࠶ࠧ৿")
bstack1lll1l11l_opy_ = bstack1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩࡻࡲࡪࡰࡪࠤࡆࡶࡰࠡࡷࡳࡰࡴࡧࡤ࠯ࠢࡾࢁࠬ਀")
bstack1l1lll1_opy_ = bstack1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡄࡴࡵ࠴ࠠࡊࡰࡹࡥࡱ࡯ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡻࡾ࠰ࠪਁ")
bstack1l1l1_opy_ = bstack1l_opy_ (u"ࠧࡌࡧࡼࡷࠥࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࠮ࡧࡻ࡭ࡸࡺࠠࡢࡵࠣࡥࡵࡶࠠࡷࡣ࡯ࡹࡪࡹࠬࠡࡷࡶࡩࠥࡧ࡮ࡺࠢࡲࡲࡪࠦࡰࡳࡱࡳࡩࡷࡺࡹࠡࡨࡵࡳࡲࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠰ࠥࡵ࡮࡭ࡻࠣࠦࡵࡧࡴࡩࠤࠣࡥࡳࡪࠠࠣࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠦࠥࡩࡡ࡯ࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡹࡵࡧࡦࡶ࡫ࡩࡷ࠴ࠧਂ")
bstack1l1ll11_opy_ = bstack1l_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠣࡥࡷ࡫ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪਃ")
bstack1lllll111_opy_ = bstack1l_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡘࡻࡰࡱࡱࡵࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࡹࠠࡰࡨࠣࡥࡵࡶࠠࡢࡴࡨࠤࡴ࡬ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ਄")
bstack11l1l11l_opy_ = bstack1l_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡶࡰࠡ࡫ࡧࠤࢀࢃࠠࡧࡱࡵࠤ࡭ࡧࡳࡩࠢ࠽ࠤࢀࢃ࠮ࠨਅ")
bstack1l1lll1ll_opy_ = bstack1l_opy_ (u"ࠫࡆࡶࡰࠡࡗࡳࡰࡴࡧࡤࡦࡦࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠣࡍࡉࠦ࠺ࠡࡽࢀࠫਆ")
bstack1l1ll11l_opy_ = bstack1l_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡆࡶࡰࠡ࠼ࠣࡿࢂ࠴ࠧਇ")
bstack1l11l11l_opy_ = bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡱࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠲ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡴࡤࡰࡱ࡫࡬ࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥࡃࠠ࠲ࠩਈ")
bstack1l1llllll_opy_ = bstack1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡀࠠࡼࡿࠪਉ")
bstack1l1l11lll_opy_ = bstack1l_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵ࠾ࠥࢁࡽࠨਊ")
bstack11ll1l_opy_ = bstack1l_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡵࡩࡦࡹ࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥ࠯ࠢࡾࢁࠬ਋")
bstack1llll11ll_opy_ = bstack1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡤࡴ࡮ࠦࡣࡢ࡮࡯࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ਌")
bstack1l1llll1l_opy_ = bstack1l_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡪࡲࡻࠥࡨࡵࡪ࡮ࡧࠤ࡚ࡘࡌ࠭ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡷࡶࡩࡩ࠴ࠧ਍")
bstack1ll11l1_opy_ = bstack1l_opy_ (u"࡙ࠬࡥࡳࡸࡨࡶࠥࡹࡩࡥࡧࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠮ࡻࡾࠫࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡦࡳࡥࠡࡣࡶࠤࡨࡲࡩࡦࡰࡷࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠩ਎")
bstack11llll1l_opy_ = bstack1l_opy_ (u"࠭ࡖࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠻ࠢࡾࢁࠬਏ")
bstack1lllll11_opy_ = bstack1l_opy_ (u"ࠧࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡥࡨࡩࡥࡴࡵࠣࡥࠥࡶࡲࡪࡸࡤࡸࡪࠦࡤࡰ࡯ࡤ࡭ࡳࡀࠠࡼࡿࠣ࠲࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡦࡰ࡮࡯ࡳࡼ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡲࠥࡿ࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠾ࠥࡢ࡮࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱ࠥࡢ࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰ࠿ࠦࡴࡳࡷࡨࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠫਐ")
bstack1111ll1_opy_ = bstack1l_opy_ (u"ࠨࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࡤ࡫ࡲࡳࡱࡵࠤ࠿ࠦࡻࡾࠩ਑")
bstack1l1l1lll1_opy_ = bstack1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏࡘ࡫ࡴࡶࡲࠣࡿࢂࠨ਒")
bstack1ll111l1_opy_ = bstack1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥࢁࡽࠣਓ")
bstack1l1l1l1ll_opy_ = bstack1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡰࡧࡣࡦࡳࡰ࡭࡫ࡷࡹࡩ࡫࡟ࡦࡸࡨࡲࡹࠦࡦࡰࡴࠣࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠠࡼࡿࠥਔ")
bstack111l1l1_opy_ = bstack1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡵࡩࡤࡸࡥࡲࡷࡨࡷࡹࠦࡻࡾࠤਕ")
bstack111ll1l_opy_ = bstack1l_opy_ (u"ࠨࡐࡐࡕࡗࠤࡊࡼࡥ࡯ࡶࠣࡿࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡ࠼ࠣࡿࢂࠨਖ")
bstack1lll111l_opy_ = bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡰࡳࡱࡻࡽࠥࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫਗ")
bstack11l1_opy_ = bstack1l_opy_ (u"ࠨࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࠡࠢ࡬ࡪ࠭ࡶࡡࡨࡧࠣࡁࡂࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠡࡽ࡟ࡲࠥࠦࠠࡵࡴࡼࡿࡡࡴࠠࡤࡱࡱࡷࡹࠦࡦࡴࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭ࡢࠧࡧࡵ࡟ࠫ࠮ࡁ࡜࡯ࠢࠣࠤࠥࠦࡦࡴ࠰ࡤࡴࡵ࡫࡮ࡥࡈ࡬ࡰࡪ࡙ࡹ࡯ࡥࠫࡦࡸࡺࡡࡤ࡭ࡢࡴࡦࡺࡨ࠭ࠢࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡴࡤ࡯࡮ࡥࡧࡻ࠭ࠥ࠱ࠠࠣ࠼ࠥࠤ࠰ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬ࠭ࡧࡷࡢ࡫ࡷࠤࡳ࡫ࡷࡑࡣࡪࡩ࠷࠴ࡥࡷࡣ࡯ࡹࡦࡺࡥࠩࠤࠫ࠭ࠥࡃ࠾ࠡࡽࢀࠦ࠱ࠦ࡜ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡩࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡉ࡫ࡴࡢ࡫࡯ࡷࠧࢃ࡜ࠨࠫࠬ࠭ࡠࠨࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠤࡠ࠭ࠥ࠱ࠠࠣ࠮࡟ࡠࡳࠨࠩ࡝ࡰࠣࠤࠥࠦࡽࡤࡣࡷࡧ࡭࠮ࡥࡹࠫࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡾ࡞ࡱࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯ࠨਘ")
bstack11l1ll1_opy_ = bstack1l_opy_ (u"ࠩ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬ࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡦࡸࡺࡡࡤ࡭ࡢࡧࡦࡶࡳࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠵ࡢࡢ࡮ࡤࡱࡱࡷࡹࠦࡰࡠ࡫ࡱࡨࡪࡾࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠵ࡡࡡࡴࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴ࡳ࡭࡫ࡦࡩ࠭࠶ࠬࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶࠭ࡡࡴࡣࡰࡰࡶࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭ࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ࠮ࡁ࡜࡯࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯࡮ࡤࡹࡳࡩࡨࠡ࠿ࠣࡥࡸࡿ࡮ࡤࠢࠫࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠬࠤࡂࡄࠠࡼ࡞ࡱࡰࡪࡺࠠࡤࡣࡳࡷࡀࡢ࡮ࡵࡴࡼࠤࢀࡢ࡮ࡤࡣࡳࡷࠥࡃࠠࡋࡕࡒࡒ࠳ࡶࡡࡳࡵࡨࠬࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠫ࡟ࡲࠥࠦࡽࠡࡥࡤࡸࡨ࡮ࠨࡦࡺࠬࠤࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡤࡻࡦ࡯ࡴࠡ࡫ࡰࡴࡴࡸࡴࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠹ࡥࡢࡴࡶࡤࡧࡰ࠴ࡣࡩࡴࡲࡱ࡮ࡻ࡭࠯ࡥࡲࡲࡳ࡫ࡣࡵࠪࡾࡠࡳࠦࠠࠡࠢࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹࡀࠠࡡࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠧࡿࡪࡴࡣࡰࡦࡨ࡙ࡗࡏࡃࡰ࡯ࡳࡳࡳ࡫࡮ࡵࠪࡍࡗࡔࡔ࠮ࡴࡶࡵ࡭ࡳ࡭ࡩࡧࡻࠫࡧࡦࡶࡳࠪࠫࢀࡤ࠱ࡢ࡮ࠡࠢࠣࠤ࠳࠴࠮࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹ࡜࡯ࠢࠣࢁ࠮ࡢ࡮ࡾ࡞ࡱ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࡢ࡮ࠨਙ")
from ._version import __version__
bstack1111l1ll_opy_ = None
CONFIG = {}
bstack11lll11l_opy_ = None
bstack11l1ll_opy_ = None
bstack1l1ll111l_opy_ = None
bstack1l1l11l_opy_ = -1
bstack1l11ll1_opy_ = DEFAULT_LOG_LEVEL
bstack1lllll1ll_opy_ = 1
bstack1l1ll1l1l_opy_ = False
bstack11l11_opy_ = bstack1l_opy_ (u"ࠪࠫਚ")
bstack1ll11l_opy_ = bstack1l_opy_ (u"ࠫࠬਛ")
bstack1l111111_opy_ = False
bstack1l1ll1ll1_opy_ = True
bstack1lll1l1ll_opy_ = None
bstack1lllll1l1_opy_ = None
bstack11lll_opy_ = None
bstack1llll11l_opy_ = None
bstack111l11_opy_ = None
bstack1111_opy_ = None
bstack11ll_opy_ = None
bstack1ll11l11l_opy_ = None
bstack111l1_opy_ = None
bstack111l_opy_ = None
bstack1l11l111_opy_ = None
bstack111ll11l_opy_ = None
bstack1ll111lll_opy_ = bstack1l_opy_ (u"ࠧࠨਜ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1l11ll1_opy_,
                    format=bstack1l_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫਝ"),
                    datefmt=bstack1l_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩਞ"))
def bstack1111l1l1_opy_():
  global CONFIG
  global bstack1l11ll1_opy_
  if bstack1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪਟ") in CONFIG:
    bstack1l11ll1_opy_ = bstack1l1l1111_opy_[CONFIG[bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫਠ")]]
    logging.getLogger().setLevel(bstack1l11ll1_opy_)
def bstack1ll1ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lll111l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧਡ") in args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1lll1l1ll_opy_
      bstack1lll1l1ll_opy_ = path
      return path
  return None
def bstack1lll1l1_opy_():
  bstack11l1111l_opy_ = bstack1lll111l1_opy_()
  if bstack11l1111l_opy_ and os.path.exists(os.path.abspath(bstack11l1111l_opy_)):
    fileName = bstack11l1111l_opy_
  if bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨਢ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩਣ")])) and not bstack1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨਤ") in locals():
    fileName = os.environ[bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫਥ")]
  if not bstack1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪਦ") in locals():
    fileName = bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬਧ")
  bstack111l1l1l_opy_ = os.path.abspath(fileName)
  if not os.path.exists(bstack111l1l1l_opy_):
    fileName = bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧਨ")
    bstack111l1l1l_opy_ = os.path.abspath(fileName)
    if not os.path.exists(bstack111l1l1l_opy_):
      bstack1lll11l_opy_(
        bstack11l11l1_opy_.format(os.getcwd()))
  with open(bstack111l1l1l_opy_, bstack1l_opy_ (u"ࠫࡷ࠭਩")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack1lll11l_opy_(bstack1l1111l1_opy_.format(str(exc)))
def bstack1ll11111_opy_(config):
  bstack1lll11ll_opy_ = bstack11ll111l_opy_(config)
  for option in list(bstack1lll11ll_opy_):
    if option.lower() in bstack11l1l1ll_opy_ and option != bstack11l1l1ll_opy_[option.lower()]:
      bstack1lll11ll_opy_[bstack11l1l1ll_opy_[option.lower()]] = bstack1lll11ll_opy_[option]
      del bstack1lll11ll_opy_[option]
  return config
def bstack11lllll_opy_(config):
  bstack1l1ll1l_opy_ = config.keys()
  for bstack1l11l1_opy_, bstack11llllll_opy_ in bstack11l111_opy_.items():
    if bstack11llllll_opy_ in bstack1l1ll1l_opy_:
      config[bstack1l11l1_opy_] = config[bstack11llllll_opy_]
      del config[bstack11llllll_opy_]
  for bstack1l11l1_opy_, bstack11llllll_opy_ in bstack11l111l1_opy_.items():
    if isinstance(bstack11llllll_opy_, list):
      for bstack111lllll_opy_ in bstack11llllll_opy_:
        if bstack111lllll_opy_ in bstack1l1ll1l_opy_:
          config[bstack1l11l1_opy_] = config[bstack111lllll_opy_]
          del config[bstack111lllll_opy_]
          break
    elif bstack11llllll_opy_ in bstack1l1ll1l_opy_:
        config[bstack1l11l1_opy_] = config[bstack11llllll_opy_]
        del config[bstack11llllll_opy_]
  for bstack111lllll_opy_ in list(config):
    for bstack1l111l1_opy_ in bstack111l11l_opy_:
      if bstack111lllll_opy_.lower() == bstack1l111l1_opy_.lower() and bstack111lllll_opy_ != bstack1l111l1_opy_:
        config[bstack1l111l1_opy_] = config[bstack111lllll_opy_]
        del config[bstack111lllll_opy_]
  bstack11l1ll1l_opy_ = []
  if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਪ") in config:
    bstack11l1ll1l_opy_ = config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਫ")]
  for platform in bstack11l1ll1l_opy_:
    for bstack111lllll_opy_ in list(platform):
      for bstack1l111l1_opy_ in bstack111l11l_opy_:
        if bstack111lllll_opy_.lower() == bstack1l111l1_opy_.lower() and bstack111lllll_opy_ != bstack1l111l1_opy_:
          platform[bstack1l111l1_opy_] = platform[bstack111lllll_opy_]
          del platform[bstack111lllll_opy_]
  for bstack1l11l1_opy_, bstack11llllll_opy_ in bstack11l111l1_opy_.items():
    for platform in bstack11l1ll1l_opy_:
      if isinstance(bstack11llllll_opy_, list):
        for bstack111lllll_opy_ in bstack11llllll_opy_:
          if bstack111lllll_opy_ in platform:
            platform[bstack1l11l1_opy_] = platform[bstack111lllll_opy_]
            del platform[bstack111lllll_opy_]
            break
      elif bstack11llllll_opy_ in platform:
        platform[bstack1l11l1_opy_] = platform[bstack11llllll_opy_]
        del platform[bstack11llllll_opy_]
  for bstack1ll1l1ll1_opy_ in bstack1lll11l11_opy_:
    if bstack1ll1l1ll1_opy_ in config:
      if not bstack1lll11l11_opy_[bstack1ll1l1ll1_opy_] in config:
        config[bstack1lll11l11_opy_[bstack1ll1l1ll1_opy_]] = {}
      config[bstack1lll11l11_opy_[bstack1ll1l1ll1_opy_]].update(config[bstack1ll1l1ll1_opy_])
      del config[bstack1ll1l1ll1_opy_]
  for platform in bstack11l1ll1l_opy_:
    for bstack1ll1l1ll1_opy_ in bstack1lll11l11_opy_:
      if bstack1ll1l1ll1_opy_ in list(platform):
        if not bstack1lll11l11_opy_[bstack1ll1l1ll1_opy_] in platform:
          platform[bstack1lll11l11_opy_[bstack1ll1l1ll1_opy_]] = {}
        platform[bstack1lll11l11_opy_[bstack1ll1l1ll1_opy_]].update(platform[bstack1ll1l1ll1_opy_])
        del platform[bstack1ll1l1ll1_opy_]
  config = bstack1ll11111_opy_(config)
  return config
def bstack1l1lllll_opy_(config):
  global bstack1ll11l_opy_
  if bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ") in config and str(config[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")]).lower() != bstack1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨਮ"):
    if not bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧਯ") in config:
      config[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨਰ")] = {}
    if not bstack1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ਱") in config[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪਲ")]:
      if bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩਲ਼") in os.environ:
        config[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ਴")][bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ")] = os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬਸ਼")]
      else:
        current_time = datetime.datetime.now()
        bstack1l1l11_opy_ = current_time.strftime(bstack1l_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨ਷"))
        hostname = socket.gethostname()
        bstack11111ll1_opy_ = bstack1l_opy_ (u"ࠬ࠭ਸ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack1l_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨਹ").format(bstack1l1l11_opy_, hostname, bstack11111ll1_opy_)
        config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ਺")][bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ਻")] = identifier
    bstack1ll11l_opy_ = config[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ਼࠭")][bstack1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ਽")]
  return config
def bstack1ll11l111_opy_(config):
  if bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧਾ") in config and config[bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨਿ")] not in bstack1ll111ll_opy_:
    return config[bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩੀ")]
  elif bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪੁ") in os.environ:
    return os.environ[bstack1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫੂ")]
  else:
    return None
def bstack1ll11llll_opy_(config):
  if bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬ੃") in os.environ:
    return os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊ࠭੄")]
  elif bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ੅") in config:
    return config[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ੆")]
  else:
    return None
def bstack111ll1ll_opy_():
  if (
    isinstance(os.getenv(bstack1l_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠫੇ")), str) and len(os.getenv(bstack1l_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠬੈ"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l_opy_ (u"ࠨࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠧ੉")), str) and len(os.getenv(bstack1l_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠨ੊"))) > 0
  ):
    return os.getenv(bstack1l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩੋ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠫࡈࡏࠧੌ"))).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧ੍ࠪ") and str(os.getenv(bstack1l_opy_ (u"࠭ࡃࡊࡔࡆࡐࡊࡉࡉࠨ੎"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ੏"):
    return os.getenv(bstack1l_opy_ (u"ࠨࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠫ੐"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࠬੑ"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ੒") and str(os.getenv(bstack1l_opy_ (u"࡙ࠫࡘࡁࡗࡋࡖࠫ੓"))).lower() == bstack1l_opy_ (u"ࠬࡺࡲࡶࡧࠪ੔"):
    return os.getenv(bstack1l_opy_ (u"࠭ࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬ੕"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࠪ੖"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭੗") and str(os.getenv(bstack1l_opy_ (u"ࠩࡆࡍࡤࡔࡁࡎࡇࠪ੘"))).lower() == bstack1l_opy_ (u"ࠪࡧࡴࡪࡥࡴࡪ࡬ࡴࠬਖ਼"):
    return 0 # bstack1l1l1l11l_opy_ bstack1l11111l_opy_ not set build number env
  if os.getenv(bstack1l_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠧਗ਼")) and os.getenv(bstack1l_opy_ (u"ࠬࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠨਜ਼")):
    return os.getenv(bstack1l_opy_ (u"࠭ࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨੜ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࠪ੝"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ਫ਼") and str(os.getenv(bstack1l_opy_ (u"ࠩࡇࡖࡔࡔࡅࠨ੟"))).lower() == bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ੠"):
    return os.getenv(bstack1l_opy_ (u"ࠫࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩ੡"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠬࡉࡉࠨ੢"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫ੣") and str(os.getenv(bstack1l_opy_ (u"ࠧࡔࡇࡐࡅࡕࡎࡏࡓࡇࠪ੤"))).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭੥"):
    return os.getenv(bstack1l_opy_ (u"ࠩࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠬ੦"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠪࡇࡎ࠭੧"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ੨") and str(os.getenv(bstack1l_opy_ (u"ࠬࡍࡉࡕࡎࡄࡆࡤࡉࡉࠨ੩"))).lower() == bstack1l_opy_ (u"࠭ࡴࡳࡷࡨࠫ੪"):
    return os.getenv(bstack1l_opy_ (u"ࠧࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠪ੫"), 0)
  if str(os.getenv(bstack1l_opy_ (u"ࠨࡅࡌࠫ੬"))).lower() == bstack1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ੭") and str(os.getenv(bstack1l_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡍࡌࡘࡊ࠭੮"))).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩ੯"):
    return os.getenv(bstack1l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧੰ"), 0)
  if str(os.getenv(bstack1l_opy_ (u"࠭ࡔࡇࡡࡅ࡙ࡎࡒࡄࠨੱ"))).lower() == bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬੲ"):
    return os.getenv(bstack1l_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨੳ"), 0)
  return -1
def bstack1ll1l1ll_opy_(bstack111l111_opy_):
  global CONFIG
  if not bstack1l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫੴ") in CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬੵ")]:
    return
  CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੶")] = CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ੷")].replace(
    bstack1l_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨ੸"),
    str(bstack111l111_opy_)
  )
def bstack111llll1_opy_():
  global CONFIG
  if not bstack1l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭੹") in CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ੺")]:
    return
  current_time = datetime.datetime.now()
  bstack1l1l11_opy_ = current_time.strftime(bstack1l_opy_ (u"ࠩࠨࡨ࠲ࠫࡢ࠮ࠧࡋ࠾ࠪࡓࠧ੻"))
  CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ੼")] = CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭੽")].replace(
    bstack1l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ੾"),
    bstack1l1l11_opy_
  )
def bstack1ll11ll_opy_():
  global CONFIG
  if bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ੿") in CONFIG and not bool(CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ઀")]):
    del CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪઁ")]
    return
  if not bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫં") in CONFIG:
    CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬઃ")] = bstack1l_opy_ (u"ࠫࠨࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧ઄")
  if bstack1l_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫઅ") in CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨઆ")]:
    bstack111llll1_opy_()
    os.environ[bstack1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫઇ")] = CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪઈ")]
  if not bstack1l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫઉ") in CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬઊ")]:
    return
  bstack111l111_opy_ = bstack1l_opy_ (u"ࠫࠬઋ")
  bstack1111l1l_opy_ = bstack111ll1ll_opy_()
  if bstack1111l1l_opy_ != -1:
    bstack111l111_opy_ = bstack1l_opy_ (u"ࠬࡉࡉࠡࠩઌ") + str(bstack1111l1l_opy_)
  if bstack111l111_opy_ == bstack1l_opy_ (u"࠭ࠧઍ"):
    bstack1lll1l111_opy_ = bstack111llll_opy_(CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ઎")])
    if bstack1lll1l111_opy_ != -1:
      bstack111l111_opy_ = str(bstack1lll1l111_opy_)
  if bstack111l111_opy_:
    bstack1ll1l1ll_opy_(bstack111l111_opy_)
    os.environ[bstack1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬએ")] = CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫઐ")]
def bstack1l111ll1_opy_(bstack1llllll_opy_, bstack1l1l1ll_opy_, path):
  bstack1llll1111_opy_ = {
    bstack1l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧઑ"): bstack1l1l1ll_opy_
  }
  if os.path.exists(path):
    bstack1llllll1l_opy_ = json.load(open(path, bstack1l_opy_ (u"ࠫࡷࡨࠧ઒")))
  else:
    bstack1llllll1l_opy_ = {}
  bstack1llllll1l_opy_[bstack1llllll_opy_] = bstack1llll1111_opy_
  with open(path, bstack1l_opy_ (u"ࠧࡽࠫࠣઓ")) as outfile:
    json.dump(bstack1llllll1l_opy_, outfile)
def bstack111llll_opy_(bstack1llllll_opy_):
  bstack1llllll_opy_ = str(bstack1llllll_opy_)
  bstack1l1l11l1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"࠭ࡾࠨઔ")), bstack1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧક"))
  try:
    if not os.path.exists(bstack1l1l11l1_opy_):
      os.makedirs(bstack1l1l11l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠨࢀࠪખ")), bstack1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩગ"), bstack1l_opy_ (u"ࠪ࠲ࡧࡻࡩ࡭ࡦ࠰ࡲࡦࡳࡥ࠮ࡥࡤࡧ࡭࡫࠮࡫ࡵࡲࡲࠬઘ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l_opy_ (u"ࠫࡼ࠭ઙ")):
        pass
      with open(file_path, bstack1l_opy_ (u"ࠧࡽࠫࠣચ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l_opy_ (u"࠭ࡲࠨછ")) as bstack1llllll11_opy_:
      bstack1l11l1ll_opy_ = json.load(bstack1llllll11_opy_)
    if bstack1llllll_opy_ in bstack1l11l1ll_opy_:
      bstack1lll11l1l_opy_ = bstack1l11l1ll_opy_[bstack1llllll_opy_][bstack1l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫજ")]
      bstack11ll1l11_opy_ = int(bstack1lll11l1l_opy_) + 1
      bstack1l111ll1_opy_(bstack1llllll_opy_, bstack11ll1l11_opy_, file_path)
      return bstack11ll1l11_opy_
    else:
      bstack1l111ll1_opy_(bstack1llllll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1llllll_opy_.format(str(e)))
    return -1
def bstack11111l11_opy_(config):
  if bstack1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪઝ") in config and config[bstack1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫઞ")] not in bstack1ll11ll1l_opy_:
    return config[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬટ")]
  elif bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬઠ") in os.environ:
    return os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ડ")]
  else:
    return None
def bstack11l111l_opy_(config):
  if not bstack11111l11_opy_(config) or not bstack1ll11l111_opy_(config):
    return True
  else:
    return False
def bstack1l1l1ll1l_opy_(config):
  if bstack1l11l_opy_() < version.parse(bstack1l_opy_ (u"࠭࠳࠯࠶࠱࠴ࠬઢ")):
    return False
  if bstack1l11l_opy_() >= version.parse(bstack1l_opy_ (u"ࠧ࠵࠰࠴࠲࠺࠭ણ")):
    return True
  if bstack1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨત") in config and config[bstack1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩથ")] == False:
    return False
  else:
    return True
def bstack11ll11ll_opy_(config, index = 0):
  global bstack1l111111_opy_
  bstack111l1l11_opy_ = {}
  caps = bstack1l1lll111_opy_ + bstack11111111_opy_
  if bstack1l111111_opy_:
    caps += bstack1l1lllll1_opy_
  for key in config:
    if key in caps + [bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭દ")]:
      continue
    bstack111l1l11_opy_[key] = config[key]
  if bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧધ") in config:
    for bstack1l11111_opy_ in config[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨન")][index]:
      if bstack1l11111_opy_ in caps + [bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ઩"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨપ")]:
        continue
      bstack111l1l11_opy_[bstack1l11111_opy_] = config[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫફ")][index][bstack1l11111_opy_]
  bstack111l1l11_opy_[bstack1l_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫબ")] = socket.gethostname()
  if bstack1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫભ") in bstack111l1l11_opy_:
    del(bstack111l1l11_opy_[bstack1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬમ")])
  return bstack111l1l11_opy_
def bstack1lll1llll_opy_(config):
  global bstack1l111111_opy_
  bstack11lll111_opy_ = {}
  caps = bstack11111111_opy_
  if bstack1l111111_opy_:
    caps+= bstack1l1lllll1_opy_
  for key in caps:
    if key in config:
      bstack11lll111_opy_[key] = config[key]
  return bstack11lll111_opy_
def bstack1l1lll11l_opy_(bstack111l1l11_opy_, bstack11lll111_opy_):
  bstack1111l11_opy_ = {}
  for key in bstack111l1l11_opy_.keys():
    if key in bstack11l111_opy_:
      bstack1111l11_opy_[bstack11l111_opy_[key]] = bstack111l1l11_opy_[key]
    else:
      bstack1111l11_opy_[key] = bstack111l1l11_opy_[key]
  for key in bstack11lll111_opy_:
    if key in bstack11l111_opy_:
      bstack1111l11_opy_[bstack11l111_opy_[key]] = bstack11lll111_opy_[key]
    else:
      bstack1111l11_opy_[key] = bstack11lll111_opy_[key]
  return bstack1111l11_opy_
def bstack11lllll1_opy_(config, index = 0):
  global bstack1l111111_opy_
  caps = {}
  bstack11lll111_opy_ = bstack1lll1llll_opy_(config)
  bstack1111l1_opy_ = bstack11111111_opy_
  bstack1111l1_opy_ += bstack1l1111ll_opy_
  if bstack1l111111_opy_:
    bstack1111l1_opy_ += bstack1l1lllll1_opy_
  if bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨય") in config:
    if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫર") in config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ઱")][index]:
      caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭લ")] = config[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬળ")][index][bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ઴")]
    if bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬવ") in config[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ")][index]:
      caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧષ")] = str(config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")][index][bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩહ")])
    bstack11111ll_opy_ = {}
    for bstack1ll1l1l1_opy_ in bstack1111l1_opy_:
      if bstack1ll1l1l1_opy_ in config[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ઺")][index]:
        if bstack1ll1l1l1_opy_ == bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ઻"):
          bstack11111ll_opy_[bstack1ll1l1l1_opy_] = str(config[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ઼ࠧ")][index][bstack1ll1l1l1_opy_] * 1.0)
        else:
          bstack11111ll_opy_[bstack1ll1l1l1_opy_] = config[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨઽ")][index][bstack1ll1l1l1_opy_]
        del(config[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩા")][index][bstack1ll1l1l1_opy_])
    bstack11lll111_opy_ = update(bstack11lll111_opy_, bstack11111ll_opy_)
  bstack111l1l11_opy_ = bstack11ll11ll_opy_(config, index)
  for bstack111lllll_opy_ in bstack11111111_opy_ + [bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬિ"), bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩી")]:
    if bstack111lllll_opy_ in bstack111l1l11_opy_:
      bstack11lll111_opy_[bstack111lllll_opy_] = bstack111l1l11_opy_[bstack111lllll_opy_]
      del(bstack111l1l11_opy_[bstack111lllll_opy_])
  if bstack1l1l1ll1l_opy_(config):
    bstack111l1l11_opy_[bstack1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩુ")] = True
    caps.update(bstack11lll111_opy_)
    caps[bstack1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫૂ")] = bstack111l1l11_opy_
  else:
    bstack111l1l11_opy_[bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫૃ")] = False
    caps.update(bstack1l1lll11l_opy_(bstack111l1l11_opy_, bstack11lll111_opy_))
    if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪૄ") in caps:
      caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧૅ")] = caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૆")]
      del(caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ે")])
    if bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪૈ") in caps:
      caps[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬૉ")] = caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ૊")]
      del(caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ો")])
  return caps
def bstack1llll_opy_():
  if bstack1l11l_opy_() <= version.parse(bstack1l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ૌ")):
    return bstack1l1l111l_opy_
  return bstack1111111l_opy_
def bstack1l1ll1l1_opy_(options):
  return hasattr(options, bstack1l_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ્"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11111l_opy_(options, bstack111l1l_opy_):
  for bstack1lll111ll_opy_ in bstack111l1l_opy_:
    if bstack1lll111ll_opy_ in [bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭૎"), bstack1l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭૏")]:
      next
    if bstack1lll111ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1lll111ll_opy_]= update(options._experimental_options[bstack1lll111ll_opy_], bstack111l1l_opy_[bstack1lll111ll_opy_])
    else:
      options.add_experimental_option(bstack1lll111ll_opy_, bstack111l1l_opy_[bstack1lll111ll_opy_])
  if bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨૐ") in bstack111l1l_opy_:
    for arg in bstack111l1l_opy_[bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ૑")]:
      options.add_argument(arg)
    del(bstack111l1l_opy_[bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪ૒")])
  if bstack1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ૓") in bstack111l1l_opy_:
    for ext in bstack111l1l_opy_[bstack1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ૔")]:
      options.add_extension(ext)
    del(bstack111l1l_opy_[bstack1l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ૕")])
def bstack1ll1ll1ll_opy_(options, bstack1lll111_opy_):
  if bstack1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ૖") in bstack1lll111_opy_:
    for bstack1l1l1l11_opy_ in bstack1lll111_opy_[bstack1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ૗")]:
      if bstack1l1l1l11_opy_ in options._preferences:
        options._preferences[bstack1l1l1l11_opy_] = update(options._preferences[bstack1l1l1l11_opy_], bstack1lll111_opy_[bstack1l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ૘")][bstack1l1l1l11_opy_])
      else:
        options.set_preference(bstack1l1l1l11_opy_, bstack1lll111_opy_[bstack1l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ૙")][bstack1l1l1l11_opy_])
  if bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ૚") in bstack1lll111_opy_:
    for arg in bstack1lll111_opy_[bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ૛")]:
      options.add_argument(arg)
def bstack11lll1l1_opy_(options, bstack1l11l1l_opy_):
  if bstack1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࠩ૜") in bstack1l11l1l_opy_:
    options.use_webview(bool(bstack1l11l1l_opy_[bstack1l_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪ૝")]))
  bstack11111l_opy_(options, bstack1l11l1l_opy_)
def bstack1ll1l11l_opy_(options, bstack1l1lll11_opy_):
  for bstack1ll111l1l_opy_ in bstack1l1lll11_opy_:
    if bstack1ll111l1l_opy_ in [bstack1l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ૞"), bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ૟")]:
      next
    options.set_capability(bstack1ll111l1l_opy_, bstack1l1lll11_opy_[bstack1ll111l1l_opy_])
  if bstack1l_opy_ (u"ࠬࡧࡲࡨࡵࠪૠ") in bstack1l1lll11_opy_:
    for arg in bstack1l1lll11_opy_[bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫૡ")]:
      options.add_argument(arg)
  if bstack1l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫૢ") in bstack1l1lll11_opy_:
    options.use_technology_preview(bool(bstack1l1lll11_opy_[bstack1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬૣ")]))
def bstack1l1ll_opy_(options, bstack1ll11_opy_):
  for bstack111l11ll_opy_ in bstack1ll11_opy_:
    if bstack111l11ll_opy_ in [bstack1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭૤"), bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ૥")]:
      next
    options._options[bstack111l11ll_opy_] = bstack1ll11_opy_[bstack111l11ll_opy_]
  if bstack1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ૦") in bstack1ll11_opy_:
    for bstack1ll1llll_opy_ in bstack1ll11_opy_[bstack1l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ૧")]:
      options.add_additional_option(
          bstack1ll1llll_opy_, bstack1ll11_opy_[bstack1l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ૨")][bstack1ll1llll_opy_])
  if bstack1l_opy_ (u"ࠧࡢࡴࡪࡷࠬ૩") in bstack1ll11_opy_:
    for arg in bstack1ll11_opy_[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭૪")]:
      options.add_argument(arg)
def bstack1l11lll1_opy_(options, caps):
  if not hasattr(options, bstack1l_opy_ (u"ࠩࡎࡉ࡞࠭૫")):
    return
  if options.KEY == bstack1l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ૬") and options.KEY in caps:
    bstack11111l_opy_(options, caps[bstack1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ૭")])
  elif options.KEY == bstack1l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪ૮") and options.KEY in caps:
    bstack1ll1ll1ll_opy_(options, caps[bstack1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ૯")])
  elif options.KEY == bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ૰") and options.KEY in caps:
    bstack1ll1l11l_opy_(options, caps[bstack1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ૱")])
  elif options.KEY == bstack1l_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ૲") and options.KEY in caps:
    bstack11lll1l1_opy_(options, caps[bstack1l_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ૳")])
  elif options.KEY == bstack1l_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ૴") and options.KEY in caps:
    bstack1l1ll_opy_(options, caps[bstack1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ૵")])
def bstack111111_opy_(caps):
  global bstack1l111111_opy_
  if bstack1l111111_opy_:
    if bstack1ll1ll_opy_() < version.parse(bstack1l_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬ૶")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ૷")
    if bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭૸") in caps:
      browser = caps[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧૹ")]
    elif bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫૺ") in caps:
      browser = caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬૻ")]
    browser = str(browser).lower()
    if browser == bstack1l_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬૼ") or browser == bstack1l_opy_ (u"࠭ࡩࡱࡣࡧࠫ૽"):
      browser = bstack1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧ૾")
    if browser == bstack1l_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩ૿"):
      browser = bstack1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ଀")
    if browser not in [bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪଁ"), bstack1l_opy_ (u"ࠫࡪࡪࡧࡦࠩଂ"), bstack1l_opy_ (u"ࠬ࡯ࡥࠨଃ"), bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭଄"), bstack1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨଅ")]:
      return None
    try:
      package = bstack1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪଆ").format(browser)
      name = bstack1l_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪଇ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1ll1l1_opy_(options):
        return None
      for bstack111lllll_opy_ in caps.keys():
        options.set_capability(bstack111lllll_opy_, caps[bstack111lllll_opy_])
      bstack1l11lll1_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1l1l_opy_(options, bstack1ll1lllll_opy_):
  if not bstack1l1ll1l1_opy_(options):
    return
  for bstack111lllll_opy_ in bstack1ll1lllll_opy_.keys():
    if bstack111lllll_opy_ in bstack1l1111ll_opy_:
      next
    if bstack111lllll_opy_ in options._caps and type(options._caps[bstack111lllll_opy_]) in [dict, list]:
      options._caps[bstack111lllll_opy_] = update(options._caps[bstack111lllll_opy_], bstack1ll1lllll_opy_[bstack111lllll_opy_])
    else:
      options.set_capability(bstack111lllll_opy_, bstack1ll1lllll_opy_[bstack111lllll_opy_])
  bstack1l11lll1_opy_(options, bstack1ll1lllll_opy_)
  if bstack1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩଈ") in options._caps:
    if options._caps[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଉ")] and options._caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଊ")].lower() != bstack1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧଋ"):
      del options._caps[bstack1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ଌ")]
def bstack11ll111_opy_(proxy_config):
  if bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ଍") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫ଎")] = proxy_config[bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧଏ")]
    del(proxy_config[bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨଐ")])
  if bstack1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ଑") in proxy_config and proxy_config[bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ଒")].lower() != bstack1l_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧଓ"):
    proxy_config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫଔ")] = bstack1l_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩକ")
  if bstack1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨଖ") in proxy_config:
    proxy_config[bstack1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧଗ")] = bstack1l_opy_ (u"ࠬࡶࡡࡤࠩଘ")
  return proxy_config
def bstack1llll11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬଙ") in config:
    return proxy
  config[bstack1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ଚ")] = bstack11ll111_opy_(config[bstack1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧଛ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨଜ")])
  return proxy
def bstack1l1l111_opy_(self):
  global CONFIG
  global bstack111l1_opy_
  if bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ଝ") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧଞ")]
  elif bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩଟ") in CONFIG:
    return CONFIG[bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪଠ")]
  else:
    return bstack111l1_opy_(self)
def bstack1111l_opy_():
  global CONFIG
  return bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪଡ") in CONFIG or bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬଢ") in CONFIG
def bstack11111l1_opy_(config):
  if not bstack1111l_opy_():
    return
  if config.get(bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬଣ")):
    return config.get(bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ତ"))
  if config.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨଥ")):
    return config.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩଦ"))
def bstack1l111ll_opy_():
  return bstack1111l_opy_() and bstack1l11l_opy_() >= version.parse(bstack1ll1l1l1l_opy_)
def bstack1ll1ll1l1_opy_(config):
  if bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪଧ") in config:
    if str(config[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫନ")]).lower() == bstack1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭଩"):
      return True
    else:
      return False
  elif bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧପ") in os.environ:
    if str(os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨଫ")]).lower() == bstack1l_opy_ (u"ࠫࡹࡸࡵࡦࠩବ"):
      return True
    else:
      return False
  else:
    return False
def bstack11ll111l_opy_(config):
  if bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩଭ") in config:
    return config[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪମ")]
  if bstack1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ଯ") in config:
    return config[bstack1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧର")]
  return {}
def bstack1ll1ll11_opy_(caps):
  global bstack1ll11l_opy_
  if bstack1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ଱") in caps:
    caps[bstack1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫଲ")][bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪଳ")] = True
    if bstack1ll11l_opy_:
      caps[bstack1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭଴")][bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨଵ")] = bstack1ll11l_opy_
  else:
    caps[bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬଶ")] = True
    if bstack1ll11l_opy_:
      caps[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଷ")] = bstack1ll11l_opy_
def bstack1ll11lll_opy_():
  global CONFIG
  if bstack1ll1ll1l1_opy_(CONFIG):
    bstack1lll11ll_opy_ = bstack11ll111l_opy_(CONFIG)
    bstack1lll1l_opy_(bstack1ll11l111_opy_(CONFIG), bstack1lll11ll_opy_)
def bstack1lll1l_opy_(key, bstack1lll11ll_opy_):
  global bstack1111l1ll_opy_
  logger.info(bstack11l11ll1_opy_)
  try:
    bstack1111l1ll_opy_ = Local()
    bstack1111ll11_opy_ = {bstack1l_opy_ (u"ࠩ࡮ࡩࡾ࠭ସ"): key}
    bstack1111ll11_opy_.update(bstack1lll11ll_opy_)
    logger.debug(bstack1ll1l1_opy_.format(str(bstack1111ll11_opy_)))
    bstack1111l1ll_opy_.start(**bstack1111ll11_opy_)
    if bstack1111l1ll_opy_.isRunning():
      logger.info(bstack111l1ll1_opy_)
  except Exception as e:
    bstack1lll11l_opy_(bstack1lll1l1l_opy_.format(str(e)))
def bstack1l1l11l1l_opy_():
  global bstack1111l1ll_opy_
  if bstack1111l1ll_opy_.isRunning():
    logger.info(bstack1ll1ll1l_opy_)
    bstack1111l1ll_opy_.stop()
  bstack1111l1ll_opy_ = None
def bstack1ll1111ll_opy_():
  global bstack1ll111lll_opy_
  if bstack1ll111lll_opy_:
    logger.warning(bstack1lllll11_opy_.format(str(bstack1ll111lll_opy_)))
  logger.info(bstack11llll_opy_)
  global bstack1111l1ll_opy_
  if bstack1111l1ll_opy_:
    bstack1l1l11l1l_opy_()
  logger.info(bstack11ll1111_opy_)
  bstack11ll1ll_opy_()
def bstack1lll1ll11_opy_(self, *args):
  logger.error(bstack1llllll1_opy_)
  bstack1ll1111ll_opy_()
  sys.exit(1)
def bstack1lll11l_opy_(err):
  logger.critical(bstack1ll1111l_opy_.format(str(err)))
  bstack11ll1ll_opy_(bstack1ll1111l_opy_.format(str(err)))
  atexit.unregister(bstack1ll1111ll_opy_)
  sys.exit(1)
def bstack1l11ll1l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11ll1ll_opy_(message)
  atexit.unregister(bstack1ll1111ll_opy_)
  sys.exit(1)
def bstack111lll11_opy_():
  global CONFIG
  CONFIG = bstack1lll1l1_opy_()
  CONFIG = bstack11lllll_opy_(CONFIG)
  CONFIG = bstack1l1lllll_opy_(CONFIG)
  if bstack11l111l_opy_(CONFIG):
    bstack1lll11l_opy_(bstack1lll1111_opy_)
  CONFIG[bstack1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬହ")] = bstack11111l11_opy_(CONFIG)
  CONFIG[bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ଺")] = bstack1ll11l111_opy_(CONFIG)
  if bstack1ll11llll_opy_(CONFIG):
    CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ଻")] = bstack1ll11llll_opy_(CONFIG)
    if not os.getenv(bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆ଼ࠩ")):
      if os.getenv(bstack1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫଽ")):
        CONFIG[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪା")] = os.getenv(bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ି"))
      else:
        bstack1ll11ll_opy_()
    else:
      if bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬୀ") in CONFIG:
        del(CONFIG[bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ୁ")])
  bstack1l1ll1_opy_()
  bstack111111l1_opy_()
  if bstack1l111111_opy_:
    CONFIG[bstack1l_opy_ (u"ࠬࡧࡰࡱࠩୂ")] = bstack111ll1_opy_(CONFIG)
    logger.info(bstack1l1ll11l_opy_.format(CONFIG[bstack1l_opy_ (u"࠭ࡡࡱࡲࠪୃ")]))
def bstack111111l1_opy_():
  global CONFIG
  global bstack1l111111_opy_
  if bstack1l_opy_ (u"ࠧࡢࡲࡳࠫୄ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack111l1111_opy_)
    bstack1l111111_opy_ = True
def bstack111ll1_opy_(config):
  bstack11lll1ll_opy_ = bstack1l_opy_ (u"ࠨࠩ୅")
  app = config[bstack1l_opy_ (u"ࠩࡤࡴࡵ࠭୆")]
  if isinstance(config[bstack1l_opy_ (u"ࠪࡥࡵࡶࠧେ")], str):
    if os.path.splitext(app)[1] in bstack1lllll1_opy_:
      if os.path.exists(app):
        bstack11lll1ll_opy_ = bstack1l1lll1l1_opy_(config, app)
      elif bstack11ll1_opy_(app):
        bstack11lll1ll_opy_ = app
      else:
        bstack1lll11l_opy_(bstack1l1lll1_opy_.format(app))
    else:
      if bstack11ll1_opy_(app):
        bstack11lll1ll_opy_ = app
      elif os.path.exists(app):
        bstack11lll1ll_opy_ = bstack1l1lll1l1_opy_(app)
      else:
        bstack1lll11l_opy_(bstack1lllll111_opy_)
  else:
    if len(app) > 2:
      bstack1lll11l_opy_(bstack1l1l1_opy_)
    elif len(app) == 2:
      if bstack1l_opy_ (u"ࠫࡵࡧࡴࡩࠩୈ") in app and bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ୉") in app:
        if os.path.exists(app[bstack1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ୊")]):
          bstack11lll1ll_opy_ = bstack1l1lll1l1_opy_(config, app[bstack1l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬୋ")], app[bstack1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫୌ")])
        else:
          bstack1lll11l_opy_(bstack1l1lll1_opy_.format(app))
      else:
        bstack1lll11l_opy_(bstack1l1l1_opy_)
    else:
      for key in app:
        if key in bstack1ll1l11ll_opy_:
          if key == bstack1l_opy_ (u"ࠩࡳࡥࡹ࡮୍ࠧ"):
            if os.path.exists(app[key]):
              bstack11lll1ll_opy_ = bstack1l1lll1l1_opy_(config, app[key])
            else:
              bstack1lll11l_opy_(bstack1l1lll1_opy_.format(app))
          else:
            bstack11lll1ll_opy_ = app[key]
        else:
          bstack1lll11l_opy_(bstack1l1ll11_opy_)
  return bstack11lll1ll_opy_
def bstack11ll1_opy_(bstack11lll1ll_opy_):
  import re
  bstack1ll11111l_opy_ = re.compile(bstack1l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ୎"))
  bstack1l111lll_opy_ = re.compile(bstack1l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ୏"))
  if bstack1l_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫ୐") in bstack11lll1ll_opy_ or re.fullmatch(bstack1ll11111l_opy_, bstack11lll1ll_opy_) or re.fullmatch(bstack1l111lll_opy_, bstack11lll1ll_opy_):
    return True
  else:
    return False
def bstack1l1lll1l1_opy_(config, path, bstack11l1lll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l_opy_ (u"࠭ࡲࡣࠩ୑")).read()).hexdigest()
  bstack11l1l111_opy_ = bstack1l1ll111_opy_(md5_hash)
  bstack11lll1ll_opy_ = None
  if bstack11l1l111_opy_:
    logger.info(bstack11l1l11l_opy_.format(bstack11l1l111_opy_, md5_hash))
    return bstack11l1l111_opy_
  bstack11llll1_opy_ = MultipartEncoder(
    fields={
        bstack1l_opy_ (u"ࠧࡧ࡫࡯ࡩࠬ୒"): (os.path.basename(path), open(os.path.abspath(path), bstack1l_opy_ (u"ࠨࡴࡥࠫ୓")), bstack1l_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭୔")),
        bstack1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭୕"): bstack11l1lll_opy_
    }
  )
  response = requests.post(bstack1ll1ll1_opy_, data=bstack11llll1_opy_,
                         headers={bstack1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪୖ"): bstack11llll1_opy_.content_type}, auth=(bstack11111l11_opy_(config), bstack1ll11l111_opy_(config)))
  try:
    res = json.loads(response.text)
    bstack11lll1ll_opy_ = res[bstack1l_opy_ (u"ࠬࡧࡰࡱࡡࡸࡶࡱ࠭ୗ")]
    logger.info(bstack1l1lll1ll_opy_.format(bstack11lll1ll_opy_))
    bstack111ll11_opy_(md5_hash, bstack11lll1ll_opy_)
  except ValueError as err:
    bstack1lll11l_opy_(bstack1lll1l11l_opy_.format(str(err)))
  return bstack11lll1ll_opy_
def bstack1l1ll1_opy_():
  global CONFIG
  global bstack1lllll1ll_opy_
  bstack1l1l1l1_opy_ = 1
  if bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭୘") in CONFIG:
    bstack1l1l1l1_opy_ = CONFIG[bstack1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ୙")]
  bstack1l11_opy_ = 0
  if bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୚") in CONFIG:
    bstack1l11_opy_ = len(CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୛")])
  bstack1lllll1ll_opy_ = int(bstack1l1l1l1_opy_) * int(bstack1l11_opy_)
def bstack1l1ll111_opy_(md5_hash):
  bstack1l1l11ll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠪࢂࠬଡ଼")), bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଢ଼"), bstack1l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭୞"))
  if os.path.exists(bstack1l1l11ll1_opy_):
    bstack1ll1l_opy_ = json.load(open(bstack1l1l11ll1_opy_,bstack1l_opy_ (u"࠭ࡲࡣࠩୟ")))
    if md5_hash in bstack1ll1l_opy_:
      bstack111ll111_opy_ = bstack1ll1l_opy_[md5_hash]
      bstack11lll1l_opy_ = datetime.datetime.now()
      bstack1l1ll1l11_opy_ = datetime.datetime.strptime(bstack111ll111_opy_[bstack1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪୠ")], bstack1l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬୡ"))
      if (bstack11lll1l_opy_ - bstack1l1ll1l11_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack111ll111_opy_[bstack1l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧୢ")]):
        return None
      return bstack111ll111_opy_[bstack1l_opy_ (u"ࠪ࡭ࡩ࠭ୣ")]
  else:
    return None
def bstack111ll11_opy_(md5_hash, bstack11lll1ll_opy_):
  bstack1l1l11l1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠫࢃ࠭୤")), bstack1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ୥"))
  if not os.path.exists(bstack1l1l11l1_opy_):
    os.makedirs(bstack1l1l11l1_opy_)
  bstack1l1l11ll1_opy_ = os.path.join(os.path.expanduser(bstack1l_opy_ (u"࠭ࡾࠨ୦")), bstack1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ୧"), bstack1l_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩ୨"))
  bstack1111ll1l_opy_ = {
    bstack1l_opy_ (u"ࠩ࡬ࡨࠬ୩"): bstack11lll1ll_opy_,
    bstack1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭୪"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨ୫")),
    bstack1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ୬"): str(__version__)
  }
  if os.path.exists(bstack1l1l11ll1_opy_):
    bstack1ll1l_opy_ = json.load(open(bstack1l1l11ll1_opy_,bstack1l_opy_ (u"࠭ࡲࡣࠩ୭")))
  else:
    bstack1ll1l_opy_ = {}
  bstack1ll1l_opy_[md5_hash] = bstack1111ll1l_opy_
  with open(bstack1l1l11ll1_opy_, bstack1l_opy_ (u"ࠢࡸ࠭ࠥ୮")) as outfile:
    json.dump(bstack1ll1l_opy_, outfile)
def bstack1l1llll_opy_(self):
  return
def bstack1ll111l11_opy_(self):
  return
def bstack1lll1l11_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1ll1ll111_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11lll11l_opy_
  global bstack1l1l11l_opy_
  global bstack1l1ll111l_opy_
  global bstack1l1ll1l1l_opy_
  global bstack11l11_opy_
  global bstack1lllll1l1_opy_
  global bstack1l11l111_opy_
  CONFIG[bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ୯")] = str(bstack11l11_opy_) + str(__version__)
  command_executor = bstack1llll_opy_()
  logger.debug(bstack11111l1l_opy_.format(command_executor))
  proxy = bstack1llll11_opy_(CONFIG, proxy)
  bstack11l11lll_opy_ = 0 if bstack1l1l11l_opy_ < 0 else bstack1l1l11l_opy_
  if bstack1l1ll1l1l_opy_ is True:
    bstack11l11lll_opy_ = int(threading.current_thread().getName())
  bstack1ll1lllll_opy_ = bstack11lllll1_opy_(CONFIG, bstack11l11lll_opy_)
  logger.debug(bstack1111l11l_opy_.format(str(bstack1ll1lllll_opy_)))
  if bstack1ll1ll1l1_opy_(CONFIG):
    bstack1ll1ll11_opy_(bstack1ll1lllll_opy_)
  if desired_capabilities:
    bstack1llll1ll1_opy_ = bstack11lllll1_opy_(bstack11lllll_opy_(desired_capabilities))
    if bstack1llll1ll1_opy_:
      bstack1ll1lllll_opy_ = update(bstack1llll1ll1_opy_, bstack1ll1lllll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1l1l_opy_(options, bstack1ll1lllll_opy_)
  if not options:
    options = bstack111111_opy_(bstack1ll1lllll_opy_)
  if options and bstack1l11l_opy_() >= version.parse(bstack1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ୰")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1l11l_opy_() < version.parse(bstack1l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩୱ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll1lllll_opy_)
  logger.info(bstack1l1ll1111_opy_)
  if bstack1l11l_opy_() >= version.parse(bstack1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪ୲")):
    bstack1lllll1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11l_opy_() >= version.parse(bstack1l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ୳")):
    bstack1lllll1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lllll1l1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack11lll11l_opy_ = self.session_id
  if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୴") in CONFIG and bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ୵") in CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୶")][bstack11l11lll_opy_]:
    bstack1l1ll111l_opy_ = CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୷")][bstack11l11lll_opy_][bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୸")]
  logger.debug(bstack11l1l_opy_.format(bstack11lll11l_opy_))
try:
  from playwright._impl._api_structures import (
      ProxySettings,
  )
  from playwright._impl._helper import (
      Env,
  )
  import pathlib
  from pathlib import Path
  from typing import Dict, List, Union
  def bstack1ll1l111l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11lll11l_opy_
    global bstack1l1l11l_opy_
    global bstack1l1ll111l_opy_
    global bstack1l1ll1l1l_opy_
    global bstack11l11_opy_
    global bstack1lllll1l1_opy_
    CONFIG[bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭୹")] = str(bstack11l11_opy_) + str(__version__)
    bstack11l11lll_opy_ = 0 if bstack1l1l11l_opy_ < 0 else bstack1l1l11l_opy_
    if bstack1l1ll1l1l_opy_ is True:
      bstack11l11lll_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1l_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧ୺")] = False
    bstack1ll1lllll_opy_ = bstack11lllll1_opy_(CONFIG, bstack11l11lll_opy_)
    logger.debug(bstack1111l11l_opy_.format(str(bstack1ll1lllll_opy_)))
    if bstack1ll1ll1l1_opy_(CONFIG):
      bstack1ll1ll11_opy_(bstack1ll1lllll_opy_)
    if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୻") in CONFIG and bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ୼") in CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ୽")][bstack11l11lll_opy_]:
      bstack1l1ll111l_opy_ = CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ୾")][bstack11l11lll_opy_][bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୿")]
    import urllib
    import json
    bstack111l1lll_opy_ = bstack1l_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭஀") + urllib.parse.quote(json.dumps(bstack1ll1lllll_opy_))
    browser = self.connect(bstack111l1lll_opy_)
    return browser
  try:
    import Browser
    from subprocess import Popen
    bstack111l111l_opy_ = Popen.__init__
    def bstack1llll111_opy_(self, args, bufsize=-1, executable=None,
                 stdin=None, stdout=None, stderr=None,
                 preexec_fn=None, close_fds=True,
                 shell=False, cwd=None, env=None, universal_newlines=None,
                 startupinfo=None, creationflags=0,
                 restore_signals=True, start_new_session=False,
                 pass_fds=(), *, user=None, group=None, extra_groups=None,
                 encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      if(bstack1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ஁") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"࠭ࡾࠨஂ")), bstack1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧஃ"), bstack1l_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪ஄")), bstack1l_opy_ (u"ࠩࡺࠫஅ")) as fp:
          fp.write(bstack1l_opy_ (u"ࠥࠦஆ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨஇ")))):
          with open(args[1], bstack1l_opy_ (u"ࠬࡸࠧஈ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠬஉ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11l1_opy_)
            lines.insert(1, bstack11l1ll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤஊ")), bstack1l_opy_ (u"ࠨࡹࠪ஋")) as bstack1lllll_opy_:
              bstack1lllll_opy_.writelines(lines)
        CONFIG[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ஌")] = str(bstack11l11_opy_) + str(__version__)
        bstack11l11lll_opy_ = 0 if bstack1l1l11l_opy_ < 0 else bstack1l1l11l_opy_
        if bstack1l1ll1l1l_opy_ is True:
          bstack11l11lll_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1l_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ஍")] = False
        bstack1ll1lllll_opy_ = bstack11lllll1_opy_(CONFIG, bstack11l11lll_opy_)
        logger.debug(bstack1111l11l_opy_.format(str(bstack1ll1lllll_opy_)))
        if bstack1ll1ll1l1_opy_(CONFIG):
          bstack1ll1ll11_opy_(bstack1ll1lllll_opy_)
        if bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஎ") in CONFIG and bstack1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪஏ") in CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩஐ")][bstack11l11lll_opy_]:
          bstack1l1ll111l_opy_ = CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ஑")][bstack11l11lll_opy_][bstack1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ஒ")]
        args.append(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠩࢁࠫஓ")), bstack1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪஔ"), bstack1l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭க")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll1lllll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ஖"))
      return bstack111l111l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
except Exception as e:
    logger.debug(bstack111lll1l_opy_)
def bstack1l111l_opy_():
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1l111l_opy_
    except Exception as e:
        logger.debug(bstack111lll1l_opy_)
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1llll111_opy_
    except:
      pass
def bstack1llll1ll_opy_(context, bstack1l1l1ll1_opy_):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ஗"), bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ஘")+ json.dumps(bstack1l1l1ll1_opy_) + bstack1l_opy_ (u"ࠣࡿࢀࠦங"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢச"), e)
def bstack1l111l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ஛"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩஜ") + json.dumps(message) + bstack1l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨ஝") + json.dumps(level) + bstack1l_opy_ (u"࠭ࡽࡾࠩஞ"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥட"), e)
def bstack1111lll_opy_(context, status, message = bstack1l_opy_ (u"ࠣࠤ஠")):
  try:
    if(status == bstack1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ஡")):
      context.page.evaluate(bstack1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ஢"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠬண") + json.dumps(bstack1l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦࠢத") + str(message)) + bstack1l_opy_ (u"࠭ࠬࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪ஥") + json.dumps(status) + bstack1l_opy_ (u"ࠢࡾࡿࠥ஦"))
    else:
      context.page.evaluate(bstack1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ஧"), bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪந") + json.dumps(status) + bstack1l_opy_ (u"ࠥࢁࢂࠨன"))
  except Exception as e:
    logger.debug(bstack1l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣப"), e)
def bstack1l111l11_opy_(self, url):
  global bstack111ll11l_opy_
  try:
    bstack11l1l1l1_opy_(url)
  except Exception as err:
    logger.debug(bstack1111ll1_opy_.format(str(err)))
  bstack111ll11l_opy_(self, url)
def bstack1ll11ll11_opy_(self, test):
  global CONFIG
  global bstack11lll11l_opy_
  global bstack11l1ll_opy_
  global bstack1l1ll111l_opy_
  global bstack11lll_opy_
  try:
    if not bstack11lll11l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l_opy_ (u"ࠬࢄࠧ஫")), bstack1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭஬"), bstack1l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ஭"))) as f:
        bstack1l1l1lll_opy_ = json.loads(bstack1l_opy_ (u"ࠣࡽࠥம") + f.read().strip() + bstack1l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫய") + bstack1l_opy_ (u"ࠥࢁࠧர"))
        bstack11lll11l_opy_ = bstack1l1l1lll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11lll11l_opy_:
    try:
      data = {}
      bstack1ll111ll1_opy_ = None
      if test:
        bstack1ll111ll1_opy_ = str(test.data)
      if bstack1ll111ll1_opy_ and not bstack1l1ll111l_opy_:
        data[bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩற")] = bstack1ll111ll1_opy_
      if bstack11l1ll_opy_:
        if bstack11l1ll_opy_.status == bstack1l_opy_ (u"ࠬࡖࡁࡔࡕࠪல"):
          data[bstack1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ள")] = bstack1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧழ")
        elif bstack11l1ll_opy_.status == bstack1l_opy_ (u"ࠨࡈࡄࡍࡑ࠭வ"):
          data[bstack1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩஶ")] = bstack1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪஷ")
          if bstack11l1ll_opy_.message:
            data[bstack1l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫஸ")] = str(bstack11l1ll_opy_.message)
      user = CONFIG[bstack1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧஹ")]
      key = CONFIG[bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ஺")]
      url = bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡢࡲ࡬࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠳ࢀࢃ࠮࡫ࡵࡲࡲࠬ஻").format(user, key, bstack11lll11l_opy_)
      headers = {
        bstack1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ஼"): bstack1l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ஽"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1lll1lll_opy_.format(str(e)))
  bstack11lll_opy_(self, test)
def bstack1ll1l1l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll11l_opy_
  bstack1llll11l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1ll_opy_
  bstack11l1ll_opy_ = self._test
def bstack1ll11l1l1_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1l_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶࠥா"), bstack1l_opy_ (u"ࠦࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠣி"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1l_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࡩ࡯ࡲࠣீ"), bstack1l_opy_ (u"ࠨ࠮ࠣு")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1l_opy_ (u"ࠢࠫ࠰ࡻࡱࡱࠨூ"))))
  if not files:
    pabot._write(bstack1l_opy_ (u"ࠨ࡙ࡄࡖࡓࡀࠠࡏࡱࠣࡳࡺࡺࡰࡶࡶࠣࡪ࡮ࡲࡥࡴࠢ࡬ࡲࠥࠨࠥࡴࠤࠪ௃") % outs_dir, pabot.Color.YELLOW)
    return bstack1l_opy_ (u"ࠤࠥ௄")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1ll111111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢ௅") in options:
    del options[bstack1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣெ")]
  if ROBOT_VERSION < bstack1l_opy_ (u"ࠧ࠺࠮࠱ࠤே"):
    stats = {
      bstack1l_opy_ (u"ࠨࡣࡳ࡫ࡷ࡭ࡨࡧ࡬ࠣை"): {bstack1l_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨ௉"): 0, bstack1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣொ"): 0, bstack1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤோ"): 0},
      bstack1l_opy_ (u"ࠥࡥࡱࡲࠢௌ"): {bstack1l_opy_ (u"ࠦࡹࡵࡴࡢ࡮்ࠥ"): 0, bstack1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ௎"): 0, bstack1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ௏"): 0},
    }
  else:
    stats = {
      bstack1l_opy_ (u"ࠢࡵࡱࡷࡥࡱࠨௐ"): 0,
      bstack1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ௑"): 0,
      bstack1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ௒"): 0,
      bstack1l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦ௓"): 0,
    }
  if pabot_args[bstack1l_opy_ (u"ࠦࡇ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑࡥࡒࡖࡐࠥ௔")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1l_opy_ (u"ࠧࡈࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒ࡟ࡓࡗࡑࠦ௕")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1l_opy_ (u"ࠨࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠤ௖")], pabot_args[bstack1l_opy_ (u"ࠢࡢࡴࡷ࡭࡫ࡧࡣࡵࡵ࡬ࡲࡸࡻࡢࡧࡱ࡯ࡨࡪࡸࡳࠣௗ")]
      )
      outputs += [
        bstack1ll11l1l1_opy_(
          os.path.join(outs_dir, str(index)+ bstack1l_opy_ (u"ࠣ࠱ࠥ௘")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1l_opy_ (u"ࠤࡳࡥࡧࡵࡴࡠࡴࡨࡷࡺࡲࡴࡴࠤ௙"), bstack1l_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶࠨࡷ࠳ࡾ࡭࡭ࠤ௚") % index),
        )
      ]
    if bstack1l_opy_ (u"ࠦࡴࡻࡴࡱࡷࡷࠦ௛") not in options:
      options[bstack1l_opy_ (u"ࠧࡵࡵࡵࡲࡸࡸࠧ௜")] = bstack1l_opy_ (u"ࠨ࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠥ௝")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll11lll1_opy_(self, ff_profile_dir):
  global bstack111l11_opy_
  if not ff_profile_dir:
    return None
  return bstack111l11_opy_(self, ff_profile_dir)
def bstack11l1111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll11l_opy_
  bstack1lll11lll_opy_ = []
  if bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௞") in CONFIG:
    bstack1lll11lll_opy_ = CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௟")]
  bstack111111ll_opy_ = len(suite_group) * len(pabot_args[bstack1l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤ௠")] or [(bstack1l_opy_ (u"ࠥࠦ௡"), None)]) * len(bstack1lll11lll_opy_)
  pabot_args[bstack1l_opy_ (u"ࠦࡇ࡙ࡔࡂࡅࡎࡣࡕࡇࡒࡂࡎࡏࡉࡑࡥࡒࡖࡐࠥ௢")] = []
  for q in range(bstack111111ll_opy_):
    pabot_args[bstack1l_opy_ (u"ࠧࡈࡓࡕࡃࡆࡏࡤࡖࡁࡓࡃࡏࡐࡊࡒ࡟ࡓࡗࡑࠦ௣")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢ௤")],
      pabot_args[bstack1l_opy_ (u"ࠢࡷࡧࡵࡦࡴࡹࡥࠣ௥")],
      argfile,
      pabot_args.get(bstack1l_opy_ (u"ࠣࡪ࡬ࡺࡪࠨ௦")),
      pabot_args[bstack1l_opy_ (u"ࠤࡳࡶࡴࡩࡥࡴࡵࡨࡷࠧ௧")],
      platform[0],
      bstack1ll11l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࡫࡯࡬ࡦࡵࠥ௨")] or [(bstack1l_opy_ (u"ࠦࠧ௩"), None)]
    for platform in enumerate(bstack1lll11lll_opy_)
  ]
def bstack1l1llll1_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1l1l1ll11_opy_=bstack1l_opy_ (u"ࠬ࠭௪")):
  global bstack11ll_opy_
  self.platform_index = platform_index
  self.bstack1ll1lll11_opy_ = bstack1l1l1ll11_opy_
  bstack11ll_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1l1llll11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll11l11l_opy_
  global bstack1lll1l1ll_opy_
  if not bstack1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௫") in item.options:
    item.options[bstack1l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ௬")] = []
  for v in item.options[bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ௭")]:
    if bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ௮") in v:
      item.options[bstack1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௯")].remove(v)
  item.options[bstack1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௰")].insert(0, bstack1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧ௱").format(item.platform_index))
  item.options[bstack1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௲")].insert(0, bstack1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࠾ࢀࢃࠧ௳").format(item.bstack1ll1lll11_opy_))
  if bstack1lll1l1ll_opy_:
    item.options[bstack1l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ௴")].insert(0, bstack1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡒࡒࡋࡏࡇࡇࡋࡏࡉ࠿ࢁࡽࠨ௵").format(bstack1lll1l1ll_opy_))
  return bstack1ll11l11l_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11111_opy_(command):
  global bstack1lll1l1ll_opy_
  if bstack1lll1l1ll_opy_:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ௶"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠥ࠭௷") + bstack1lll1l1ll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௸"), bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௹"), 1)
def bstack1llll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1111_opy_
  bstack11111_opy_(command)
  return bstack1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll11l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1111_opy_
  bstack11111_opy_(command)
  return bstack1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1111ll_opy_(self, runner, quiet=False, capture=True):
  global bstack1llll1l_opy_
  bstack1lll1ll1_opy_ = bstack1llll1l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ௺")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ௻")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1ll1_opy_
def bstack1l1ll1lll_opy_(self, name, context, *args):
  global bstack11l11l11_opy_
  if name in [bstack1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ௼"), bstack1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ௽")]:
    bstack11l11l11_opy_(self, name, context, *args)
  if name == bstack1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ௾"):
    try:
      bstack1l1l1ll1_opy_ = str(self.feature.name)
      bstack1llll1ll_opy_(context, bstack1l1l1ll1_opy_)
      context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ௿") + json.dumps(bstack1l1l1ll1_opy_) + bstack1l_opy_ (u"࠭ࡽࡾࠩఀ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧఁ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪం"):
    try:
      if not hasattr(self, bstack1l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫః")):
        self.driver_before_scenario = True
      bstack1lll1111l_opy_ = args[0].name
      bstack1l11l11_opy_ = bstack1l1l1ll1_opy_ = str(self.feature.name)
      bstack1l1l1ll1_opy_ = bstack1l11l11_opy_ + bstack1l_opy_ (u"ࠪࠤ࠲ࠦࠧఄ") + bstack1lll1111l_opy_
      if self.driver_before_scenario:
        bstack1llll1ll_opy_(context, bstack1l1l1ll1_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩఅ") + json.dumps(bstack1l1l1ll1_opy_) + bstack1l_opy_ (u"ࠬࢃࡽࠨఆ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧఇ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨఈ"):
    try:
      bstack11l1l1_opy_ = args[0].status.name
      if str(bstack11l1l1_opy_).lower() == bstack1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨఉ"):
        bstack1ll11l1ll_opy_ = bstack1l_opy_ (u"ࠩࠪఊ")
        bstack11llll11_opy_ = bstack1l_opy_ (u"ࠪࠫఋ")
        bstack1llllllll_opy_ = bstack1l_opy_ (u"ࠫࠬఌ")
        try:
          import traceback
          bstack1ll11l1ll_opy_ = self.exception.__class__.__name__
          bstack1ll111_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11llll11_opy_ = bstack1l_opy_ (u"ࠬࠦࠧ఍").join(bstack1ll111_opy_)
          bstack1llllllll_opy_ = bstack1ll111_opy_[-1]
        except Exception as e:
          logger.debug(bstack11ll1l_opy_.format(str(e)))
        bstack1ll11l1ll_opy_ += bstack1llllllll_opy_
        bstack1l111l1l_opy_(context, json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧఎ") + str(bstack11llll11_opy_)), bstack1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨఏ"))
        if self.driver_before_scenario:
          bstack1111lll_opy_(context, bstack1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣఐ"), bstack1ll11l1ll_opy_)
        context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ఑") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤఒ") + str(bstack11llll11_opy_)) + bstack1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫఓ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬఔ") + json.dumps(bstack1l_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥక") + str(bstack1ll11l1ll_opy_)) + bstack1l_opy_ (u"ࠧࡾࡿࠪఖ"))
      else:
        bstack1l111l1l_opy_(context, bstack1l_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤగ"), bstack1l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢఘ"))
        if self.driver_before_scenario:
          bstack1111lll_opy_(context, bstack1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥఙ"))
        context.browser.execute_script(bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩచ") + json.dumps(str(args[0].name) + bstack1l_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤఛ")) + bstack1l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬజ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡲࡤࡷࡸ࡫ࡤࠣࡿࢀࠫఝ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪఞ").format(str(e)))
  if name == bstack1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩట"):
    try:
      if context.failed is True:
        bstack111111l_opy_ = []
        bstack1l1lll_opy_ = []
        bstack1111111_opy_ = []
        bstack111l1ll_opy_ = bstack1l_opy_ (u"ࠪࠫఠ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack111111l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll111_opy_ = traceback.format_tb(exc_tb)
            bstack1l1ll11l1_opy_ = bstack1l_opy_ (u"ࠫࠥ࠭డ").join(bstack1ll111_opy_)
            bstack1l1lll_opy_.append(bstack1l1ll11l1_opy_)
            bstack1111111_opy_.append(bstack1ll111_opy_[-1])
        except Exception as e:
          logger.debug(bstack11ll1l_opy_.format(str(e)))
        bstack1ll11l1ll_opy_ = bstack1l_opy_ (u"ࠬ࠭ఢ")
        for i in range(len(bstack111111l_opy_)):
          bstack1ll11l1ll_opy_ += bstack111111l_opy_[i] + bstack1111111_opy_[i] + bstack1l_opy_ (u"࠭࡜࡯ࠩణ")
        bstack111l1ll_opy_ = bstack1l_opy_ (u"ࠧࠡࠩత").join(bstack1l1lll_opy_)
        if not self.driver_before_scenario:
          bstack1l111l1l_opy_(context, bstack111l1ll_opy_, bstack1l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢథ"))
          bstack1111lll_opy_(context, bstack1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤద"), bstack1ll11l1ll_opy_)
          context.browser.execute_script(bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨధ") + json.dumps(bstack111l1ll_opy_) + bstack1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫన"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬ఩") + json.dumps(bstack1l_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦప") + str(bstack1ll11l1ll_opy_)) + bstack1l_opy_ (u"ࠧࡾࡿࠪఫ"))
      else:
        if not self.driver_before_scenario:
          bstack1l111l1l_opy_(context, bstack1l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦబ") + str(self.feature.name) + bstack1l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦభ"), bstack1l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣమ"))
          bstack1111lll_opy_(context, bstack1l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦయ"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪర") + json.dumps(bstack1l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤఱ") + str(self.feature.name) + bstack1l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤల")) + bstack1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧళ"))
          context.browser.execute_script(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡴࡦࡹࡳࡦࡦࠥࢁࢂ࠭ఴ"))
    except Exception as e:
      logger.debug(bstack1l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬవ").format(str(e)))
  if name in [bstack1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫశ"), bstack1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ష")]:
    bstack11l11l11_opy_(self, name, context, *args)
def bstack1ll1lll1l_opy_(bstack1lll11l1_opy_):
  global bstack11l11_opy_
  bstack11l11_opy_ = bstack1lll11l1_opy_
  logger.info(bstack1lll1ll1l_opy_.format(bstack11l11_opy_.split(bstack1l_opy_ (u"࠭࠭ࠨస"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack1l1lll1l_opy_ + str(e))
  Service.start = bstack1l1llll_opy_
  Service.stop = bstack1ll111l11_opy_
  webdriver.Remote.__init__ = bstack1ll1ll111_opy_
  webdriver.Remote.get = bstack1l111l11_opy_
  WebDriver.close = bstack1lll1l11_opy_
  bstack1l111l_opy_()
  if bstack1l111ll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1l111_opy_
    except Exception as e:
      logger.error(bstack1lll111l_opy_.format(str(e)))
  if (bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭హ") in str(bstack1lll11l1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll11lll1_opy_
      except Exception as e:
        logger.warn(bstack1l11llll_opy_ + str(e))
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack1l11llll_opy_)
    Output.end_test = bstack1ll11ll11_opy_
    TestStatus.__init__ = bstack1ll1l1l11_opy_
    QueueItem.__init__ = bstack1l1llll1_opy_
    pabot._create_items = bstack11l1111_opy_
    try:
      from pabot import __version__ as bstack1l1l1l111_opy_
      if version.parse(bstack1l1l1l111_opy_) >= version.parse(bstack1l_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨ఺")):
        pabot._run = bstack1ll11l1l_opy_
      else:
        pabot._run = bstack1llll1l1_opy_
    except Exception as e:
      pabot._run = bstack1llll1l1_opy_
    pabot._create_command_for_execution = bstack1l1llll11_opy_
    pabot._report_results = bstack1ll111111_opy_
  if bstack1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ఻") in str(bstack1lll11l1_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack111l11l1_opy_)
    Runner.run_hook = bstack1l1ll1lll_opy_
    Step.run = bstack1111ll_opy_
def bstack1l11ll11_opy_():
  global CONFIG
  if bstack1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯఼ࠪ") in CONFIG and int(CONFIG[bstack1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫఽ")]) > 1:
    logger.warn(bstack1l11l11l_opy_)
def bstack1ll1lll_opy_(bstack1l1l1l1l_opy_, index):
  bstack1ll1lll1l_opy_(bstack1l11l1l1_opy_)
  exec(open(bstack1l1l1l1l_opy_).read())
def bstack1llll111l_opy_(arg):
  global CONFIG
  bstack1ll1lll1l_opy_(bstack1ll111l_opy_)
  os.environ[bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ా")] = CONFIG[bstack1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨి")]
  os.environ[bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪీ")] = CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫు")]
  from _pytest.config import main as bstack11l1lll1_opy_
  bstack11l1lll1_opy_(arg)
def bstack11l1llll_opy_(arg):
  bstack1ll1lll1l_opy_(bstack11ll11_opy_)
  from behave.__main__ import main as bstack1ll11ll1_opy_
  bstack1ll11ll1_opy_(arg)
def bstack1ll1l111_opy_():
  logger.info(bstack111lll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨూ"), help=bstack1l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫృ"))
  parser.add_argument(bstack1l_opy_ (u"ࠫ࠲ࡻࠧౄ"), bstack1l_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ౅"), help=bstack1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬె"))
  parser.add_argument(bstack1l_opy_ (u"ࠧ࠮࡭ࠪే"), bstack1l_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧై"), help=bstack1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ౉"))
  parser.add_argument(bstack1l_opy_ (u"ࠪ࠱࡫࠭ొ"), bstack1l_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩో"), help=bstack1l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫౌ"))
  bstack1l1l11ll_opy_ = parser.parse_args()
  try:
    bstack11111lll_opy_ = bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧ్ࠪ")
    if bstack1l1l11ll_opy_.framework and bstack1l1l11ll_opy_.framework not in (bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౎"), bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ౏")):
      bstack11111lll_opy_ = bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ౐")
    bstack11ll1ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11111lll_opy_)
    bstack1lllll1l_opy_ = open(bstack11ll1ll1_opy_, bstack1l_opy_ (u"ࠪࡶࠬ౑"))
    bstack1l11ll_opy_ = bstack1lllll1l_opy_.read()
    bstack1lllll1l_opy_.close()
    if bstack1l1l11ll_opy_.username:
      bstack1l11ll_opy_ = bstack1l11ll_opy_.replace(bstack1l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫ౒"), bstack1l1l11ll_opy_.username)
    if bstack1l1l11ll_opy_.key:
      bstack1l11ll_opy_ = bstack1l11ll_opy_.replace(bstack1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ౓"), bstack1l1l11ll_opy_.key)
    if bstack1l1l11ll_opy_.framework:
      bstack1l11ll_opy_ = bstack1l11ll_opy_.replace(bstack1l_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ౔"), bstack1l1l11ll_opy_.framework)
    file_name = bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ౕࠪ")
    file_path = os.path.abspath(file_name)
    bstack1l111_opy_ = open(file_path, bstack1l_opy_ (u"ࠨࡹౖࠪ"))
    bstack1l111_opy_.write(bstack1l11ll_opy_)
    bstack1l111_opy_.close()
    logger.info(bstack11ll1l1l_opy_)
    try:
      os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ౗")] = bstack1l1l11ll_opy_.framework if bstack1l1l11ll_opy_.framework != None else bstack1l_opy_ (u"ࠥࠦౘ")
      config = yaml.safe_load(bstack1l11ll_opy_)
      config[bstack1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫౙ")] = bstack1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫౚ")
      bstack1lll11111_opy_(bstack11lll1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1l1lll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11ll1l1_opy_.format(str(e)))
def bstack1lll11111_opy_(bstack11l1l1l_opy_, config, bstack1ll1111_opy_ = {}):
  global bstack1l1ll1ll1_opy_
  if not config:
    return
  bstack1llll1_opy_ = bstack1lll1_opy_ if not bstack1l1ll1ll1_opy_ else ( bstack1ll11l11_opy_ if bstack1l_opy_ (u"࠭ࡡࡱࡲࠪ౛") in config else bstack1ll1ll11l_opy_ )
  data = {
    bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ౜"): bstack11111l11_opy_(config),
    bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫౝ"): bstack1ll11l111_opy_(config),
    bstack1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭౞"): bstack11l1l1l_opy_,
    bstack1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭౟"): {
      bstack1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩౠ"): str(config[bstack1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬౡ")]) if bstack1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ౢ") in config else bstack1l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣౣ"),
      bstack1l_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪ౤"): bstack11ll1lll_opy_(os.getenv(bstack1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦ౥"), bstack1l_opy_ (u"ࠥࠦ౦"))),
      bstack1l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭౧"): bstack1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ౨"),
      bstack1l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧ౩"): bstack1llll1_opy_,
      bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ౪"): config[bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ౫")] if bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ౬") in config else bstack1l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ౭"),
      bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭౮"): str(config[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ౯")]) if bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ౰") in config else bstack1l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣ౱"),
      bstack1l_opy_ (u"ࠨࡱࡶࠫ౲"): sys.platform,
      bstack1l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ౳"): socket.gethostname()
    }
  }
  update(data[bstack1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭౴")], bstack1ll1111_opy_)
  try:
    response = bstack11l1l11_opy_(bstack1l_opy_ (u"ࠫࡕࡕࡓࡕࠩ౵"), bstack111lll1_opy_, data, config)
    if response:
      logger.debug(bstack111ll1l_opy_.format(bstack11l1l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack111l1l1_opy_.format(str(e)))
def bstack11l1l11_opy_(type, url, data, config):
  bstack1llll1l1l_opy_ = bstack1ll1l1l_opy_.format(url)
  proxy = bstack11111l1_opy_(config)
  proxies = {}
  response = {}
  if config.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ౶")):
    proxies = {
      bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ౷"): proxy
    }
  if config.get(bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ౸")):
    proxies = {
      bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ౹"): proxy
    }
  if type == bstack1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ౺"):
    response = requests.post(bstack1llll1l1l_opy_, json=data,
                    headers={bstack1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ౻"): bstack1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ౼")}, auth=(bstack11111l11_opy_(config), bstack1ll11l111_opy_(config)), proxies=proxies)
  return response
def bstack11ll1lll_opy_(framework):
  return bstack1l_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤ౽").format(str(framework), __version__) if framework else bstack1l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ౾").format(__version__)
def bstack1ll1111l1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack111lll11_opy_()
  logger.debug(bstack11l11111_opy_.format(str(CONFIG)))
  bstack1111l1l1_opy_()
  sys.excepthook = bstack1111llll_opy_
  atexit.register(bstack1ll1111ll_opy_)
  signal.signal(signal.SIGINT, bstack1lll1ll11_opy_)
  signal.signal(signal.SIGTERM, bstack1lll1ll11_opy_)
def bstack1111llll_opy_(exctype, value, traceback):
  bstack11ll1ll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
def bstack11ll1ll_opy_(message = bstack1l_opy_ (u"ࠧࠨ౿")):
  global CONFIG
  try:
    if message:
      bstack1ll1111_opy_ = {
        bstack1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧಀ"): message
      }
      bstack1lll11111_opy_(bstack111ll_opy_, CONFIG, bstack1ll1111_opy_)
    else:
      bstack1lll11111_opy_(bstack111ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1l1l1ll_opy_.format(str(e)))
def bstack1l1111l_opy_(bstack11ll11l1_opy_, size):
  bstack1lll11ll1_opy_ = []
  while len(bstack11ll11l1_opy_) > size:
    bstack1ll1llll1_opy_ = bstack11ll11l1_opy_[:size]
    bstack1lll11ll1_opy_.append(bstack1ll1llll1_opy_)
    bstack11ll11l1_opy_   = bstack11ll11l1_opy_[size:]
  bstack1lll11ll1_opy_.append(bstack11ll11l1_opy_)
  return bstack1lll11ll1_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1111_opy_)
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠩ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬಁ")  or sys.argv[1] == bstack1l_opy_ (u"ࠪ࠱ࡻ࠭ಂ"):
    logger.info(bstack1l_opy_ (u"ࠫࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡔࡾࡺࡨࡰࡰࠣࡗࡉࡑࠠࡷࡽࢀࠫಃ").format(__version__))
    return
  if sys.argv[1] == bstack1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ಄"):
    bstack1ll1l111_opy_()
    return
  args = sys.argv
  bstack1ll1111l1_opy_()
  global CONFIG
  global bstack1lllll1ll_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1l1l11l_opy_
  global bstack1ll11l_opy_
  global bstack1lll1l1ll_opy_
  bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"࠭ࠧಅ")
  if args[1] == bstack1l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧಆ") or args[1] == bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩಇ"):
    bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩಈ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩಉ"):
    bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪಊ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫಋ"):
    bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬಌ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ಍"):
    bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩಎ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಏ"):
    bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪಐ")
    args = args[2:]
  elif args[1] == bstack1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ಑"):
    bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬಒ")
    args = args[2:]
  else:
    if not bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಓ") in CONFIG or str(CONFIG[bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪಔ")]).lower() in [bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨಕ"), bstack1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪಖ")]:
      bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪಗ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧಘ")]).lower() == bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫಙ"):
      bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬಚ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪಛ")]).lower() == bstack1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧಜ"):
      bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨಝ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಞ")]).lower() == bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಟ"):
      bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬಠ")
      args = args[1:]
    elif str(CONFIG[bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಡ")]).lower() == bstack1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಢ"):
      bstack1l1l1l1l1_opy_ = bstack1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨಣ")
      args = args[1:]
    else:
      os.environ[bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫತ")] = bstack1l1l1l1l1_opy_
      bstack1lll11l_opy_(bstack1ll1l1111_opy_)
  global bstack1l11l111_opy_
  try:
    os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬಥ")] = bstack1l1l1l1l1_opy_
    bstack1lll11111_opy_(bstack111ll1l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1l1l1ll_opy_.format(str(e)))
  global bstack1lllll1l1_opy_
  global bstack11lll_opy_
  global bstack1llll11l_opy_
  global bstack111l11_opy_
  global bstack1111_opy_
  global bstack11ll_opy_
  global bstack1ll11l11l_opy_
  global bstack111l_opy_
  global bstack11l11l11_opy_
  global bstack1llll1l_opy_
  global bstack111ll11l_opy_
  global bstack111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    logger.warn(bstack1l1lll1l_opy_ + str(e))
  bstack1lllll1l1_opy_ = webdriver.Remote.__init__
  bstack111l_opy_ = WebDriver.close
  try:
    import Browser
    bstack1l11l111_opy_ = Browser.Browser.__init__
  except:
    pass
  bstack111ll11l_opy_ = WebDriver.get
  if bstack1111l_opy_():
    if bstack1l11l_opy_() < version.parse(bstack1ll1l1l1l_opy_):
      logger.error(bstack11l11ll_opy_.format(bstack1l11l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1lll111l_opy_.format(str(e)))
  if (bstack1l1l1l1l1_opy_ in [bstack1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪದ"), bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫಧ"), bstack1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧನ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll11lll1_opy_
      except Exception as e:
        logger.warn(bstack1l11llll_opy_ + str(e))
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack1l11llll_opy_)
    bstack11lll_opy_ = Output.end_test
    bstack1llll11l_opy_ = TestStatus.__init__
    bstack1111_opy_ = pabot._run
    bstack11ll_opy_ = QueueItem.__init__
    bstack1ll11l11l_opy_ = pabot._create_command_for_execution
  if bstack1l1l1l1l1_opy_ == bstack1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ಩"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack111l11l1_opy_)
    bstack11l11l11_opy_ = Runner.run_hook
    bstack1llll1l_opy_ = Step.run
  if bstack1l1l1l1l1_opy_ == bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨಪ"):
    bstack1ll11lll_opy_()
    bstack1l11ll11_opy_()
    if bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಫ") in CONFIG:
      bstack1l1ll1l1l_opy_ = True
      bstack1ll1l11_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಬ")]):
        bstack1ll1l11_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1ll1lll_opy_, args=(args[0], index)))
      for t in bstack1ll1l11_opy_:
        t.start()
      for t in bstack1ll1l11_opy_:
        t.join()
    else:
      bstack1ll1lll1l_opy_(bstack1l11l1l1_opy_)
      exec(open(args[0]).read())
  elif bstack1l1l1l1l1_opy_ == bstack1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪಭ") or bstack1l1l1l1l1_opy_ == bstack1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫಮ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack1l11llll_opy_)
    bstack1ll11lll_opy_()
    bstack1ll1lll1l_opy_(bstack1lll11_opy_)
    if bstack1l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫಯ") in args:
      i = args.index(bstack1l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬರ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1lllll1ll_opy_))
    args.insert(0, str(bstack1l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ಱ")))
    pabot.main(args)
  elif bstack1l1l1l1l1_opy_ == bstack1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪಲ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack1l11llll_opy_)
    for a in args:
      if bstack1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩಳ") in a:
        bstack1l1l11l_opy_ = int(a.split(bstack1l_opy_ (u"ࠫ࠿࠭಴"))[1])
      if bstack1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩವ") in a:
        bstack1ll11l_opy_ = str(a.split(bstack1l_opy_ (u"࠭࠺ࠨಶ"))[1])
      if bstack1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡐࡐࡉࡍࡌࡌࡉࡍࡇࠪಷ") in a:
        bstack1lll1l1ll_opy_ = str(a.split(bstack1l_opy_ (u"ࠨ࠼ࠪಸ"))[1])
    bstack1ll1lll1l_opy_(bstack1lll11_opy_)
    run_cli(args)
  elif bstack1l1l1l1l1_opy_ == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಹ"):
    try:
      from _pytest.config import _prepareconfig
      import importlib
      bstack11l1ll11_opy_ = importlib.find_loader(bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ಺"))
      if bstack11l1ll11_opy_ is None:
        bstack1l11ll1l_opy_(e, bstack1l11lll_opy_)
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack1l11lll_opy_)
    bstack1ll11lll_opy_()
    try:
      if bstack1l_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭಻") in args:
        i = args.index(bstack1l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸ಼ࠧ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩಽ") in args:
        i = args.index(bstack1l_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪಾ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠨ࠯ࡳࠫಿ") in args:
        i = args.index(bstack1l_opy_ (u"ࠩ࠰ࡴࠬೀ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫು") in args:
        i = args.index(bstack1l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬೂ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l_opy_ (u"ࠬ࠳࡮ࠨೃ") in args:
        i = args.index(bstack1l_opy_ (u"࠭࠭࡯ࠩೄ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1111lll1_opy_ = config.args
    bstack1ll1l1lll_opy_ = config.invocation_params.args
    bstack1ll1l1lll_opy_ = list(bstack1ll1l1lll_opy_)
    bstack1lllllll_opy_ = []
    for arg in bstack1ll1l1lll_opy_:
      for spec in bstack1111lll1_opy_:
        if os.path.normpath(arg) != os.path.normpath(spec):
          bstack1lllllll_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ೅"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1111lll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l11l_opy_)))
                    for bstack11l11l_opy_ in bstack1111lll1_opy_]
    bstack1lllllll_opy_.append(bstack1l_opy_ (u"ࠨ࠯ࡳࠫೆ"))
    bstack1lllllll_opy_.append(bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧೇ"))
    bstack1lllllll_opy_.append(bstack1l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬೈ"))
    bstack1lllllll_opy_.append(bstack1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ೉"))
    bstack11ll11l_opy_ = []
    for spec in bstack1111lll1_opy_:
      bstack1llll1l11_opy_ = []
      bstack1llll1l11_opy_.append(spec)
      bstack1llll1l11_opy_ += bstack1lllllll_opy_
      bstack11ll11l_opy_.append(bstack1llll1l11_opy_)
    bstack1l1ll1l1l_opy_ = True
    bstack1lll1lll1_opy_ = 1
    if bstack1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬೊ") in CONFIG:
      bstack1lll1lll1_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ೋ")]
    bstack1lllllll1_opy_ = int(bstack1lll1lll1_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪೌ")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ್ࠫ")]):
      for bstack1llll1l11_opy_ in bstack11ll11l_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠩࡤࡶ࡬࠭೎")] = bstack1llll1l11_opy_
        item[bstack1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ೏")] = index
        execution_items.append(item)
    bstack1lll1ll_opy_ = bstack1l1111l_opy_(execution_items, bstack1lllllll1_opy_)
    for execution_item in bstack1lll1ll_opy_:
      bstack1ll1l11_opy_ = []
      for item in execution_item:
        bstack1ll1l11_opy_.append(threading.Thread(name=str(item[bstack1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ೐")]),
                                            target=bstack1llll111l_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠬࡧࡲࡨࠩ೑")],)))
      for t in bstack1ll1l11_opy_:
        t.start()
      for t in bstack1ll1l11_opy_:
        t.join()
  elif bstack1l1l1l1l1_opy_ == bstack1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭೒"):
    try:
      from behave.__main__ import main as bstack1ll11ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l11ll1l_opy_(e, bstack111l11l1_opy_)
    bstack1ll11lll_opy_()
    bstack1l1ll1l1l_opy_ = True
    bstack1lll1lll1_opy_ = 1
    if bstack1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ೓") in CONFIG:
      bstack1lll1lll1_opy_ = CONFIG[bstack1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ೔")]
    bstack1lllllll1_opy_ = int(bstack1lll1lll1_opy_)*int(len(CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೕ")]))
    config = Configuration(args)
    bstack1111lll1_opy_ = config.paths
    bstack11l11l1l_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1111lll1_opy_:
        bstack11l11l1l_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack1l_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫೖ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1111lll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l11l_opy_)))
                    for bstack11l11l_opy_ in bstack1111lll1_opy_]
    bstack11ll11l_opy_ = []
    for spec in bstack1111lll1_opy_:
      bstack1llll1l11_opy_ = []
      bstack1llll1l11_opy_ += bstack11l11l1l_opy_
      bstack1llll1l11_opy_.append(spec)
      bstack11ll11l_opy_.append(bstack1llll1l11_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೗")]):
      for bstack1llll1l11_opy_ in bstack11ll11l_opy_:
        item = {}
        item[bstack1l_opy_ (u"ࠬࡧࡲࡨࠩ೘")] = bstack1l_opy_ (u"࠭ࠠࠨ೙").join(bstack1llll1l11_opy_)
        item[bstack1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭೚")] = index
        execution_items.append(item)
    bstack1lll1ll_opy_ = bstack1l1111l_opy_(execution_items, bstack1lllllll1_opy_)
    for execution_item in bstack1lll1ll_opy_:
      bstack1ll1l11_opy_ = []
      for item in execution_item:
        bstack1ll1l11_opy_.append(threading.Thread(name=str(item[bstack1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ೛")]),
                                            target=bstack11l1llll_opy_,
                                            args=(item[bstack1l_opy_ (u"ࠩࡤࡶ࡬࠭೜")],)))
      for t in bstack1ll1l11_opy_:
        t.start()
      for t in bstack1ll1l11_opy_:
        t.join()
  else:
    bstack1lll11l_opy_(bstack1ll1l1111_opy_)
  bstack1lll1l1l1_opy_()
def bstack1lll1l1l1_opy_():
  global CONFIG
  try:
    if bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೝ") in CONFIG:
      host = bstack1l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧೞ") if bstack1l_opy_ (u"ࠬࡧࡰࡱࠩ೟") in CONFIG else bstack1l_opy_ (u"࠭ࡡࡱ࡫ࠪೠ")
      user = CONFIG[bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩೡ")]
      key = CONFIG[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫೢ")]
      bstack1llll1lll_opy_ = bstack1l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨೣ") if bstack1l_opy_ (u"ࠪࡥࡵࡶࠧ೤") in CONFIG else bstack1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭೥")
      url = bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬ೦").format(user, key, host, bstack1llll1lll_opy_)
      headers = {
        bstack1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ೧"): bstack1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ೨"),
      }
      if bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೩") in CONFIG:
        params = {bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ೪"):CONFIG[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭೫")], bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೬"):CONFIG[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೭")]}
      else:
        params = {bstack1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೮"):CONFIG[bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೯")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1lllll11l_opy_ = response.json()[0][bstack1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫ೰")]
        if bstack1lllll11l_opy_:
          bstack1l1ll11ll_opy_ = bstack1lllll11l_opy_[bstack1l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ೱ")].split(bstack1l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩೲ"))[0] + bstack1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬೳ") + bstack1lllll11l_opy_[bstack1l_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ೴")]
          logger.info(bstack11llll1l_opy_.format(bstack1l1ll11ll_opy_))
          bstack1ll1lll1_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ೵")]
          if bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೶") in CONFIG:
            bstack1ll1lll1_opy_ += bstack1l_opy_ (u"ࠨࠢࠪ೷") + CONFIG[bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೸")]
          if bstack1ll1lll1_opy_!= bstack1lllll11l_opy_[bstack1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ೹")]:
            logger.debug(bstack1ll11l1_opy_.format(bstack1lllll11l_opy_[bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೺")], bstack1ll1lll1_opy_))
    else:
      logger.warn(bstack1l1llll1l_opy_)
  except Exception as e:
    logger.debug(bstack1llll11ll_opy_.format(str(e)))
def bstack11l1l1l1_opy_(url):
  global CONFIG
  global bstack1ll111lll_opy_
  if not bstack1ll111lll_opy_:
    hostname = bstack11lll11_opy_(url)
    is_private = bstack1l1l1llll_opy_(hostname)
    if not bstack1ll1ll1l1_opy_(CONFIG) and is_private:
      bstack1ll111lll_opy_ = hostname
def bstack11lll11_opy_(url):
  return urlparse(url).hostname
def bstack1l1l1llll_opy_(hostname):
  for bstack11l111ll_opy_ in bstack1111l111_opy_:
    regex = re.compile(bstack11l111ll_opy_)
    if regex.match(hostname):
      return True
  return False