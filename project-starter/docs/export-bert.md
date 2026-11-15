# Export your fine-tuned BERT to ONNX and shrink it

Run this in Colab at the end of your training notebook, after `trainer.save_model("my-bert")` and
`tokenizer.save_pretrained("my-bert")`. The model's config must have `id2label` set when you train it.

```python
!pip install -q "optimum[onnxruntime]"

# 1. Export. For NER use --task token-classification.
!optimum-cli export onnx --model my-bert --task text-classification onnx-out/

# 2. Shrink: store the weights as 8-bit numbers. The file gets about 4 times smaller.
from onnxruntime.quantization import QuantType, quantize_dynamic
quantize_dynamic("onnx-out/model.onnx", "onnx-out/model-int8.onnx", weight_type=QuantType.QInt8)

# 3. Keep the three files the app needs.
import shutil, os
os.makedirs("model", exist_ok=True)
shutil.copy("onnx-out/model-int8.onnx", "model/model.onnx")
shutil.copy("onnx-out/tokenizer.json", "model/tokenizer.json")
shutil.copy("onnx-out/config.json", "model/config.json")
!ls -lh model/
```

Download the `model/` folder and put it in your repo, or upload it to the Hugging Face Hub.

Check the shrunk model before you use it: run your test set through it and make sure accuracy has
dropped by no more than a point or two. If `optimum-cli` is not found, install `optimum-onnx` instead.
