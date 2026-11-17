def to_weekly(returns):
    return (1+returns).resample("W-FRI").prod()-1


def risky_returns(returns):
    return returns[returns.columns.drop("RF")]


def excess_returns(returns):
    return risky_returns(returns).sub(returns["RF"], axis=0)
