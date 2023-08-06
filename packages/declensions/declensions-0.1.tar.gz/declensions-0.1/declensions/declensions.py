def decline(word: str, quantity: int, endings: dict) -> str:
    '''decline - function for declension of the transmitted word depending on the transmitted number of letters.

    :: word - the singular word that will incline; 
    :: quantity - the number depending on which the word will be inclined;
    :: endings - possible endings of the transmitted word depending on the declension variant* Example: {'first': 'ека', 'second': 'ек'}.

    * - there are two declension options - the first and the second. 
        The first option is a declination in which the last digit in the number is equal to one of these numbers - '2', '3', '4'; 
        The second option is that the last digit in the number is equal to one of these numbers -'5', '6', '7', '8', '9', '0'. '''


    if isinstance(word, str) and isinstance(quantity, int) and isinstance(endings, dict):
        # The last number in the quantity.
        last_quantity_number = str(quantity)[len(str(quantity)) - 1]

        
        if last_quantity_number == '1':
            # The word will not be declined, since it is in the singular.
            inclined_word = word

        elif last_quantity_number in ['2', '3', '4']: # the first variant of declension.
            ending = word[len(word)-2:] # the end of the transmitted word.

            inclined_word = word.replace(ending, endings['first']) # replacement of the ending in the word ( declension of the word )            

        elif last_quantity_number in ['5', '6', '7', '8', '9', '0']: # the second variant of declension.
            ending = word[len(word)-2:] # the end of the transmitted word.

            inclined_word = word.replace(ending, endings['second']) # replacement of the ending in the word ( declension of the word )

        else:
            # If the word could not be declined, an abbreviated version of the originally transmitted word will be returned.
            # Example: "days" -> "d."
            inclined_word = f'{word[0]}.'


        # Returning the resulting word after declension.
        return inclined_word


    else:
        if isinstance(word, str) == False:
            raise(TypeError('the word argument must contain the string.'))

        elif isinstance(word, int) == False:
            raise(TypeError('the quantity argument must contain the integer.'))

        elif isinstance(endings, int) == False:
            raise(TypeError('the endings argument must contain the dictionary.'))