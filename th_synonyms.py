"""
At Top Hat, an answer that doesn’t match exactly may be correct
if it uses synonyms of the right answer.

Given a list of tuples of words that are synonyms
and a list of expected/actual answer tuples,
return a list of booleans indicating if each answer is correct.


Given:
"""
SYNONYMS = [("quick", "fast"), ("runs", "sprints"), ("runner", "athlete")]
ANSWERS = [
    ("Usain Bolt is a fast athlete", "Usain Bolt is a quick runner"),
    ("The runner sprints to the finish", "The athlete runs to the finish"),
    ("The long jump record is 8.9 metres", "The high jump record is 8.9 metres"),
]
"""
Output:
correct_answers() -> [True, True, False]
"""

### ASSUMPTIONS ###
# transitive i.e. a -> b -> c => a -> c (false)
# reflexive i.e. a -> b => b -> a       (true)
# always one word i.e. no phrases       (true)
# case sensitive                        (false)

### SOLUTION ###
from collections import defaultdict


def map_synonyms(pairs):
    synonyms = defaultdict(set)
    for word_one, word_two in pairs:
        synonyms[word_one].add(word_two)
        synonyms[word_two].add(word_one)
    return synonyms


def to_lowercase_words(sentence):
    return [word.lower() for word in sentence.split()]


def is_correct(sentences, synonyms):
    words_expected, words_actual = map(to_lowercase_words, sentences)
    len_expected = len(words_expected)
    len_actual = len(words_actual)
    if len_expected != len_actual:
        return False

    for i in range(min(len_expected, len_actual)):
        expected_word = words_expected[i]
        actual_word = words_actual[i]
        is_equal = expected_word == actual_word
        is_synonym = actual_word in synonyms.get(expected_word, set())
        if not (is_equal or is_synonym):
            return False

    return True


def correct_answers():
    synonyms = map_synonyms(SYNONYMS)
    print([is_correct(sentences, synonyms) for sentences in ANSWERS])


correct_answers()
