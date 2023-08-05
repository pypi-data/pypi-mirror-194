# ovos-PHAL-plugin - pulseaudio volume control

controls system volume with pulseaudio

```python
self.bus.on("mycroft.volume.get", self.handle_volume_request)
self.bus.on("mycroft.volume.set", self.handle_volume_change)
self.bus.on("mycroft.volume.mute", self.handle_mute_request)
self.bus.on("mycroft.volume.unmute", self.handle_unmute_request)
```