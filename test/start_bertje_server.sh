#!/usr/bin/env bash

bert-serving-start -model_dir bertje-base -num_worker=2 -config_name=config.json -ckpt_name=model.ckpt