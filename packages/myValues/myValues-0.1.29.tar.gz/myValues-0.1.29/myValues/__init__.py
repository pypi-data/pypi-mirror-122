for i in['tk','math',"tools"]:
    exec ("from myValues import "+i)
    exec ("from myValues."+i+" import *")