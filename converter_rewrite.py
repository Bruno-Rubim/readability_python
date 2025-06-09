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


def converter(enterString: str):
    word = []

    if enterString.startswith("-"):
        word.append("(negative)")
        enterString = enterString.removeprefix("-")

    # verifica se o numero de digitos é maior que 3 e não divisível por três
    if len(enterString) > 3 and len(enterString) % 3 != 0:
        # adiciona 0s à esquerda até que seja um número de dígitos multiplo de 3
        desiredLength = 3 * (((len(enterString) - 1) // 3) + 1)
        enterString = enterString.zfill(desiredLength)

    # divide a string em grupos de 3 digitos
    three_digit_list = [enterString[i : i + 3] for i in range(0, len(enterString), 3)]
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
                        # tenha pelo menos 2 grupos de 3 digitos
                        len(three_digit_list) > 1
                        or (
                            # tenha exatamente 3 digitos
                            len(three_digit_list) == 1
                            and len(three_digit_list[0]) == 3
                        )
                    )
                    # seja o ultimo da lista de 3 digitos
                    and i == len(three_digit_list) - 1
                    # tenha uma das "palavras de grande numeros"
                    and (word[-1] in large_sum_words or "hundred" in word[-1])
                ):
                    word.append("and")

                # adiciona o primeiro digito dos 3 digitos atuais à palavra
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
                    # adiciona palavra da centena
                    word.append(one_digit_words[three_digits[0]][0] + " " + hundred)
                    # essa parte não faz diferença
                    # if three_digits[1:] == "00":
                    #     break
                # remove o 0 à esquerda
                three_digits = three_digits[1:]

        if len(three_digit_list) > 2 and not skip:
            word.append(large_sum_words[len(three_digit_list) - 3])
            skip = True

    word = " ".join(map(str.strip, word))

    if "negative" not in word:
        return word[0].lstrip().upper() + word[1:].rstrip().lower()
    else:
        return word[:11].lstrip() + word[11].upper() + word[12:].rstrip().lower()


if __name__ == "__main__":
    while True:
        try:
            inputString = input(
                "Enter any number to convert it into words or 'exit' to stop: "
            )
            if inputString == "exit":
                break
            int(inputString)
            print(inputString, "-->", converter(inputString))
        except ValueError:
            print("Error: Invalid Number!")
