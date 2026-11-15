"""Runs your fine-tuned BERT from model/, with onnxruntime (no PyTorch).

model/ must hold three files, all produced by the export in your training notebook:
  model.onnx       the (quantised) model
  tokenizer.json   the fast tokenizer
  config.json      the model config, with id2label
This is set up for text classification. For NER, ask your agent to change predict() to return one
label per token (token classification) and to join the word pieces back into words.
"""
import json
from pathlib import Path

import numpy as np

MODEL_DIR = Path(__file__).resolve().parents[2] / "model"


class ModelMissing(RuntimeError):
    pass


class BertClassifier:
    def __init__(self, model_dir: Path = MODEL_DIR, max_length: int = 256):
        if not (model_dir / "model.onnx").exists():
            raise ModelMissing(f"No model.onnx in {model_dir}. Export your fine-tuned model there first.")
        import onnxruntime as ort
        from tokenizers import Tokenizer

        self.tokenizer = Tokenizer.from_file(str(model_dir / "tokenizer.json"))
        self.tokenizer.enable_truncation(max_length)
        self.session = ort.InferenceSession(str(model_dir / "model.onnx"), providers=["CPUExecutionProvider"])
        self.input_names = {i.name for i in self.session.get_inputs()}
        id2label = json.loads((model_dir / "config.json").read_text())["id2label"]
        self.labels = [id2label[str(i)] for i in range(len(id2label))]

    def predict(self, text: str) -> tuple[str, float]:
        enc = self.tokenizer.encode(text)
        feeds = {
            "input_ids": np.array([enc.ids], dtype=np.int64),
            "attention_mask": np.array([enc.attention_mask], dtype=np.int64),
            "token_type_ids": np.array([enc.type_ids], dtype=np.int64),
        }
        logits = self.session.run(None, {k: v for k, v in feeds.items() if k in self.input_names})[0][0]
        probs = np.exp(logits - logits.max())
        probs /= probs.sum()
        best = int(probs.argmax())
        return self.labels[best], float(probs[best])


_classifier: BertClassifier | None = None


def get_classifier() -> BertClassifier:
    """Loads the model once per server start."""
    global _classifier
    if _classifier is None:
        _classifier = BertClassifier()
    return _classifier
