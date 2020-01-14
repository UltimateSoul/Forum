from django.test import TestCase

# Create your tests here.

# SOLID
# SELF_CONFIDENCE
# OPEN-CLOSED
# Liscov Subtitution Priciple
# Interface Segregation Principle
# Dependency inversion Principle


string = "bill mother bill bill bill bill com abba dog abba mother com abba com mother "
words = string.split()
print(words)
sorted_list = list(sorted(words, key=lambda word: words.count(word)))[::-1]
values = []
for value in sorted_list:
    if value not in values:
        values.append(value)
print(values)