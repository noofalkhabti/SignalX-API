from sklearn.linear_model import LinearRegression
def run_regression_estimation(df):
    X = df[["trend_score","store_density","iot_score","time_factor"]]
    y = (df["vehicles_live"]*8 + df["store_density"]*5).values
    model = LinearRegression()
    model.fit(X,y)
    preds = model.predict(X)
    zones=[]
    for zone,p in zip(df["zone"],preds):
        zones.append({"zone":zone,"estimated_workers":round(float(p),1)})
    return {"zones":zones}
