# NER-sklearn-crfsuite-validation
 Training algorithm for the **sklearn-crfsuite** classifier 
 
<p>The model used to train entity recognition was Conditional Random Fields (CRF), available in the Scikit-learn library set. 
This CRF model makes it possible to classify previously determined entities using statistical approaches and machine learning resources that take into account the order in which the words are arranged in the posts. In this CRF model training, we used the file generated in Doccano (see part 2), converting it from JSONL to IOB (also known as CONLL2003). A markup format used in tokens for clustering tasks, used to recognize named entities. The IOB markup system contains marks in the format: 
<ul>B - (Beginning): for the word in the initial block;</ul>
<ul>I - (Inside): for words inside the block; </ul>
<ul>O - (Outside): Outside of any piece.</ul>
<p>

<p>After the transformation, we created a new collection called bio_tokens, stored them in mongodb, where the tweets are separated by each word and label, according to the IOB standard, resulting in:
 <ul>I-Drug, B-Drug, I-ADR, B-ADR and O.</ul>
</p>

<p>The metrics used to measure the performance of the model built in this project were:
 <ul>-<strong>Precision</strong> (or Accuracy) metric is an evaluation metric based on the accuracy of its positive classification, i.e. from the moment something is classified as positive, this metric evaluates how many were actually classified correctly. In this project, precision aims to assess whether the words classified as medicines were, in fact, a medicine, for example. </ul>
<ul>-<strong>Recall</strong>  measure, on the other hand, analyzes the whole, i.e. it uses the positive truth as a reference and compares it with the positive hit. In this project, recall aims to assess how many of the samples that really belonged to an entity (ADR or MEDICINE) the algorithm actually classified into the correct entity.</ul>
<ul>-<strong>F1-score</strong> is the harmonic mean between precision and recall.</ul>
</p>

<p>Results:<br>
<img align="center" width='400px' src='https://user-images.githubusercontent.com/55667496/149041360-bcf3640d-dd47-415b-b21e-df586dabcf0d.png'></p>
 
#
This is part 3 of 5 of the course completion work. Developed by <a href="https://github.com/bpaixao">Beatriz Paixão</a> and <a href="https://github.com/katheleen-gregorato">Katheleen Gregorato</a>. See our publication on CONICT - IFSP at: https://bit.ly/3IsqULo
