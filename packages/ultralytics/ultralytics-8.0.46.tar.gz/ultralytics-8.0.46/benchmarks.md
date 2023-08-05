
Benchmarks complete for yolov8n.pt on coco128.yaml at imgsz=160 (16.74s)
                   Format Status❔  Size (MB)  metrics/mAP50-95(B)  Inference time (ms/im)
0                 PyTorch       ✅        6.2               0.2089                   12.53
1             TorchScript       ✅       12.3               0.2095                   12.26
2                    ONNX       ✅       12.1               0.2095                    5.98
3                OpenVINO       ✅       12.2               0.2095                   51.18
4                TensorRT       ❌        NaN                  NaN                     NaN
5                  CoreML       ❌        NaN                  NaN                     NaN
6   TensorFlow SavedModel       ❌        NaN                  NaN                     NaN
7     TensorFlow GraphDef       ❌        NaN                  NaN                     NaN
8         TensorFlow Lite       ❌        NaN                  NaN                     NaN
9     TensorFlow Edge TPU       ❌        NaN                  NaN                     NaN
10          TensorFlow.js       ❌        NaN                  NaN                     NaN
11           PaddlePaddle       ❌        NaN                  NaN                     NaN