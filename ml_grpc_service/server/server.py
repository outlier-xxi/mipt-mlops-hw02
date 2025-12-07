import grpc, os
from concurrent import futures
from ml_grpc_service import model_pb2, model_pb2_grpc
from ml_grpc_service.server.inference import ModelRunner
from ml_grpc_service.server.validation import features_to_dict, ValidationError

MODEL_PATH = os.getenv("MODEL_PATH", "ml_grpc_service/models/model.pkl")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.0.1")
SCALER_PATH = os.getenv("SCALER_PATH", None)  
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
PORT = int(os.getenv("PORT", "50051"))

class PredictionService(model_pb2_grpc.PredictionServiceServicer):
    def __init__(self):
        self.runner = ModelRunner(MODEL_PATH, version=MODEL_VERSION, scaler_path=SCALER_PATH)

    def Health(self, request, context):
        return model_pb2.HealthResponse(status="ok", model_version=self.runner.version)

    def Predict(self, request, context):
        try:
            feats = features_to_dict(request.features)
            pred, conf = self.runner.predict(feats)
            return model_pb2.PredictResponse(
                prediction=pred, confidence=conf, model_version=self.runner.version
            )
        except ValidationError as ve:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(ve))
            return model_pb2.PredictResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"internal error: {e}")
            return model_pb2.PredictResponse()

def serve():
    options = [
        ("grpc.max_send_message_length", 50 * 1024 * 1024),
        ("grpc.max_receive_message_length", 50 * 1024 * 1024),
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS), options=options)
    model_pb2_grpc.add_PredictionServiceServicer_to_server(PredictionService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    scaler_info = f", scaler={SCALER_PATH}" if SCALER_PATH else ""
    print(f"gRPC server started on :{PORT}, model={MODEL_PATH}, version={MODEL_VERSION}{scaler_info}")
    server.wait_for_termination()

if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
    except Exception:
        pass
    serve()