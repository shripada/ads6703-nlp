# model/

Put your exported BERT here (see ../docs/export-bert.md):

- `model.onnx`: the quantised model
- `tokenizer.json`: the fast tokenizer
- `config.json`: with `id2label`, so the app can turn a number into a label name

Other files from the export (vocab.txt, special_tokens_map.json…) can be deleted.
