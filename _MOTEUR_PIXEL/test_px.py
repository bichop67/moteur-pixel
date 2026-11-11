import sys
from px import Px
import decors_px, freres_px
c = Px()
decors_px.ablutions(c)
freres_px.petit(c, 78, 452, "question")
freres_px.grand(c, 186, 462, "explique")
c.img().save(sys.argv[1])
