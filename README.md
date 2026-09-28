# ADS 6703 Natural Language Processing: notebooks and data

Prof. Shripada Hebbar · T A Pai Management Institute, Manipal

This repo is your course folder. Slides, pre-reads and practice problems are on the course website: https://shripada.github.io/ads6703-nlp/

## First time

Follow the [laptop setup guide](https://shripada.github.io/ads6703-nlp/setup.html). In short:

```
git clone https://github.com/shripada/ads6703-nlp.git ADS6703
cd ADS6703
uv venv --python 3.12
uv pip install -r requirements.txt
uv run jupyter lab
```

Open `W00-setup-check.ipynb` and run all cells. Every line should end in ✅.

## Every week

```
cd ADS6703
git pull
uv run jupyter lab
```

`git pull` brings in the new workshop's notebooks and, after class, its solutions.

## What's here

```
ADS6703/
├── requirements.txt       the course libraries
├── W00-setup-check.ipynb  checks your setup
├── data/                  the course datasets
├── w01/                   Workshop 1: Text is data
└── …                      more folders appear as the term goes on
```

Fill in the notebooks where they are. Files that have been published here never change afterwards, so `git pull` will not clash with your work. Please don't rename or move them.
