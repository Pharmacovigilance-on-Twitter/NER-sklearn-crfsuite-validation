# NER-sklearn-crfsuite-validation
 Algorithm for classifier training **sklearn-crfsuite**
 
<p>The model used for training entity recognition was the Conditional Random Fields (CRF), available in the scikit-learn set of libraries. The CRF model allows classifying the entities, previously determined, through statistical approaches and machine learning resources, which take into account the order in which the words are arranged in the posts.
For training the CRF model, we use the generated file in Doccano (see part 2), and convert it from JSONL to IOB (also known as CONLL2003).
This is a markup format used in tokens for grouping tasks such as named entity recognition.
The IOB tagging system contains tags in the format: 
<ul>B - (Beginning): for the word in the initial block;</ul>
<ul>I - (Inside): for words inside the block; </ul>
<ul>O - (Outside): Outside of any piece.</ul>
<p>

<p>After the transformation, we created a new collection called bio_tokens, where the tweets are separated by each word and tag, according to the IOB standard, resulting in: 
 <ul>I-Drug, B-Drug, I-ADR, B-ADR and O.</ul>
</p>

<p>The metrics to measure the performance of the model built in this project were:
<ul>-<strong>Precision</strong> measure is an evaluation metric based on the accuracy of its positive classification, that is, from the moment something is classified as positive, this metric evaluates how many were in fact classified correctly. In this project, precision aims to assess whether the words classified as medicines were, in fact, a medicine, for example.</ul>
<ul>-<strong>Recall</strong> measure, in turn, looks at the whole, that is, it uses the positive truth as a reference and compares it with the positive hit. In this project, the recall aims to evaluate among all the samples that really belonged to some entity (ADR or DRUG), how many of them the algorithm actually classified in the correct entity.</ul>
<ul>-<strong>F1-score</strong> is the harmonic mean between precision and recall.</ul>
The trained algorithm was applied to a database with approximately 9,571 thousand tweets. In this step, the built algorithm was able to identify 2,842 posts with the presence of Drug and/or ADR entities. Results: </p>

<img align="center" width='400px' src='https://user-images.githubusercontent.com/55667496/149041360-bcf3640d-dd47-415b-b21e-df586dabcf0d.png'>
 
#
This is part 3 of 5 of the course completion work. Developed by <a href="https://github.com/bpaixao">Beatriz Paixão</a> and <a href="https://github.com/katheleen-gregorato">Katheleen Gregorato</a>. See our publication in CONICT - IFSP at: https://bit.ly/3IsqULo
