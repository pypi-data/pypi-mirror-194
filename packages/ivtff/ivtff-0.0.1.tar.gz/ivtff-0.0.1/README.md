# ivtff-py

A simple Python tool to work with Rene Zandbergen's IVTFF file format, inspired by [his IVTT software](https://www.voynich.nu/software/ivtt/)

## Motivation

Currently, no open-source tool exists for working with IVTFF files (while Zandbergen does provide the source code for his tool, it is not officially released under any open-source license). Additionally, Zandbergen's tool is written in C. To make IVTFF files easier to use by more programmers, this simple Python tool is provided.

## Obtaining IVTFF files

The most up to date IVTFF transliteration files can be found on [Rene Zandbergen's website](https://www.voynich.nu/data/). I personally use the `ZL_ivtff_2b` transliteration. You can download this transliteration using the following command:

```bash
curl https://www.voynich.nu/data/ZL_ivtff_2b.txt -o ZL_ivtff_2b.txt
```
