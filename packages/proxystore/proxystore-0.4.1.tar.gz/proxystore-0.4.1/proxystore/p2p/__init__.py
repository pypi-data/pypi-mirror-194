"""Peer-to-peer communication and signaling.

This module provides two main functionalities: the
[`PeerManager`][proxystore.p2p.manager.PeerManager] and
[`SignalingServer`][proxystore.p2p.server.SignalingServer].

* The [`PeerManager`][proxystore.p2p.manager.PeerManager] enables
  easy communication between arbitrary peers even if peers are behind separate
  NATs. Peer connections are established using
  [aiortc](https://aiortc.readthedocs.io/), an asyncio WebRTC implementation.
* The [`SignalingServer`][proxystore.p2p.server.SignalingServer] is a
  commonly accessible server by peers that is used to facilitate WebRTC peer
  connections.
"""
from __future__ import annotations
