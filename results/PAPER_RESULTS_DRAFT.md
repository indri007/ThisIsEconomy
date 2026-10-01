# Academic Results Draft for TIME-E 2026 Camera-Ready Manuscript

### 4.3 Multi-Class Affective Classification Performance and Baseline Benchmarking

To benchmark the natural language processing component, the dataset of $N = 5,263$ tweets was partitioned into training ($80\%$, $n = 4205$) and held-out evaluation ($20\%$, $n = 1058$) subsets using a group-aware split protocol (`GroupShuffleSplit`, random seed 42) grouped by normalized text sequences. This strictly guaranteed zero lexical overlap between training and testing partitions (`Text Overlap = 0`), preventing data leakage caused by viral retweet duplications. Evaluation was conducted against silver-standard reference annotations derived from automated semantic labeling.

Table 2 summarizes the comparative performance across architectures. On the group-aware test partition, the fine-tuned `indobert-base-p2` model achieved an overall accuracy of 0.7940 and a weighted F1-score of 0.7851, with an unweighted macro F1-score of 0.5160. For linear baselines evaluated under the identical zero-leakage split, TF-IDF with Logistic Regression yielded an accuracy of 0.6947 and macro F1 of 0.3429, while TF-IDF with Linear SVM obtained an accuracy of 0.6720 and macro F1 of 0.4095.

**Table 2: Empirical Performance Benchmark on Group-Aware Test Set ($n = 1058$)**
| Model Architecture | Feature Representation | Accuracy | Macro F1 | Weighted F1 | Protocol |
| :--- | :--- | :---: | :---: | :---: | :---: |
| TF-IDF + Logistic Regression | Word & Bigram TF-IDF | 0.6947 | 0.3429 | 0.6457 | Group-Aware (Zero Leakage) |
| TF-IDF + Linear SVM | Word & Bigram TF-IDF | 0.6720 | 0.4095 | 0.6558 | Group-Aware (Zero Leakage) |
| IndoBERT (Fine-Tuned) | Contextual Transformer Embeddings | 0.7940 | 0.5160 | 0.7851 | Group-Aware (Zero Leakage) |

As illustrated in the confusion matrix (Figure 4), empirical performance reflects the extreme class imbalance of public discourse surrounding the Free Nutritious Meal rollout. The *Disgust* category represented 56.2\% of the empirical corpus, yielding high recall (0.8729) and F1 (0.8444) for IndoBERT on majority critical discourse. Conversely, severe under-representation of minor affective categories (*Anger*, *Sadness*, and *Fear*, each below 1.5\% of the corpus) constrained macro-averaged metrics. The observed variance between linear ngram baselines and contextual transformer embeddings may be associated with the strong discriminative power of explicit affective keywords in sparse short-text social media postings under high class skew.
