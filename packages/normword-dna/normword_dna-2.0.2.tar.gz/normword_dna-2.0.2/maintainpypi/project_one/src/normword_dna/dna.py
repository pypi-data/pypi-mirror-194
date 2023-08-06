def from_user(number_):
    ones = (
        "",
        "First",
        "Second",
        "Third",
        "Fourth",
        "Fifth",
        "Sixth",
        "Seventh",
        "Eight",
        "Ninth",
    )

    twos = (
        "Tenth",
        "Eleventh",
        "Twelve",
        "Thirteenth",
        "Fourteenth",
        "Fifteenth",
        "Sixteenth",
        "Seventeenth",
        "Eighteenth",
        "Nineteenth",
    )

    tens = (
        "Twenty",
        "Thirty",
        "Forty",
        "Fifty",
        "Sixty",
        "Seventy",
        "Eighty",
        "Ninety",
        "Hundred",
    )

    suffixes = ("", "Thousand", "Million", "Billion")

    def process(number, index):

        if number == "0":
            return "Zeroth"

        length = len(number)

        if length > 3:
            return False

        number = number.zfill(3)
        words = ""

        hdigit = int(number[0])
        tdigit = int(number[1])
        odigit = int(number[2])

        words += "" if number[0] == "0" else ones[hdigit]
        words += " Hundred " if not words == "" else ""

        if tdigit > 1:
            words += tens[tdigit - 2]
            words += " "
            words += ones[odigit]

        elif tdigit == 1:
            words += twos[(int(tdigit + odigit) % 10) - 1]

        elif tdigit == 0:
            words += ones[odigit]

        if words.endswith("Zero"):
            words = words[: -len("Zero")]
        else:
            words += " "

        if not len(words) == 0:
            words += suffixes[index]

        return words

    def getWords(number):
        length = len(str(number))

        if length > 2:
            return "|DNA Says| This program supports only birth date numbers which are between 1 to 31 ( *Note* : i have wrote this module for my personal use! ) Have a good day."

        count = length // 3 if length % 3 == 0 else length // 3 + 1
        copy = count
        words = []

        for i in range(length - 1, -1, -3):
            words.append(
                process(str(number)[0 if i - 2 <
                        0 else i - 2: i + 1], copy - count)
            )
            count -= 1

        final_words = ""
        for s in reversed(words):
            temp = s + " "
            final_words += temp

        return final_words

    number = int(number_)
    this = getWords(number)
    return this
