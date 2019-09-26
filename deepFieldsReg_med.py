import pyregion
from astropy.io.fits import Header
from astropy.wcs import WCS
from regions import CircleSkyRegion, write_ds9
from astropy.coordinates import Angle, SkyCoord
from pathlib import Path
import numpy as np
import astropy.units as u

# read cr file
# replace with header name
# convert from png coord to fits coord
# convert from fits image coord to ra/dec coord
# create region files
# change radius to 5" (done)
# change reg file output to be per image
# do they need to be color specific?

imgHeaderPath = Path(input('Image Header Directory? '))
crfile = Path(input('Coord File? \'https:... x y author\' -- format '))
regFile = Path(input('Region file directory? '))


arcsec2deg = 1/3600
regRadius = 20. * arcsec2deg

fp = open(crfile, 'r')
ll = fp.readlines()
fp.close()
for imgName in range(len(ll)):
    try:
        p = Path(ll[imgName].split()[0])
        print(p)
        header = p.stem.replace(p.stem[p.stem.find('_', 8):], '.head') 
        print(header)
        imgHeader = Header.fromtextfile(str(imgHeaderPath.joinpath(header)))
        pngX,pngY = float(ll[imgName].split()[1]), float(ll[imgName].split()[2])
        if ll[imgName].split()[0][-3:] == 'jpg':
#         pixX, pixY = pngX*1.689, 2200-(pngY*1.686)
            pixX, pixY = pngX/.5, (1100-pngY)/.5
        elif ll[imgName].split()[0][-3:] == 'png':
            pixX, pixY = (pngX/(2487/2100))/.5, ((1306-pngY)/(1306/1100))/.5
        else:
            print('what the hell happened!?!')
            break
        xy = np.column_stack((pixX,pixY))
        print(header)
        w = WCS(imgHeader)
        coords = w.wcs_pix2world(xy,1)                   
        raDec = SkyCoord(coords[0][0]*u.deg, coords[0][1]*u.deg)
        region = CircleSkyRegion(raDec, regRadius*u.deg)
        region.visual['color'] = 'red'
        region.visual['width'] = '2'
        header = Path(header).stem+'_'+str(imgName)
        print(header)
        regName = regFile.joinpath(header).with_suffix('.reg')
        print(regName)
        write_ds9([region], regName)
    except:
        pass

regfiles = sorted(regFile.glob('*reg'))
for rf,x in zip(regfiles,range(len(regfiles)-1)):
    if regfiles[x].stem[:regfiles[x].stem.find('_', 8)] != regfiles[x+1].stem[:regfiles[x].stem.find('_', 8)]:
        print('break')
        fp.close(regfiles[x].stem[:regfiles[x].stem.find('_', 8)])
    else:
        print('match')
        fp.open() 

        

            
