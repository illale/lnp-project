
# Project 27: Semantic Similarity 3

This project will demonstrate various methodologies for computing sentence-to-sentence similarity scores.

## Files

`project.ipynb` - Tasks 1-7  
`gui.py` - Task 8

## 1. Annotated Word Pair Datasets
Consider the datasets of word pairs whose similarity is manually annotated, especially **MC-28**, **WordSim**, and **RG**, available at [https://github.com/alexanderpanchenko/sim-eval](https://github.com/alexanderpanchenko/sim-eval). Similarly to the work on this repository, we would like to test the usefulness of any new similarity measure by computing its correlation with human judgment (using **Pearson coefficient**). Review how Pearson Coefficient works and identify python script to achieve this. Study **Datamuse API**, which outputs a set of words that are available to a query word. This API is available at [http://www.datamuse.com/api/](http://www.datamuse.com/api/).

## 2. Testing Similarity with Datamuse API and Jaccard Similarity
We would like to test the similarity between the pair (X, Y) by using the output of the Datamuse API for both X and Y. Set the number of outcome words in the API to be large, e.g., 100. Use **Jaccard similarity** to compute the similarity between X and Y (counting the ratio of common words among the outputs of X and Y from the Datamuse API over the total number of distinct words in the two outputs). Repeat this process of calculating the similarity between each pair in **MC-28** dataset, and then calculate the correlation coefficient with the human judgment using the Pearson coefficient. Try to optimize the parameters of the Datamuse API call by testing a distinct number of outputs and monitor the value of the correlation until you reach the highest correlation value. Use the latest configuration to calculate the correlation value for other datasets, and compare the result with other state-of-the-art results as reported in relevant literature (e.g., previous **sim-eval** repository). Report the findings in a table highlighting the optimal parameters of the Datamuse function as well as the result of the correlation analysis for each dataset.

## 3. Sentence-Level Similarity Using Datamuse API
We would like to test the above strategy at the **sentence level** as well. For this purpose, given sentences **S1** and **S2**, which are tokenized as **S1 = (w1, w2, …, wn)** and **S2 = (p1, p2, …, pm)**. The representation of **S1** will consist of the overlap of the Datamuse output of each individual token w1, w2,…wn (it is important to set the number of outputted words per API call high in order to increase the chance of overlapping), and add to this list the tokens of **S1** as well. Repeat the same process for **S2** and then compute the similarity between **S1** and **S2** as **Jaccard similarity** of the representation of **S1** and the representation of **S2**. Write a simple Python code that allows you to achieve this.

## 4. Academic Sentence Similarity Testing
We want to test this strategy on a set of academic sentences:
- **S1**: Today is quite hot for a winter. 
- **S2**: Never is warm in winter.
- **S1**: The car is running fast but has some troubles recently.
- **S2**: Toyota cars are recalled for a fault.
- **S1**: The teacher cannot do it again and never again.
- **S2**: Teacher has been prohibited from this task.

Proceed by applying the Datamuse approach on each of the above pairs (S1, S2) and report the findings in a table, and comment on the findings.

## 5. Optimizing Datamuse API Call Frequency
We want to reduce the number of pairs that will be queried from Datamuse. For this purpose, we assume that if Datamuse(w1) generates a set of words that contains one of the terms in sentence S2, say, p2, then **Sim(S1, S2)** will be boosted and p2 will be discarded from the list of terms that require a Datamuse query. Suggest a script that implements this refinement and test its performance on the above sentence pairs.

## 6. Testing on Publicly Available Datasets
We want to test this strategy on publicly available sentence datasets. For this purpose, use the **STSS-131 dataset**, available in "A new benchmark dataset with production methodology for short text semantic similarity algorithms" by O’Shea, Bandar, and Crockett (ACM Transactions on Speech and Language Processing, 2013). Use the **Pearson correlation coefficient** to test the correlation with the provided human judgment using both versions of Datamuse-based sentence similarity.

## 7. TF-IDF Embeddings and Cosine Similarity
Repeat the process of sentence similarity for the **STSS-131 dataset**, but use **TF-IDF embeddings** as in the labs, assuming the vector representation of a sentence. Use **cosine similarity** to compute the similarity score and calculate the corresponding Pearson correlation as well.

## 8. Alternative Similarity Methods with Other Lexical Databases
Study the programs in [https://github.com/gsi-upm/sematch](https://github.com/gsi-upm/sematch) which provide other individual similarity measures using lexical databases other than WordNet. Accommodate the provided files into your comparison and repeat the calculation of **Sim(S1, S2)** for each pair of sentences where the individual similarity **Sim(s,t)** is calculated using **YAGO concepts** or **DBPedia concepts** freely available from the program. Compare the behavior of the results.

## 9. GUI for Demonstrating Results
Suggest a **GUI** of your own that facilitates the demonstration of your findings above.

## 10. Analysis and Reporting
Use appropriate literature to comment on the findings. Identify any additional inputs that would allow you to further elucidate the preceding steps and use corpus linguistic literature to justify your findings. Finally, comment on the limitations and structural weaknesses of the data processing pipeline.
