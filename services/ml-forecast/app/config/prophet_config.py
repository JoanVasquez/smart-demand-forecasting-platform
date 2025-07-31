from prophet import Prophet


def get_prophet_model():
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    return model

