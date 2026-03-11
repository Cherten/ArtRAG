import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.rag_pipeline import RAGPipeline
from rouge_score import rouge_scorer

def main():
    with open("data/test_set.json", "r") as f:
        test_data = json.load(f) 

    pipeline = RAGPipeline()
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    rouge1, rouge2, rougeL = [], [], []
    for item in test_data:
        result = pipeline.answer(item["question"])
        scores = scorer.score(item["expected_answer"], result["answer"])
        rouge1.append(scores['rouge1'].fmeasure)
        rouge2.append(scores['rouge2'].fmeasure)
        rougeL.append(scores['rougeL'].fmeasure)

    print(f"ROUGE-1: {sum(rouge1)/len(rouge1):.4f}")
    print(f"ROUGE-2: {sum(rouge2)/len(rouge2):.4f}")
    print(f"ROUGE-L: {sum(rougeL)/len(rougeL):.4f}")

if __name__ == "__main__":
    main()