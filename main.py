from get_page import *

LENGTH = 1500

def main():
    page = get_rand_wiki_page()
    while len(page['text']) < LENGTH:
        print('too short')
        page = get_rand_wiki_page()

    toSpeak = 'Page of the day : ' + page['title'] + '. ' + \
    remove_extra_whitespace(soft_cut_string(page['text'],LENGTH).replace("\n"," ")) + \
    ' Read more at ' + page['url'] +'.'

    print(toSpeak)

if __name__ == '__main__':
    main()