import pysc2
import pysc2.lib.units # Not included in pysc2 import

import util

# Generate a directory of units.
unitsSc = util.StrIdMap() # 259 units numbered up to 1961
unitsMl = util.StrIdMap() # With 0-to-258 numbering
unitsMain = util.StrIdMap() # No neutral units.  Don't use the numbering here!
for unitList in [ pysc2.lib.units.Protoss,
                  pysc2.lib.units.Terran,
                  pysc2.lib.units.Zerg ]:
    for enum in unitList:
        unitsSc[enum.numerator] = enum.name
        unitsMain[enum.numerator] = enum.name
for enum in pysc2.lib.units.Neutral:
        unitsSc[enum.numerator] = enum.name
            
for iUnit, scId in enumerate( unitsSc ):
    unitName = unitsSc[scId]
    unitsMl[iUnit] = unitName
