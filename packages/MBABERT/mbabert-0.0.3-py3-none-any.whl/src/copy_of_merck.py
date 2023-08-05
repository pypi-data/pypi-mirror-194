# -*- coding: utf-8 -*-
import numpy as np
import torch
import torch.nn.functional as F
from typing import Tuple
import json
from typing import Tuple
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, IntervalStrategy, TrainerCallback
from transformers import TrainingArguments, default_data_collator, Trainer, BertConfig, TFBertModel, load_tf_weights_in_bert
import pandas as pd
# from model_testing import ModelTester
from typing import Tuple
import pandas as pd
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import json, sys
from typing import Counter, Tuple
from transformers import BertForTokenClassification, BertTokenizerFast, BertConfig
from sklearn.metrics import accuracy_score
# from custom_dataset import dataset
from collections import defaultdict
# from ner_utils import test_model, get_device, get_datasets
from sklearn.metrics import classification_report
# from NER_Constants import test_data_files_dir, testing_model_dir, MAX_LEN, TRAIN_BATCH_SIZE, VALID_BATCH_SIZE
######
from transformers import BertForTokenClassification
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
from operator import itemgetter
import re
from itertools import groupby

testing_model_dir = "./"

ids_to_labels = {
    0: "ACCURACY",
    1: "ANALYTE",
    2: "BIOLOGICAL SUBSTANCE",
    3: "COEFFICIENT OF VARIATION",
    4: "COLUMN DIMENSIONS",
    5: "COLUMN MANUFACTURER",
    6: "COLUMN TEMPERATURE",
    7: "FLOW RATE",
    8: "INTERNAL STANDARD",
    9: "IONIZATION METHOD",
    10: "LIMIT OF QUANTIFICATION",
    11: "LINEAR RANGE",
    12: "MASS TRANSITION",
    13: "MATRIX EFFECTS",
    14: "METHOD",
    15: "MOBILE PHASE",
    16: "O",
    17: "PRECISION",
    18: "RUN TIME",
    19: "SENSITIVITY"
  }

labels_to_ids = {"ACCURACY": 0, "ANALYTE": 1, "BIOLOGICAL SUBSTANCE": 2,
    "COEFFICIENT OF VARIATION": 3,
    "COLUMN DIMENSIONS": 4,
    "COLUMN MANUFACTURER": 5,
    "COLUMN TEMPERATURE": 6,
    "FLOW RATE": 7,
    "INTERNAL STANDARD": 8,
    "IONIZATION METHOD": 9,
    "LIMIT OF QUANTIFICATION": 10,
    "LINEAR RANGE": 11,
    "MASS TRANSITION": 12,
    "MATRIX EFFECTS": 13,
    "METHOD": 14,
    "MOBILE PHASE": 15,
    "O": 16,
    "PRECISION": 17,
    "RUN TIME": 18,
    "SENSITIVITY": 19}

class BertModel(torch.nn.Module):

    def __init__(self):

        super(BertModel, self).__init__()

        self.bert = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=20)

    def forward(self, input_id, mask, label):

        output = self.bert(input_ids=input_id, attention_mask=mask, labels=label, return_dict=False)

        return output

tokenizer = BertTokenizerFast.from_pretrained(testing_model_dir, local_files_only=True)
def align_word_ids(texts):
    label_all_tokens = False
    tokenized_inputs = tokenizer(texts, padding='max_length', max_length=512, truncation=True)

    word_ids = tokenized_inputs.word_ids()

    previous_word_idx = None
    label_ids = []

    for word_idx in word_ids:

        if word_idx is None:
            label_ids.append(-100)

        elif word_idx != previous_word_idx:
            try:
                label_ids.append(1)
            except:
                label_ids.append(-100)
        else:
            try:
                label_ids.append(1 if label_all_tokens else -100)
            except:
                label_ids.append(-100)
        previous_word_idx = word_idx

    return label_ids
config = BertConfig.from_json_file("./config.json")
def get_device():                    
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = get_device()
#print(model)
def evaluate_one_text(model, sentence):
    sentence = sentence.lower()
    words = re.split(' ', sentence)
    word_dict = {}
    #print(words)
    #word_dict = {word:i for i, word in enumerate(words)}
    use_cuda = torch.cuda.is_available()
    inputs = tokenizer(words,
                       is_split_into_words=True,
                       return_offsets_mapping=True,
                       padding='max_length',
                       truncation=True,
                       max_length=512,
                       return_tensors="pt")

    ids = inputs["input_ids"].to(device)
    mask = inputs["attention_mask"].to(device)
    # forward pass
    outputs = model(ids, attention_mask=mask)
    logits = outputs[0]
    config: BertConfig = model.config
    active_logits = logits.view(-1, 20)  # shape (batch_size * seq_len, num_labels)
    flattened_predictions = torch.argmax(active_logits,
                                         axis=1)  # shape (batch_size*seq_len,) - predictions at the token level
    #print(flattened_predictions)
    tokens = tokenizer.convert_ids_to_tokens(ids.squeeze().tolist())
    prediction = []
    token_predictions = [config.id2label[i] for i in flattened_predictions.cpu().numpy()]
    wp_preds = list(zip(tokens, token_predictions))  # list of tuples. Each tuple = (wordpiece, prediction)
    for token_pred, mapping in zip(wp_preds, inputs["offset_mapping"].squeeze().tolist()):
        # only predictions on first word pieces are important
        if mapping[0] == 0 and mapping[1] != 0:
            prediction.append(token_pred[1])
        else:
            continue
    #return predicts
    filteredPreds = []
    filteredWords = []
    finalPreds = {}
    #print(len(words))
    #print(len(prediction))
    for i in range(len(words)):
      word_dict[words[i]] = prediction[i]
      if(prediction[i] != "O"):
        filteredPreds.append(prediction[i])
        filteredWords.append(words[i])
    #print(filteredPreds)
    labelList = []
    dummyV = []
    realV = []
    num = 0
    counter = 0
    predict_dict = {}
    for group in groupby(prediction):
       labelList.append(list(group[1]))
    for i in labelList:
       dummyV.append(len(i))

    for i in dummyV:
       num = num + i
       realV.append(num)
    #print(realV)

    tokenJoin = [words[s:e] for s, e in zip([0]+realV, realV+[None])]
    j = 0
    tokenJoin.remove([])
    #print(len(labelList))
    #print(len(tokenJoin))
    while j < len(tokenJoin):
      finalTokens = " ".join(tokenJoin[j])
      finalPreds = labelList[j][0]
      predict_dict[finalTokens] = finalPreds
      j = j + 1
    for j, k in predict_dict.items():
      print(k, ": ", j)
#evaluate_one_text(BertForTokenClassification.from_pretrained(testing_model_dir, local_files_only=True, ignore_mismatched_sizes=True).to(device),
#"This analytical method is based on an automated 96-well format protein precipitation of drug from dog plasma. MK-0111 and stable isotope labeled internal standard (SIL-MK-0111) are chromatographed using reversed phase liquid chromatography and detected with tandem mass spectrometric detection employing a turbo ionspray (TIS) interface in the positive ion mode. The Multiple Reaction Monitoring (MRM) transitions monitored were m/z 517.2 482.3 for the drug and m/z 525.2 489.2 for the internal standard. The lower limit of quantitation (LLOQ) for this method is 5.00 ng/mL with a linear 1/x2 (weighting) calibration range from 5.00 to 5,000 ng/mL using a 20 L plasma sample. Standard solutions are prepared in ACN/H2O [50/50] and stored at +4C when not in use. EDTA is used as the anticoagulant and plasma study samples are stored at -70C.")



