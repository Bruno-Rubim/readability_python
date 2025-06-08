one_digit_words = [
    ["zero"],
    ["one"],
    ["two", "twen"],
    ["three", "thir"],
    ["four", "for"],
    ["five", "fif"],
    ["six"],
    ["seven"],
    ["eight"],
    ["nine"],
]

two_digit_words = ["ten", "eleven", "twelve"]
hundred = "hundred"
large_sum_words = [
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
    "sextillion",
    "septillion",
    "octillion",
    "nonillion",
]


def converter(string: str):
    word = []

    if string.startswith("-"):
        word.append("(negative)")
        string = string.removeprefix("-")

    # verifica se o numero de digitos é maior que 3 e não divisível por três
    if len(string) > 3 and len(string) % 3 != 0:
        # adiciona 0s à esquerda até que seja um número de dígitos multiplo de 3
        desiredLength = 3 * (((len(string) - 1) // 3) + 1)
        string = string.zfill(desiredLength)

    # divide a string em grupos de 3 digitos
    three_digit_list = [string[i : i + 3] for i in range(0, len(string), 3)]
    skip = False

    # para cada index e grupo de 3 digitos
    for i, three_digits in enumerate(three_digit_list):
        if three_digits != "000":
            skip = False

        for _ in range(len(three_digits)):
            # remove os 0s no inicio do grupo
            three_digits = three_digits.lstrip("0")
            if len(three_digits) == 1:
                if (
                    (
                        len(three_digit_list) > 1
                        or (
                            len(three_digit_list) == 1 and len(three_digit_list[0]) == 3
                        )
                    )
                    and i == len(three_digit_list) - 1
                    and (word[-1] in large_sum_words or hundred in word[-1])
                ):
                    word.append("and")

                word.append(one_digit_words[three_digits][0])
                # remove o primeiro digito
                three_digits = three_digits[1:]
                break

            if len(three_digits) == 2:
                if three_digits[0] != "0":
                    if (
                        len(three_digit_list) > 1
                        or (
                            len(three_digit_list) == 1 and len(three_digit_list[0]) == 3
                        )
                    ) and i == len(three_digit_list) - 1:
                        word.append("and")
                    if three_digits.startswith("1"):
                        if int(three_digits[1]) in range(3):
                            word.append(two_digit_words[int(three_digits[1])])
                        else:
                            number = one_digit_words[three_digits[1]][
                                1 if int(three_digits[1]) in range(3, 6, 2) else 0
                            ]
                            word.append(
                                number + ("teen" if not number[-1] == "t" else "een")
                            )
                    else:
                        word.append(
                            one_digit_words[three_digits[0]][
                                1 if int(three_digits[0]) in range(2, 6) else 0
                            ]
                            + ("ty " if three_digits[0] != "8" else "y ")
                            + (
                                one_digit_words[three_digits[1]][0]
                                if three_digits[1] != "0"
                                else ""
                            )
                        )
                    break
                else:
                    three_digits = three_digits[1:]
                    continue

            if len(three_digits) == 3:
                if three_digits[0] != "0":
                    word.append(one_digit_words[three_digits[0]][0] + " " + hundred)
                    if three_digits[1:] == "00":
                        break
                three_digits = three_digits[1:]

        if len(three_digit_list[i:]) > 1 and not skip:
            word.append(large_sum_words[len(three_digit_list[i:]) - 2])
            skip = True

    word = " ".join(map(str.strip, word))
    return (
        word[0].lstrip().upper() + word[1:].rstrip().lower()
        if "negative" not in word
        else word[:11].lstrip() + word[11].upper() + word[12:].rstrip().lower()
    )


if __name__ == "__main__":
    while True:
        try:
            n = input("Enter any number to convert it into words or 'exit' to stop: ")
            if n == "exit":
                break
            int(n)
            print(n, "-->", converter(n))
        except ValueError:
            print("Error: Invalid Number!")
