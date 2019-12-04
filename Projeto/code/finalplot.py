import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as scatter

ts = [0,1]
complete = [0,26.948]
plt.xlabel('Heteroginity')
plt.ylabel('Cooperation')
plt.plot( complete, ts,'o-r')
plt.legend(loc='best', frameon=False)
plt.show()