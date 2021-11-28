import math
import re


class Bayes_Classifier:

    def __init__(self):

        # Dictionary of all the positive words from the reviews
        self.positive_dict = {}
        # Dictionary of all the negative words from the reviews
        self.negative_dict = {}

        # count of all positive reviews
        self.num_pos = 0
        # count of all negative reviews
        self.num_neg = 0

        # count of all the unique words from the reviews
        self.unique_words = 0
        # count of all unique positive words from the reviews
        self.unique_positive = 0
        # count of all unique negative words from the review
        self.unique_negative = 0

    def train(self, lines):
        """
        [summary]

        Args:
            lines ([list]): 
            Each line of data is of the form:
            NUMBER OF STARS|ID|TEXT
            - The number of stars is 1 or 5. 
            - The text goes until a newline (`\n`). 
            - The text won't contain a '|', so you can safely invoke `split('|')`.
        """

        for line in lines:
            # replace all next line commands with blank spaces
            line = line.replace('\n', '')
            # split the text data using at every '|' into various sections
            sections = line.split('|')
            # the section at 0th index is the rating either 1 or 5
            rating = sections[0]
            # the section at 2nd index is the review for that particular movie
            review = sections[2]

            # We perform the data cleaning operation the definition to which is mentioned under the 'review_cleaning' function
            updated_review = self.review_cleaning(review)

            if rating == '5':
                # add 1 to the count of positive reviews if the rating is '5'
                self.num_pos += 1
                for word in updated_review.split():
                    # if the word is not already present in the positive dictionary list, set the frequency of the word as 1 and increment the counter by 1
                    if word not in self.positive_dict:
                        self.positive_dict[word] = 1
                        self.unique_positive += 1

                        # if the word not present in the dictionary of negative words, add it to the count of unique words
                        if word not in self.negative_dict:
                            self.unique_words += 1

                    else:
                        # if the word is already present in the dictionary, increment frequency and well as the counter by 1
                        self.positive_dict[word] += 1
                        self.unique_positive += 1
            else:
                # add 1 to the count of negative reviews if the rating is '1'
                self.num_neg += 1
                for word in updated_review.split():
                    # if the word is not already present in the negative dictionary list, set the frequency of the word as 1 and increment the counter by 1
                    if word not in self.negative_dict:
                        self.negative_dict[word] = 1
                        self.unique_negative += 1

                        # if the word not present in the dictionary of positive words, add it to the count of unique words
                        if word not in self.positive_dict:
                            self.unique_words += 1

                    else:
                        # if the word is already present in the dictionary, increment frequency and well as the counter by 1
                        self.negative_dict[word] += 1
                        self.unique_negative += 1

    def classify(self, lines):
        """
        This function is used to classify the reviews into positive or negative reviews using the naive bayes algorithm.

        The probability of a review being positive given a set of features $f$ can be calculated as:
        P(positive \ | \ f) = P(positive) * \prod^n_{i=1} P(f_i \ | \ positive)

        Args:
            lines ([list]): 
            Each line of data is of the form:
            NUMBER OF STARS|ID|TEXT
            - The number of stars is 1 or 5. 
            - The text goes until a newline (`\n`). 
            - The text won't contain a '|', so you can safely invoke `split('|')`.

        Returns:
            prediction[String]: returns string '5' if it is a positive review  else returns string '1' if its a negative review
        """

        prediction = []

        for line in lines:
            line = line.replace('\n', '')
            sections = line.split('|')
            review = sections[2]

            # We perform the data cleaning operation the definition to which is mentioned under the 'review_cleaning' function
            updated_review = self.review_cleaning(review)

            '''
            probability of a review being positive = number of positive reviews / total number of reviews in the dataset
            probability of a review being negative = number of negative reviews / total number of reviews in the dataset
            '''

            positive_prob = self.num_pos / float(self.num_pos + self.num_neg)
            negative_prob = self.num_neg / float(self.num_pos + self.num_neg)

            '''
            Since probabilities can become very small, the product of these numbers can result in underflow. 
            To get around this, use *log-probabilities* (in which case, products become sums).
            '''
            positive_prob = math.log10(positive_prob)
            negative_prob = math.log10(negative_prob)

            for word in updated_review.split():
                if word in self.positive_dict:
                    positive_prob += math.log10((self.positive_dict[word] + 1) / float(
                        self.unique_positive + self.unique_words))
                else:
                    positive_prob += math.log10(1 /
                                                float(self.unique_positive + self.unique_words))

                if word in self.negative_dict:
                    negative_prob += math.log10((self.negative_dict[word] + 1) / float(
                        self.unique_negative + self.unique_words))
                else:
                    negative_prob += math.log10(1 /
                                                float(self.unique_negative + self.unique_words))

            if positive_prob > negative_prob:
                prediction.append('5')
            else:
                prediction.append('1')

        return prediction

    def review_cleaning(self, review):
        """ 
        This function is used to perform data cleaning. Raw social media messages are full of noise that could 
        prevent further steps from achieving the expected performance. In order to remove such noise, the data 
        cleaning process does the following: 1. Lowercasing the textual content 2. Removing hash tags, usernames, 
        and hyperlink 3. Removing stop words 4. Removing special characters and punctuation marks

        Returns:
            updated_review[string]: Returns a string of unique words which does not contain any special symbols or 
            punctuations as well as most commonly used words or stop words.
        """

        # List of punctuation symbols and special characters
        punctuation_list = ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+',
                            ',', '.', '/', ':', ';', '=', '?', '!']

        # List of stop words
        stop_words_list = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
                           'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being',
                           'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could',
                           'did', 'do', 'does', 'doing', 'down', 'during', 'each',
                           'few', 'for', 'from', 'further', 'had', 'has', 'have',
                           'having', 'he', 'her', 'here', 'hers', 'herself',
                           'him', 'himself', 'his', 'how', 'hows', 'i', 'im', 'if', 'in',
                           'into', 'is', 'it', 'its', 'its', 'itself', 'lets', 'me', 'more', 'most',
                           'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only',
                           'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
                           'same', 'she', 'should', 'so',
                           'some', 'such', 'than', 'that', 'thats', 'the', 'their', 'theirs', 'them',
                           'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd', 'theyll',
                           'theyve', 'this', 'those', 'through', 'to', 'too',
                           'under', 'until', 'up', 'very', 'was', 'we', 'wed', 'well', 'were',
                           'weve', 'were', 'what', 'whats', 'when', 'whens', 'where',
                           'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with',
                           'wont', 'would', 'you', 'youd', 'youll', 'youre', 'youve', 'your',
                           'yours', 'yourself', 'yourselves']

        # converting the whole review into a lower case format so that it becomes easier for data cleaning.
        review = review.lower()

        '''
        In the review if you come across any of the characters from the punctuation list, 
        we replace that character using a blank space so that we get standardised string data for
        the cleaning process
        '''

        # replace all characters with a blank space to make the cleaning an easier process
        for character in review:
            if character in punctuation_list:
                review = review.replace(character, ' ')

        split = review.split()

        for i in range(len(split)):
            if split[i] == 'not' and i + 1 != len(split):
                split[i] = split[i] + split[i+1]
                split[i+1] = ''

        # drop all stop words from the reviews as they are unnecessary
        for word in split:
            if word in stop_words_list:
                split.remove(word)

        updated_review = ' '.join(map(str, split))

        return updated_review
