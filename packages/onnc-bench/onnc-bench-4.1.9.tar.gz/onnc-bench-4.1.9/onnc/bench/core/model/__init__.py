from enum import Enum


class ModelFormat(Enum):
    NON_SPECIFIED = 0
    UNKNOWN = 1

    PT_NN_MODULE = 11
    TF_KERAS_MODEL = 12
    KERAS_MODEL = 13
    TF_SESSION = 14

    H5 = 21
    SAVED_MODEL = 22
    PB = 23
    ZIPPED_SAVED_MODEL = 24
    TFLITE = 25

    PTH = 31
    ONNX = 32
    TORCH_TRACED = 33

    CKPT = 26

    TRT_PLAN = 41
    OPENVINO_IRDIR = 42

    GRAPHDEF = 51

    RELAYIR = 61

    MLIR = 71


TF_MODEL_FORMATS = [ModelFormat.TF_KERAS_MODEL,
                    ModelFormat.KERAS_MODEL,
                    ModelFormat.H5,
                    ModelFormat.SAVED_MODEL,
                    ModelFormat.PB,
                    ModelFormat.TFLITE,
                    ModelFormat.CKPT]

PYTORCH_MODEL_FORMATS = [ModelFormat.PT_NN_MODULE,
                         ModelFormat.PTH,
                         ModelFormat.TORCH_TRACED]
class ModelDataType(Enum):
    NON_SPECIFIED = 0
    FP32 = 1
    UINT8 = 2
    INT8 = 3
    UINT16 = 4
    INT16 = 5
    INT32 = 6
    INT64 = 7
    STR = 8
    BOOL = 9
    FP16 = 10
    FP64 = 11
    UINT32 = 12
    UINT64 = 14
    COMPLEX128 = 15
    BFLOAT16 = 16
