# Alice in Wonderland

## Summarization

### 1 - Get book content
![image](/alice_assets/md/summarization/summarization_1.png)

### 2 - Clean book content
![image](/alice_assets/md/summarization/summarization_2.png)

#### 2.1 - Normalize all line break
![image](/alice_assets/md/summarization/summarization_3.png)

#### 2.2 - Normalize skip line (1 max)
![image](/alice_assets/md/summarization/summarization_4.png)

#### 2.3 - Return cleaned book
![image](/alice_assets/md/summarization/summarization_5.png)

### 3 - Text segmentation

#### 3.1 - Normalize spaces
![image](/alice_assets/md/summarization/summarization_6.png)

#### 3.2 - Split text into sentences
![image](/alice_assets/md/summarization/summarization_7.png)

#### 3.3 - Return list of sentences
![image](/alice_assets/md/summarization/summarization_8.png)

### 4 - Score sentences
![image](/alice_assets/md/summarization/summarization_9.png)

#### 4.1 - Get words frequency
![image](/alice_assets/md/summarization/summarization_10.png)

#### 4.2 - Score sentences by usefull words rate
![image](/alice_assets/md/summarization/summarization_11.png)

#### 4.3 - Return list of scored sentences (sentence, score)
![image](/alice_assets/md/summarization/summarization_12.png)

### 5 - Build summary
![image](/alice_assets/md/summarization/summarization_13.png)

#### 5.1 - Index sentences
![image](/alice_assets/md/summarization/summarization_14.png)

#### 5.2 - Sort sentences by score
![image](/alice_assets/md/summarization/summarization_15.png)

#### 5.3 - Remove possible duplicates and keep only n sentences
![image](/alice_assets/md/summarization/summarization_16.png)

#### 5.4 - Sort sentences by index
![image](/alice_assets/md/summarization/summarization_17.png)

#### 5.5 - Remove empty sentences
![image](/alice_assets/md/summarization/summarization_18.png)

#### 5.6 - Return cleaned n sentences
![image](/alice_assets/md/summarization/summarization_19.png)

### 6 - Return summary
![image](/alice_assets/md/summarization/summarization_20.png)