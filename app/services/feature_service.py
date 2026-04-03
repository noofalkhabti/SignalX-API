import pandas as pd
def build_feature_table(trends,iot,city):
    zones=["Center","Mall","Restaurants"]
    data=[]
    for i,z in enumerate(zones):
        data.append({"zone":z,"trend_score":trends["trend_score"]-i*3,"store_density":trends["store_density"]+i*2,"iot_score":iot["iot_score"]-i*10,"time_factor":iot["time_factor"],"vehicles_live":iot["vehicles_live"]-i*20})
    return pd.DataFrame(data)
