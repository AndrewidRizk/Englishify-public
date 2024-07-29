import requests
import wikitextparser as wtp
from html import unescape
import re
from pattern.en import conjugate, lemma

def get_wiktionary_content(word):
    url = f"https://en.wiktionary.org/w/api.php?action=parse&page={word}&prop=wikitext&format=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        content = data.get("parse", {}).get("wikitext", {}).get("*", "")
        return content
    else:
        return None

def clean_definition(definition):
    # Remove unwanted markup and clean up the definition
    cleaned = re.sub(r'\{\{.*?\}\}\s*', '', definition).strip()
    cleaned = unescape(cleaned)  # unescape HTML entities
    return cleaned

def parse_wiktionary_content(content):
    parsed = wtp.parse(content)
    sections = parsed.sections

    word_data = []
    
    for section in sections:
        if section.title and section.title.strip() == 'English':
            english_subsections = section.sections
            for english_subsection in english_subsections:
                if english_subsection.title and english_subsection.title.strip() == 'Etymology 1':
                    etymology_subsections = english_subsection.sections
                    for etymology_subsection in etymology_subsections:
                        if etymology_subsection.title and etymology_subsection.title.strip() in ['Verb', 'Noun', 'Adverb', 'Adjective', 'Pronoun', 'Preposition', 'Conjunction']:
                            definitions = []
                            for line in etymology_subsection.contents.split('\n'):
                                if line.startswith('# '):
                                    cleaned_def = clean_definition(line)
                                    if cleaned_def:
                                        definitions.append(cleaned_def)
                            
                            word_data.append({
                                'part_of_speech': etymology_subsection.title.strip(),
                                'definitions': definitions
                            })
                    break  # Exit after processing the Etymology 1 section
            break  # Exit after processing the English section

    return word_data

# Function to get verb forms using Pattern
def get_verb_forms(verb):
    forms = {
        'present': lemma(verb),
        'third_person_singular_present': conjugate(verb, '3sg'),
        'present_participle': conjugate(verb, 'part'),
        'simple_past': conjugate(verb, 'p'),
        'past_participle': conjugate(verb, 'ppart')
    }
    return forms

# Example usage
def main():
    word = "swim"
    content = get_wiktionary_content(word)

    if content:
        parsed_data = parse_wiktionary_content(content)
        print(f"{word}:")
        for entry in parsed_data:
            print(f"Part of speech: {entry['part_of_speech']}")
            if entry['part_of_speech'] == 'Verb':  # Check if part of speech is a verb
                verb_forms = get_verb_forms(word)
                print("Definitions:")
                for idx, definition in enumerate(entry["definitions"], start=1):
                    print(f" - {idx}. {definition}")
                print("Verb Forms:")
                for form, value in verb_forms.items():
                    print(f" - {form.replace('_', ' ').title()}: {value}")
            else:
                for idx, definition in enumerate(entry["definitions"], start=1):
                    print(f" - {idx}. {definition}")
    else:
        print(f"Could not fetch content for the word: {word}")

if __name__ == "__main__":
    main()