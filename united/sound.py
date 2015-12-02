"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
import winsound
"""
音效播放模組
"""

for i in range(10):
    i+=1
    winsound.Beep(100*i, 300)

winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
"""
winsound.PlaySound("*.wav", winsound.SND_ALIAS)
"""