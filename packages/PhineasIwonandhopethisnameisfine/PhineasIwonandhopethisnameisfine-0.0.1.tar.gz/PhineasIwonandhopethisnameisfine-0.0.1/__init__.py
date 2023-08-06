def function_main(fdistsaveF, unique_meansF, word_meansF):
    artists = ["Kanye.txt", "Justin.txt", "Eminem.txt", "Dua.txt", "Drake.txt"]
    for index, artistinput in enumerate(artists):     # For loop which
        with open(artistinput, 'r', encoding="utf8") as file:
            Lyrics = file.read().rstrip('\n')

        tokenized_word = word_tokenize(Lyrics)
        fdist = FreqDist(tokenized_word)
        print("\n__________________________________________________\n")
        print(tokenized_word, "\n")
        fdistsave[index] = fdist    # save fdist messageS
        splitted = str(fdist).split()
        unique_means[index] = int(splitted[2])   # The number of unique words
        word_means[index] = int(splitted[5])
    for index, i in enumerate(fdistsave):
        print(artists[index], ": \n", i, "\n")     # prints the name of the artist

    unique_std = [300, 300, 300, 300, 300]
    word_std = [1000, 1000, 1000, 1000, 1000]
    width = 0.7    # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(artists, unique_means, width, yerr=unique_std, label='# of unique words')
    ax.bar(artists, word_means, width, yerr=word_std, bottom=unique_means,
        label='# of words')

    ax.set_ylabel('Number of words')
    ax.set_title('Number of unique words compared to the number of words in songs')
    ax.legend()

    plt.show()  # Show graphic
