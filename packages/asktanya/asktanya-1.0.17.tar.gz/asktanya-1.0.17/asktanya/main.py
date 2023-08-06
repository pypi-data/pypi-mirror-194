from asktanya.func import how_to, try_ask, headers
from bs4 import BeautifulSoup
import requests


def ask_tanya(question):

    html = requests.get(f'https://www.google.com/search?q="{question}', headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")

    answer1 = ""
    answer2 = ""
    q = question.lower()
    print(f"\nQUESTION:\n{q.capitalize().strip('?')}?\n")
    print("ANSWER: ")
    if "who" in q:
        try:
            answer1 = soup.select_one(
                ".FLP8od"
            ).text  # "LEsW6e DVGBBd"><div class="wDYxhc NFQFxe oHglmf xzPb7d"
            answer2 = soup.select_one(".NFQFxe").text
            # print('Who is ___, exp: Who is the president of United States?')
        except:
            return try_ask(soup, question)

        if answer2 != "":
            return f"{answer1} - {answer2}"
        return answer1
    elif "where" in q:
        try:
            answer1 = soup.select_one(".hgKElc").text
            # print('Q: where is? ')
            return answer1

        except:
            try:
                answer1 = soup.select_one(".vk_sh").text

                return answer1

            except:
                return try_ask(soup, question)
    elif "when" in q:
        try:
            answer1 = soup.select_one(".zCubwf").text
            # print('Q: when is? ')
            return answer1
        except:
            return try_ask(soup, question)
    elif "how" in q:
        try:
            if "how to" in q:
                answer1 = how_to(q)
                # print('how to____ source: wikihow? ')
                return answer1
            else:
                try:
                    answer1 = soup.select_one(".ILfuVd").text
                    # print('Q: why is ___ cond? ')
                    return answer1
                except:
                    return try_ask(soup, q)
        except:
            return try_ask(soup, question)
    else:
        answer1 = try_ask(soup, question)
    answer2 = answer2.split(".")[0]
    return answer1


if __name__ == "__main__":
    print(ask_tanya(input("Ask Tanya anything! \nType your question here: ")))
