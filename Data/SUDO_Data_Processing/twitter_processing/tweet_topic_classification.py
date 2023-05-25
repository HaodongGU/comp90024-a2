from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import expit


# class TweetTopicClassifier:
#
#     def __init__(self, model_path, tweet):
#         self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
#         self.tokenizer = AutoTokenizer.from_pretrained(model_path)
#         self.tweet = tweet
#
#     def topic_classifier(self):
#         tokens = self.tokenizer(self.tweet, return_tensors='pt')
#         output = self.model(**tokens)
#         class_mapping = self.model.config.id2label
#
#         scores = output[0][0].detach().numpy()
#         scores = expit(scores)
#         predictions = (scores >= 0.5) * 1
#
#         predict_topics = []
#         for i in range(len(predictions)):
#             if predictions[i]:
#                 predict_topics.append(class_mapping[i])
#
#         return predict_topics


def load_model(model_path):
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer


def topic_classifier(model, tokenizer, tweet):
    tokens = tokenizer(tweet, return_tensors='pt')
    output = model(**tokens)
    class_mapping = model.config.id2label

    scores = output[0][0].detach().numpy()
    scores = expit(scores)
    predictions = (scores >= 0.5) * 1

    predict_topics = []
    for i in range(len(predictions)):
        if predictions[i]:
            predict_topics.append(class_mapping[i])

    return predict_topics



