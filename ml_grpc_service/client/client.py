import grpc
from ml_grpc_service import model_pb2, model_pb2_grpc

def make_stub(addr: str = "localhost:50051"):
    channel = grpc.insecure_channel(addr)
    return model_pb2_grpc.PredictionServiceStub(channel)

def health(stub):
    res = stub.Health(model_pb2.HealthRequest(), timeout=2.0)
    print("Health:", res.status, "version:", res.model_version)

def predict_wine_quality(stub):
    """
    Predict wine quality using physicochemical properties.

    Example wine features (all 11 required features):
    - "fixed acidity": 7.4
    - "volatile acidity": 0.7
    - "citric acid": 0.0
    - "residual sugar": 1.9
    - "chlorides": 0.076
    - "free sulfur dioxide": 11.0
    - "total sulfur dioxide": 34.0
    - "density": 0.9978
    - "pH": 3.51
    - "sulphates": 0.56
    - "alcohol": 9.4
    """

    sample = {
        "fixed acidity": 7.4,
        "volatile acidity": 0.70,
        "citric acid": 0.00,
        "residual sugar": 1.9,
        "chlorides": 0.076,
        "free sulfur dioxide": 11.0,
        "total sulfur dioxide": 34.0,
        "density": 0.9978,
        "pH": 3.51,
        "sulphates": 0.56,
        "alcohol": 9.4
    }

    req = model_pb2.PredictRequest(features=[
        model_pb2.Feature(name="fixed acidity", value=sample["fixed acidity"]),
        model_pb2.Feature(name="volatile acidity", value=sample["volatile acidity"]),
        model_pb2.Feature(name="citric acid", value=sample["citric acid"]),
        model_pb2.Feature(name="residual sugar", value=sample["residual sugar"]),
        model_pb2.Feature(name="chlorides", value=sample["chlorides"]),
        model_pb2.Feature(name="free sulfur dioxide", value=sample["free sulfur dioxide"]),
        model_pb2.Feature(name="total sulfur dioxide", value=sample["total sulfur dioxide"]),
        model_pb2.Feature(name="density", value=sample["density"]),
        model_pb2.Feature(name="pH", value=sample["pH"]),
        model_pb2.Feature(name="sulphates", value=sample["sulphates"]),
        model_pb2.Feature(name="alcohol", value=sample["alcohol"]),
    ])
    res = stub.Predict(req, timeout=3.0)
    print("Wine Quality Prediction:", res.prediction, "confidence:", round(res.confidence, 4), "version:", res.model_version)


if __name__ == "__main__":
    stub = make_stub()
    health(stub)
    predict_wine_quality(stub)