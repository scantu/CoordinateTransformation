# 072119 -- rewrite this to 

## read in ds9 image region files
## read in matching header
## convert pixel coords to WCS using header
## save new region files with WCS fk5/icrs
## ... should be simple?

import pyregion
from astropy.io.fits import Header
from astropy.wcs import WCS
from regions import CircleSkyRegion, write_ds9, read_ds9
from astropy.coordinates import Angle, SkyCoord
from pathlib import Path
import numpy as np
import astropy.units as u

imgHeaderPath = Path('headers')
regFile = Path('pixCoords/xyreg.lis')
regDirec = Path('regionFiles/xyregs')
finalReg = Path('regionFiles/skyregs')

arcsec2deg = 1/3600
regRadius = 20. * arcsec2deg

fp = open(regFile, 'r')
ll = fp.readlines()
fp.close()

for name in range(len(ll)):
#     print(regName)
    regName = Path(ll[name])
    print(regName)
    imgName = regName.with_suffix('')
    print(imgName)
    imgName = imgName.with_suffix('')
    print(imgName)
    reg = read_ds9(regDirec.joinpath(regName).with_suffix('.reg'))
    hdr = Header.fromtextfile(str(imgHeaderPath.joinpath(imgName).with_suffix('.head')))
    w = WCS(hdr)
    for rr in range(len(reg)):
        reg[rr] = reg[rr].to_sky(wcs=w)
        
    write_ds9(reg,finalReg.joinpath(imgName).with_suffix('.sky.reg'))


            
