HINTS = ['wp', 'login', 'includes', 'admin', 
'content', 'site', 'images', 'js', 'alibaba', 
'css', 'myaccount', 'dropbox', 'themes', 'plugins', 'signin', 'view']

def url_length(url):
    return len(url) 

def https_token(scheme):
    if scheme == 'https':
        return 0
    return 1

def char_repeat(words_raw):
            
    def __all_same(items):
                return all(x == items[0] for x in items)

    repeat = {'2': 0, '3': 0, '4': 0, '5': 0}
    part = [2, 3, 4, 5]

    for word in words_raw:
        for char_repeat_count in part:
            for i in range(len(word) - char_repeat_count + 1):
                sub_word = word[i:i + char_repeat_count]
                if __all_same(sub_word):
                    repeat[str(char_repeat_count)] = repeat[str(char_repeat_count)] + 1
    return  sum(list(repeat.values()))

def length_word_raw(words_raw):
    return len(words_raw) 

def average_word_length(words_raw):
    if len(words_raw) ==0:
        return 0
    return sum(len(word) for word in words_raw) / len(words_raw)

def longest_word_length(words_raw):
    if len(words_raw) ==0:
        return 0
    return max(len(word) for word in words_raw) 

def shortest_word_length(words_raw):
    if len(words_raw) ==0:
        return 0
    return min(len(word) for word in words_raw) 

def count_hyphens(base_url):
    if base_url is None:
        return 0
    return base_url.count('-')

def phish_hints(url_path):
    count = 0
    for hint in HINTS:
        count += url_path.lower().count(hint)
    return count
