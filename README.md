# Contribution guide
Do you want to help make this god awful project even worse? Here's a handy guide as to how to do that!
## Adding quotes
You can do this in one of two ways, depending on your expertise.
1. Send them to me personally over [https://twitter.com/_lynnux](Twitter) for me to add them manually. This is probably what you want to do.
2. Add them in the source code and create a pull request; if you have a little Python experience, this is easier for me. Basically, lines are formatted in `meme_templates.py` as follows:
    + Character names are replaced with numbers in braces corresponding to their order of appearance in the line. **Python is zero-indexed, so the first character is {0}, the second is {1}, etc.**
    + Personal pronouns of characters are all replaced with they/them pronouns. *(Note: This isn't ideal, but there's no easy way to address it. Feel free to create an issue or DM me if you have ideas.)*
    + For example, the line "Phoenix Wright is friends with Larry Butz. Phoenix met Larry when he was in elementary school." would become `{0} is friends with {1}. {0} met {1} when they were in elementary school."
    + Lines in the `quotes` category are actually key:value pairs, where the key is the quote and the value is the number of characters involved. Take a look at this quote for an example:
        ```
        """
        {0}: Look {1}
        {0}: Everything the light touches
        {0}: Is too tall for you to reach
        """:2
        ```

## Modifying the code itself
### Basic setup
You'll need [https://docs.conda.io/en/latest/](Conda) for this. Clone the repository and run `conda env create -f environment.yml`. The environment is named `misery`, so once the environment is created, run `conda activate misery` to enter the environment. When you're done, run `conda deactivate misery`.
### Running the webserver
Go to the root of the repository and run `flask run` for a dev server.
