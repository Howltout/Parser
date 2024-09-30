import argparse
import sys
from typing import List, Tuple, Dict
import re
from collections import Counter

def count_words(text: str) -> int:
    """Count the number of words in the given text.
    
    Args:
        text (str): The input text to count words in.
        
    Returns:
        int: The total number of words.
    """
    words = re.findall(r'\w+', text.lower())
    return len(words)

def count_chars(text: str) -> int:
    """Count the number of characters in the given text.
    
    Args:
        text (str): The input text to count characters in.
        
    Returns:
        int: The total number of characters.
    """
    return len(text)

def count_lines(text: str) -> int:
    """Count the number of lines in the given text.
    
    Args:
        text (str): The input text to count lines in.
        
    Returns:
        int: The total number of lines.
    """
    return len(text.splitlines())

def find_word(text: str, word: str) -> Dict[str, int]:
    """Find the occurrences of a specific word in the text.
    
    Args:
        text (str): The input text to search within.
        word (str): The word to find.
        
    Returns:
        Dict[str, int]: A dictionary with the word as the key and the count as the value.
    """
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    return {word: word_counts[word.lower()]}

def replace_word(text: str, old_word: str, new_word: str) -> Tuple[str, int]:
    """Replace occurrences of a specific word in the text with a new word.
    
    Args:
        text (str): The input text to modify.
        old_word (str): The word to replace.
        new_word (str): The word to use as a replacement.
        
    Returns:
        Tuple[str, int]: The modified text and the number of replacements made.
    """
    pattern = re.compile(r'\b' + re.escape(old_word) + r'\b', re.IGNORECASE)
    updated_text, count = re.subn(pattern, new_word, text)
    return updated_text, count

def get_word_frequency(text: str, top_n: int = 10) -> List[Tuple[str, int]]:
    """Get the top N most frequent words in the text.
    
    Args:
        text (str): The input text to analyze.
        top_n (int): The number of top frequent words to return.
        
    Returns:
        List[Tuple[str, int]]: A list of tuples containing words and their frequencies.
    """
    words = re.findall(r'\w+', text.lower())
    return Counter(words).most_common(top_n)

def process_file(file_path: str, args: argparse.Namespace) -> List[str]:
    """Process the given text file based on the provided arguments.
    
    Args:
        file_path (str): The path to the input text file.
        args (argparse.Namespace): The command-line arguments.
        
    Returns:
        List[str]: A list of results from the processing operations.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

    results = []

    if args.word_count:
        results.append(f"Word Count: {count_words(content)}")

    if args.char_count:
        results.append(f"Character Count: {count_chars(content)}")

    if args.line_count:
        results.append(f"Line Count: {count_lines(content)}")

    if args.find:
        frequency = find_word(content, args.find)
        results.append(f"The word '{args.find}' occurs {frequency[args.find]} times.")

    if args.replace:
        old_word, new_word = args.replace
        updated_content, replacements = replace_word(content, old_word, new_word)
        if replacements > 0:
            new_file_path = f"updated_{file_path}"
            try:
                with open(new_file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                results.append(f"'{old_word}' was replaced with '{new_word}' {replacements} times and saved to {new_file_path}")
            except IOError as e:
                results.append(f"Error writing to file '{new_file_path}': {e}")
        else:
            results.append(f"'{old_word}' was not found in the file.")

    if args.word_frequency:
        top_words = get_word_frequency(content, args.word_frequency)
        results.append("Top words by frequency:")
        for word, freq in top_words:
            results.append(f"  {word}: {freq}")

    return results

def main():
    """Main function to parse command-line arguments and process the file."""
    parser = argparse.ArgumentParser(description="Process a text file with various operations.")
    parser.add_argument('-f', '--file', required=True, help="Path to the input text file")
    parser.add_argument('-wc', '--word-count', action='store_true', help="Display the total word count")
    parser.add_argument('-cc', '--char-count', action='store_true', help="Display the total character count")
    parser.add_argument('-lc', '--line-count', action='store_true', help="Display the total line count")
    parser.add_argument('-find', '--find', help="A specific word to search in the text file")
    parser.add_argument('-r', '--replace', nargs=2, metavar=('OLD_WORD', 'NEW_WORD'),
                        help="Replace a word in the text file with another word")
    parser.add_argument('-wf', '--word-frequency', type=int, metavar='N',
                        help="Display the top N most frequent words")

    args = parser.parse_args()

    results = process_file(args.file, args)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
