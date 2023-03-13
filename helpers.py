__diactrics = {
    'ç':'c', 'à':'a', 'â':'a', 
    'é':'e', 'è':'e', 'ê':'e', 'ë':'e',
    'î':'i', 'ï':'i', 'ô':'o', 
    'ù':'u', 'û':'u', 'ü':'u', 'ÿ':'y'
}

# Returns None if diactric origin wasn't found else returns original letter
def find_diactric_origin(letter):
    global __diactrics
    # Assumes letter is lower case and in unicode
    if letter in __diactrics:
        return __diactrics[letter]
    else:
        return None

# Generates an SQL query that inserts data about french word 
def generate_word_addition(word):
    assert len(word) > 0, "generate_word_addition only accepts non-empty words"
    word = word.lower()
    
    # Find diactrics to ensure that they are inserted in Letter table
    diactrics = {}
    for letter in word:
        diactric_origin = find_diactric_origin(letter)
        if diactric_origin is not None:
            diactrics[letter] = diactric_origin
    
    result = ["BEGIN TRANSACTION;"]
    
    insert_relations = "INSERT INTO Letter(unicode) VALUES"
    letters_commands = []
    for letter in word:
        letters_commands.append(f"(\'{letter}\')")
    for diactric_origin in diactrics.values():
        letters_commands.append(f"(\'{diactric_origin}\')")
    result.append(insert_relations + ",".join(letters_commands) + ";")
    # Query example: INSERT INTO Letter(symbol) VALUES('t'),('h'),('e');
    
    insert_relations = "INSERT INTO IsDiactricOf(diactric_letter_id,original_letter_id) SELECT "\
        "L1.letter_id AS diactric_letter_id, L2.letter_id AS original_letter_id FROM Letter AS L1 INNER JOIN Letter AS L2 where "
    
    diactric_relations = []
    for diactric, origin in diactrics.items():
        diactric_relations.append(
            f"(L1.unicode=\'{diactric}\' and L2.unicode=\'{origin}\')"
        )
    result.append(
        insert_relations + " or ".join(diactric_relations) + ";"
    )
    # Query example: INSERT INTO IsDiactricOf(diactric_letter_id,original_letter_id) ... WHERE (L1.unicode = 'â' and L2.unicode = 'a');
    
    result.append(
        f"INSERT INTO WordCore(word,length,last_letter_id) SELECT "\
            f"\"{word}\", {len(word)}, T.letter_id FROM Letter AS T WHERE symbol = \'{word[-1]}\';"
    )
    
    insert_relations = "INSERT INTO Contains(word_id,letter_id) SELECT "\
        "W.word_id, L.letter_id FROM WordCore AS W, Letter AS L WHERE "
    contains_relations = []
    for letter in word:
        contains_relations.append(
            f"(W.word=\'{word}\' and L.unicode=\'{letter}\')"
        )
    result.append(insert_relations + " or ".join(contains_relations) + ";")
    # Query example: INSERT INTO Contains(word_id,letter_id) ... WHERE (W.word = 'la' and L.unicode = 'a');

    insert_relations = "INSERT INTO GoesAfter(letter_before_id, letter_after_id) SELECT "\
        "L1.letter_id AS letter_before_id, L2.letter_id AS letter_after_id FROM Letter AS L1 INNER JOIN Letter AS L2 where "
        
    goes_after_relations = []
    for i in range(len(word) - 1):
        goes_after_relations.append(
            f"(L1.unicode=\'{word[i]}\' and L2.unicode=\'{word[i + 1]}\')"
        )
    result.append(insert_relations + " or ".join(goes_after_relations) + ";")
    # Query example: INSERT INTO Contains(word_id,letter_id) ... WHERE (L1.unicode = 'l' and L2.unicode = 'a');
    
    result.append("END TRANSACTION;")
    
    return "\n".join(result)