
from string import punctuation

class GetKeyWords:
    def extract_keywords(nlp, sequence, special_tags: list = None):
        result = []
        pos_tag = ['PROPN', 'NOUN', 'ADJ']

        doc = nlp(sequence.lower())

        if special_tags:
            tags = [tag.lower() for tag in special_tags]
            for token in doc:
                if token.text in tags:
                    result.append(token.text)

        for chunk in doc.noun_chunks:
            final_chunk = ""
            for token in chunk:
                if (token.pos_ in pos_tag):
                    final_chunk = final_chunk + token.text + " "
            if final_chunk:
                result.append(final_chunk.strip())

        for token in doc:
            if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
                continue
            if (token.pos_ in pos_tag):
                result.append(token.text)
        return list(set(result))

# if __name__ == "__main__":
#     """
#     install the langauge model using the subprocess package
#     useful when hosting the service in the cloud as it prevents against
#     us forgetting to do this via the CLI
#     """
#     subprocess.call("python -m spacy download en_core_web_sm", shell=True)
#
#     # load the small english language model,
#     nlp = spacy.load("en_core_web_sm")


# print(extract_keywords(nlp, """Alex Pothen's research interests are in combinatorial scientific computing (CSC), parallel algorithms, graph algorithms, and bioinformatics. CSC is an interdisciplinary research area where discrete mathematics and algorithms are applied to combinatorial problems from the sciences and engineering. CSC links scientific computing with algorithmic computer science."""))
