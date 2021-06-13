all_word = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"] #all lower case characters
consonant_word = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y",
                  "z"]
start_consonant_word = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x",
                        "z"]    #consonant words without y
vowel_word = ["a", "e", "i", "o", "u"]


#english to pig_latin general rules
def regular_rule(a):
    global return_value

#When the first word is upper case
    if a[0] not in all_word: #detect if first letter is upper case
        a = a[0].lower()+a[1:] #set the first letter to lower case

        if a[0] == "q" and a[1] == "u":  #edge case with "qu" at beginning
            a = a + "quay"
            a = a[2::]
            return_value = a.capitalize() #change the first letter back to upper case
            return return_value

        if a[0] in vowel_word: #first letter is vowel_word
            a = a + "yay"
            return_value = a.capitalize()
            return return_value


        if a [0] in start_consonant_word: #first letter is consonant_word
            if a [1] == "y":
                a = a + a[0]
                a = a[1::]
                a = a + "ay"
                return_value = a.capitalize()
                return return_value
            while a[0] in consonant_word:
                a = a + a[0]
                a = a[1::]
            a = a + "ay"
            return_value = a.capitalize()
            return return_value


        if a[0] == "y": #edge case first letter is y
            a = a + "y"
            a = a[1::]
            while a[0] in start_consonant_word:
                a = a + a[0]
                a = a[1::]
            a = a + "ey"
            return_value = a.capitalize()
            return return_value


# When the first word is lower case

    if a[0] == "q" and a[1] == "u": #edge case with "qu" at beginning
        a = a + "quay"
        a = a[2::]
        return_value = a
        return return_value

    if a[0] in vowel_word:  #first letter is vowel_word
        a = a + "yay"
        return_value = a
        return return_value

    if a [0] in start_consonant_word:  #first letter is consonant_word
        if a [1] == "y":
            a = a + a[0]
            a = a[1::]
            a = a + "ay"
            return_value = a
            return return_value
        while a[0] in consonant_word:
            a = a + a[0]
            a = a[1::]

        a = a + "ay"
        return_value = a
        return return_value


    if a[0] == "y":  #edge case first letter is y
        a = a + "y"
        a = a[1::]
        while a[0] in start_consonant_word:
            a = a + a[0]
            a = a[1::]
        a = a + "ey"
        return_value = a
        return return_value

#pig_latin to english general rules
def reverse_rule(a):
    global return_value
    import enchant as e
    dictionary = e.Dict('en_US')

#first letter is upper case
    if a[0] not in all_word: #detect if first letter is upper case
        a = a[0].lower()+a[1:] #change first letter to lower case

        if a[-1] == "y" and a[-2] == "a" and a[-3] == "y": #detect "yay" at ending and remove them
            a = a[0:-3]
            return_value = a.capitalize() #change the first letter back to upper case
            return return_value

        if a[-1] == "y" and a[-2] == "a" and a[-3] == "u" and a[-4] == "q": #detect "quay" at ending and remove them
            a = a[0:-4]
            a = "qu" + a
            return_value = a.capitalize()
            return return_value

        if a[-1] == "y" and a[-2] == "a": #detect the ending of the word
            a = a[0:-2]
            while not dictionary.check(a): #compare to the dictionary
                a = a[-1] + a[0:-1]
            return_value = a.capitalize()
            return return_value

        if a[-1] == "y" and a[-2] == "e": #detect the ending of the word
            a = a[0:-2]
            while not dictionary.check(a): #compare to the dictionary
                a = a[-1] + a[0:-1]
            return_value = a.capitalize()
            return return_value

#below is the same, the only difference is the first letter is in lower case
    if a[-1] == "y" and a[-2] == "a" and a[-3] == "y":
        a = a[0:-3]
        return_value = a
        return return_value

    if a[-1] == "y" and a[-2] == "a" and a[-3] == "u" and a[-4] == "q":
        a = a[0:-4]
        a = "qu" + a
        return_value = a
        return return_value

    if a[-1] == "y" and a[-2] == "a":
        a = a[0:-2]
        while not dictionary.check(a):
            a = a[-1] + a[0:-1]
        return_value = a
        return return_value

    if a[-1] == "y" and a[-2] == "e":
        a = a[0:-2]
        while not dictionary.check(a):
            a = a[-1] + a[0:-1]
        return_value = a
        return return_value


def english_to_pig_latin(a):
    c = []
    if "-" in a:
        a = a.split('-') #seperate the word around "-"
        for word in a:
            b = word
            regular_rule(b)
            c.append(return_value)
        print("-".join(c))
        return "-".join(c)
    elif "!" in a: #detect "!" remove it and add it back to the end
        a = a[0:-1]
        regular_rule(a)
        print(return_value + "!")
        return return_value + "!"
    else:
        regular_rule(a)
        print(return_value)
        return return_value


def pig_latin_to_english(a):
    c = []
    if "-" in a:  #seperate the word around "-"
        a = a.split('-')
        for word in a:
            b = word
            reverse_rule(b)
            c.append(return_value)
        print("-".join(c))
        return "-".join(c)
    elif "!" in a:  #detect "!" remove it and add it back to the end
        a = a[0:-1]
        reverse_rule(a)
        print(return_value + "!")
        return return_value + "!"
    else:
        reverse_rule(a)
        print(return_value)
        return return_value


out1 = english_to_pig_latin("hello")
out2 = pig_latin_to_english(out1)

