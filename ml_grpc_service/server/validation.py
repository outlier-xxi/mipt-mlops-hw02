from typing import Iterable
from ml_grpc_service import model_pb2

class ValidationError(Exception):
    pass

# Wine Quality Dataset features (11 physicochemical properties)
WINE_QUALITY_FEATURES = {
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol"
}

def features_to_dict(features: Iterable[model_pb2.Feature], validate_wine_features: bool = True) -> dict[str, float]:
    """
    Convert gRPC Feature messages to a dictionary.
    """
    data = {}
    for f in features:
        if f.name in data:
            raise ValidationError(f"Duplicate feature: {f.name}")
        if not f.name:
            raise ValidationError("Empty feature name")
        data[f.name] = float(f.value)

    if not data:
        raise ValidationError("No features provided")

    # Validate wine quality features if requested
    if validate_wine_features:
        provided_features = set(data.keys())

        # Check for missing features
        missing_features = WINE_QUALITY_FEATURES - provided_features
        if missing_features:
            raise ValidationError(
                f"Missing required wine quality features: {sorted(missing_features)}"
            )

        # Check for extra/unknown features
        extra_features = provided_features - WINE_QUALITY_FEATURES
        if extra_features:
            raise ValidationError(
                f"Unknown features provided: {sorted(extra_features)}. "
                f"Expected features: {sorted(WINE_QUALITY_FEATURES)}"
            )

    return data