from abc import ABC, abstractmethod,abstractproperty
from concurrent import futures
import grpc
import inference_pb2
import inference_pb2_grpc
import json
class ZenModel(ABC):
    @abstractmethod
    def init(self) -> any:
        pass

    @abstractmethod
    def process(self, input: dict) -> any:
        pass

class Inference(inference_pb2_grpc.InferenceService):
    def __init__(self, model: ZenModel):
        self.model = model
        self.model.init()
    def IsReady(self, request, context):
        return inference_pb2.IsReadyOutput(ready=True)

    def Process(self, request, context):
        print(request)
        data = json.loads(request.input)
        print(data)
        output = self.model.process(input=data)
        data_output = json.dumps(output)
        return inference_pb2.ProcessOutput(output=data_output)

class ZenRunner:
    def __init__(self, model: ZenModel):
        self.inference = Inference(model)

    def start(self):
        port = '50051'
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        inference_pb2_grpc.add_InferenceServiceServicer_to_server(self.inference, server)
        server.add_insecure_port('[::]:' + port)
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()